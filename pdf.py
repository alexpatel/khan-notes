import os

from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from frame import get_frame
import settings

class PDF:
    def __init__(self, video, output_fn):
        self.video = video

        # document settings from global settings
        self.margin_horiz = settings.margin_horiz * inch
        self.margin_vert = settings.margin_vert * inch
        self.font = settings.font
        self.fontSize = settings.fontSize

        # use US Letter paper size
        self.width, self.height = letter

        # y position of cursor on canvas
        self.cursor = 0

        # initialize pdf and write video metadata 
        self._set_pdf_path(output_fn)
        self._canvas_init()

        self._write_header()
        self.write_string("")

    def _set_pdf_path(self, fn):
        """ Set name for output PDF file. """
        # make pdf_dir if it doesn't exist
        try:
            os.mkdir(settings.pdf_dir)
        except Exception:
            pass
        if not fn:
            fn = self.video.readable_id + ".pdf"

        self.pdf_path = os.path.join(settings.pdf_dir, fn)

    def _canvas_init(self):
        """ Initialize and return pdf canvas for video. """
        c = canvas.Canvas(self.pdf_path, pagesize=letter)
        self.canvas = c 
        self._set_font()
        self._reset_cursor()

    def _set_font(self):
        """ Set font and fontSize from settings. """
        self.canvas.setFont(self.font, self.fontSize, leading = self.fontSize)

    def _reset_cursor(self):
        """ Reset canvas cursor to top left of page. """
        self.canvas.translate(self.margin_horiz, self.height - self.margin_vert)
        self.cursor = 0

    def _new_page(self):
        """ Move canvas to next page and reset cursor. """
        self.canvas.showPage()
        self._set_font()
        self._reset_cursor()

    def write_string(self, string):
        """ Write a string to current page in PDF. """
        self.canvas.drawString(0, self.cursor, string)
        self.cursor -= self.fontSize

    def _write_header(self):
        """ Write video metadata to PDF. """
        format_field = lambda field, val: "{0}: {1}".format(field, val)

        video = self.video

        # metadata fields to write 
        title = format_field("Title", video.title)
        desc = format_field("Description", video.description)
        dur = format_field("Duration", video.get_duration())

        # write to canvas
        self.write_string(title)
        self.write_string(desc)
        self.write_string(dur)

    def _write_frame(self, video, frame_ndx):
        """ Write frame at index frame_ndx to canvas. """
        # write time of frame in video
        self.write_string("")
        self.write_string(video.get_frame_time(frame_ndx))

        frame = get_frame(frame_ndx, bw=True)

        # convert array to PIL Image and add border
        image = Image.fromarray(frame)
        image = ImageOps.expand(image, border=1, fill='black')
        f_width, f_height = image.size
        ratio = float(f_width) / f_height

        # calculate scaling dimensions for full page width 
        img_width = self.width - 2 * self.margin_horiz
        img_height = img_width / ratio 

        # write image to canvas
        self.cursor -= img_height
        self.canvas.drawInlineImage(image, 0, self.cursor, img_width, img_height)
        self.write_string("")

    def write(self, frame_ndxs):
        """ Create video with frames at each index in frame_ndxs. """
        print "Writing frames to PDF..."
        # write two frames per page
        for i in xrange(0, len(frame_ndxs), 2):
            if not i is 0 and i % 2 is 0:
                self._new_page()
            self._write_frame(self.video, frame_ndxs[i])
            if not i + 1 is len(frame_ndxs):
                self._write_frame(self.video, frame_ndxs[i + 1])
        self.canvas.save()
