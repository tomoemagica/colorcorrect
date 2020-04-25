from PIL import Image
import colorcorrect.algorithm as cca
from colorcorrect.util import from_pil, to_pil

img = Image.open('demo.jpg')
# img = to_pil(cca.stretch(cca.gray_world(from_pil(img))))
img = to_pil(cca.automatic_color_equalization(from_pil(img)))
img.save("result.jpg", quality=100)
