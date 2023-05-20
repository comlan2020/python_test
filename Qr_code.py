# install pyqrcode and pypng
import pyqrcode
import png
from pyqrcode import QRCode

# Text which is to be converted to QR code
text_to_convert=input("Enter text to convert: ")
# Name of QR code png file
image_name=input("Enter image name to save: ")
# Adding extension as .pnf
file_name=image_name+".png"
# Creating QR code
url=pyqrcode.create(text_to_convert)
# Saving QR code as  a png file
url.show()
url.png(file_name, scale =6)
