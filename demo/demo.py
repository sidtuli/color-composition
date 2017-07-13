from PIL import Image
import os, json


def getcolor(file_path) :
    im = Image.open(file_path,'r').copy()
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    
    result = im.getcolors(maxcolors=len(im.getdata()))
    im.close()
    return result

def stackbyrgb(original_img):
    im = Image.open(original_img,'r').copy()
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    pixellist = list(im.getdata())
    newpixels = list()
    for pixel in sorted(pixellist,key = lambda pixel:pixel[0]+pixel[1]+pixel[2]+pixel[3]):
        newpixels.append(pixel)

    restack = Image.new(im.mode,im.size)
    restack.putdata(newpixels)
    restack.save(original_img+"[rgb_stacked].png")
def stackbyfrequency(original_img):
    im = Image.open(original_img,'r').copy()
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    colorlist = list(im.getcolors(maxcolors=len(im.getdata())))
    newpixels = list()
    for color in sorted(colorlist, key = lambda color: color[0]):
        newpixels += [color[1]] * color[0]
    
    restack = Image.new(im.mode,im.size)
    restack.putdata(newpixels)
    restack.save(original_img+"[freq_stacked].png")
    
def process_dict(dir_path) :
    
    file = open("test.json","w")
    data = {}
    for filename in os.listdir(os.getcwd()+dir_path):
        file_path = os.getcwd()+dir_path+"/"+filename
        data[filename] = getcolor(file_path)
        stackbyfrequency(file_path)
        
        
    json.dump(data,file)
    file.close()
        


process_dict("/test_images/flags")
#stackbyrgb(os.getcwd()+"/test_images/Sør-Trøndelag.png")

