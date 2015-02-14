from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from frame import get_frame
import settings

# inintialize document settings
margin_horiz = settings.margin_horiz * inch
margin_vert = settings.margin_vert * inch
font = settings.font
fontSize = settings.fontSize

cursor = 0

def pdf_init(video):
    """ Initialize and return pdf canvas for video. """
    fn = video.readable_id + ".pdf"
    c = canvas.Canvas(fn, pagesize=letter)
    set_font(c)
    reset_cursor(c)
    return c

def set_font(canvas):
    """ Set font and fontSize from settings. """
    canvas.setFont(font, fontSize, leading = fontSize)

def reset_cursor(canvas):
    """ Reset canvas cursor to top left of page. """
    global cursor

    _, height = letter
    canvas.translate(margin_horiz, height - margin_vert)
    cursor = 0

def new_page(canvas):
    """ Move canvas to next page and reset cursor. """
    canvas.showPage()
    set_font(canvas)
    reset_cursor(canvas)

def write_string(canvas, string):
    global cursor 
    canvas.drawString(0, cursor, string)
    cursor -= fontSize

def write_header(canvas, video):
    format_field = lambda field, val: "{0}: {1}".format(field, val)

    # metadata fields to write 
    title = format_field("Title", video.title)
    desc = format_field("Description", video.description)
    dur = format_field("Duration", video.get_duration())

    # write to canvas
    write_string(canvas, title)
    write_string(canvas, desc)
    write_string(canvas, dur)

def write_frame(canvas, video, frame_ndx):
    """ Write frame at index frame_ndx to canvas. """
    global cursor
    
    # write time of frame in video
    write_string(canvas, "")
    write_string(canvas, video.get_frame_time(frame_ndx))

    frame = get_frame(frame_ndx, bw=True)

    # convert array to PIL Image and add border
    image = Image.fromarray(frame)
    image = ImageOps.expand(image, border=1, fill='black')
    f_width, f_height = image.size
    ratio = float(f_width) / f_height

    # calculate scaling dimensions for full page width 
    pg_width, _ = letter
    img_width = pg_width - 2 * margin_horiz
    img_height = img_width / ratio 

    # write image to canvas
    cursor -= img_height
    canvas.drawInlineImage(image, 0, cursor, img_width, img_height)
    write_string(canvas, "")

def create_pdf(video, frame_ndxs):
    """ Create video with frames at each index in frame_ndxs. """
    print "Creating output PDF..."

    canvas = pdf_init(video)
    write_header(canvas, video)
    write_string(canvas, "")

    # write two frames per page
    for i in xrange(0, len(frame_ndxs), 2):
        if not i is 0 and i % 2 is 0:
            new_page(canvas)
        write_frame(canvas, video, frame_ndxs[i])
        if not i + 1 is len(frame_ndxs):
            write_frame(canvas, video, frame_ndxs[i + 1])
    canvas.save()
