import optparse 
import sys

from frame import start_frame_worker, exit_frame_worker 
from video import Video

from pdf import PDF 

def parse_arg_list(argv):
    """
    Parse user-supplied command-line arguments.
    Returns an options object of valid options with supplied values. 
    """
    parser = optparse.OptionParser()
 
    # define program options
    parser.add_option("-u", "--url", type="string", dest="url", 
            help="Video URL")
    parser.add_option("-o", "--output", type="string", dest="output", 
            help="Output filename (default: <readable_id>.pdf")

    (options, args) = parser.parse_args()

    # error upon extraneous options having been provided
    if args:
        raise Exception("Command line input not understood: ", args)

    return options

def main():
    # get options from command-line arguments
    options = parse_arg_list(sys.argv[1:])

    # initialize video
    video_url = options.url
    video = Video(video_url)
    video.get_metadata()
    video.download()

    # initialize output pdf
    out_fn = options.output
    pdf = PDF(video, out_fn)

    # start thread to serve video frames
    frame_worker = start_frame_worker(video)

    # kill frame worker thread
    exit_frame_worker(frame_worker)

if __name__ == "__main__":
    main()
