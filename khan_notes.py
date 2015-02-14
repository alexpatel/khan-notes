import optparse 

from video import Video

def parse_arg_list(argv):
    """
    Parse user-supplied command-line arguments.
    Returns an options object of valid options with supplied values. 
    """
    parser = optparse.OptionParser()
 
    # define program options
    parser.add_option("-u", "--url", type="string", dest="url", 
            help="Video URL")

    (options, args) = parser.parse_args()

    # error upon extraneous options having been provided
    if args:
        raise Exception("Command line input not understood: ", args)

    return options

def main():
    # get options from command-line arguments
    options = parse_arg_list(sys.argv[1:])

    video_url = options.url

    video = Video(video_url)
    video.get_metadata()
    video.download()

if __name__ == "__main__":
    main()
