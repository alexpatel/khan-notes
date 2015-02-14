import json
import os
import urllib2 
import urlparse

import settings

class Video:
    def __init__(self, video_url):
        self.video_url = video_url

    def extract_readable_id(self):
        """ Extract readable id from video url. Save to self.readable_id. """
        parsed = urlparse.urlparse(self.video_url)
        # validate url
        if not parsed.hostname == 'www.khanacademy.org':
            raise Exception("Invalid URL:", parsed_url)
        # readable_id is last subpath in url
        path = parsed.path
        subpaths = path.split('/')
        self.readable_id = subpaths[len(subpaths) - 1]

    def query_video_data(self):
        """ Query video metadata from Khan Academy API. """
        readable_id = self.readable_id 
        api_base = "http://www.khanacademy.org/api/v1/videos/{0}" 
        api_query = api_base.format(self.readable_id)
        request = urllib2.Request(api_query)
        try:
            response = urllib2.urlopen(request)
            data = json.loads(response.read())
            self.raw_json = data
        except urllib2.URLError, AttributeError:
            Exception("Unable to access Khan Academy API: ", api_query)

    def set_video_path(self):
        """ Set the path where the video will be downloaded.  """
        assert(self.readable_id)
        # make video directory if it doesn't already exist
        try:
            os.mkdir(settings.video_dir)
        except Exception:
            pass
        # create filename
        self.video_path = os.path.join(settings.video_dir, self.readable_id + ".mp4")

    def extract_json_data(self):
        """ Extract video metadata from raw API response. """
        raw_json = self.raw_json
        self.description = raw_json['description']
        self.title = raw_json['title']
        self.duration = raw_json['duration']
        self.download_urls = raw_json['download_urls'] 
        if self.download_urls['mp4']:
            self.mp4 = self.download_urls['mp4']
            self.set_video_path()
        else:
            raise Exception("No MP4 available for video.")

    def get_metadata(self):
        """
        Find and store appropriate video metadata.
        """
        print "Getting video metadata..."
        self.extract_readable_id()
        self.query_video_data() 
        self.extract_json_data()

    def download(self):
        """ Download .mp4 version of video and saves to self.video_path. """
        if os.path.isfile(self.video_path):
            print "Video already downloaded. Skipping..."
            return
        print "Downloading video..."
        try:
            downloader = urllib2.urlopen(self.mp4) 
            temp_video = open(self.video_path, 'wb')
            temp_video.write(downloader.read())
        except urllib2.URLError, e:
            Exception("Unable to download video: ", self.mp4)

    @staticmethod
    def _secs_to_hms(secs):
        """ Return seconds as string in format hh:mm:ss. """
        mins, secs = divmod(secs, 60)
        hrs, mins = divmod(mins, 60)
        return "%d:%02d:%02d" % (hrs, mins, secs)

    def get_duration(self):
        """ Video duration as string in hh:mm:ss. """
        return self._secs_to_hms(self.duration)

    def get_frame_time(self, frame_num):
        """ Time of frame_num in video as string in format hh:mm:ss. """
        secs = round(self.duration *  frame_num / float(self.nframes))
        return self._secs_to_hms(secs)
