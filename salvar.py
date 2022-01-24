from PIL import Image

img = Image.open("duck.eps")
rgb_img = img.convert("RGB")
rgb_img.save('image.png')
