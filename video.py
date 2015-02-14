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
