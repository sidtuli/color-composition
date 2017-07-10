from PIL import Image
import os, json


def get_color(file_path) :
    im = Image.open(file_path,'r').copy()
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    
    result = im.getcolors(maxcolors=len(im.getdata()))
    im.close
    return result

def restackimage(original_img):
    im = Image.open(original_img,'r').copy()
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    pixellist = list(im.getdata())
    newpixels = list()
    for pixel in reversed(sorted(pixellist)):
        newpixels.append(pixel)

    restack = Image.new(im.mode,im.size)
    restack.putdata(newpixels)
    restack.save(original_img+"_restacked.png")
    
def process_dict(dir_path) :
    
    file = open("test.json","w")
    data = {}
    for filename in os.listdir(os.getcwd()+dir_path):
        file_path = os.getcwd()+dir_path+"/"+filename
        data[filename] = get_color(file_path)
        
        
        
    json.dump(data,file)
    file.close()
        


#process_dict("/test_images")
restackimage(os.getcwd()+"/test_images/stop_thief.png")

