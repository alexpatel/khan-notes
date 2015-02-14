import json
import urllib2 
import urlparse

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
