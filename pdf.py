from
PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from frame import get_frame
import settings

# inintialize document settings
margin_horiz = settings.margin_horiz
margin_vert = settings.margin_vert
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
    canvas.setFont(font, fontSize, leading = fontSize)

def reset_cursor(canvas):
    """ Reset canvas cursor to top left of page. """
    global cursor

    _, height = letter
    canvas.translate(margin_horiz, height - margin_vert)
    cursor = 0

def new_page(canvas):
    """ Move canvas to next page and reset cursor. """
    global cursor 
    canvas.showPage()
    set_font(canvas)
    reset_cursor(canvas)

def write_string(canvas, string):
    canvas.drawString(0, cursor, string)
    cursor -= fontSize

def write_header(canvas, video):
    format_field = lambda field, val: "{0}: {1}".format(field, val)

    title = format_field("Title", video.title)
    desc = format_field("Description", video.description)
    dur = format_field("Duration", video.get_duration())

