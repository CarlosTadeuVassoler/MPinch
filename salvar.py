from PIL import Image

img = Image.open('duck.eps')
fig = img.convert('RGBA')
fig.save('imagiii.png', lossless = True)
