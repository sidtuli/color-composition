from PIL import Image
import os, json


def get_color(file_path) :
    im = Image.open(file_path,'r')
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    
    return im.getcolors(maxcolors=len(im.getdata()))

def process_dict(dir_path) :
    
    file = open("test.json","w")
    data = {}
    for filename in os.listdir(os.getcwd()+dir_path):
        file_path = os.getcwd()+dir_path+"/"+filename
        data[filename] = get_color(file_path)
        
        
        
    json.dump(data,file)
    file.close()
        


process_dict("/test_images")

