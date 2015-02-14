import copy
import threading

import cv2

index_slot = None
frame_slot = None

cv = threading.Condition()

def frame_worker(video):
    """ Thread to open video and serve frames by index. """
    global index_slot
    global frame_slot
    global cv

    cv.acquire()
    capture = cv2.VideoCapture(video.video_path)

    # Save frame information and notify waiting main() thread.
    video.width = int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)) 
    video.height = int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)) 
    video.nframes = int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    cv.notify()

    # Accept requests from get_frame() indefinitely.
    while True:
        # Wait from queries from get_frame instance.
        cv.wait()
        index = index_slot
        index_slot = None 
        assert(index < video.nframes)
        if index == -1:
            # Exit loop and return -1 upon get_frame(-1).
            frame_slot = -1 
            cv.notify()
            break
        # Set pointer to next frame to index.
        capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, index)
        success, frame = capture.read()
        if not success:
            raise Exception("Failed to read frame {0}".format(index))
        # Send frame to get_frame() call.
        assert(frame_slot is None)
        frame_slot = frame
        cv.notify()

    # Close video and return.
    capture.release() 
    cv.release()

def get_frame(index):
    """ Get frame at 'index' from video currently loaded in frame_worker. """
    global index_slot
    global frame_slot
    global cv

    # Send index to frame_worker.  
    cv.acquire()
    assert(index_slot is None)
    index_slot = index

    # we know the frame worker thread is waiting because get_frame calls are
    # all from same thread
    cv.notify() 

    # Wait for frame_worker to load frame.
    cv.wait()
    # Copy and then wipe slot contents.
    frame = copy.deepcopy(frame_slot)
    frame_slot = None
    cv.release()
    return frame
