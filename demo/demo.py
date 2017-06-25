from PIL import Image
im = Image.open('test_image.svg','r')
width, height = im.size
pixel_values = list(im.getdata())

color_dict = {}
for color in pixel_values:
    if color in color_dict:
        color_dict[color] += 1
    else :
        color_dict[color] = 1

print(color_dict)
