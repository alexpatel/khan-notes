from PIL import Image, ImageOps
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

