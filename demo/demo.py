from PIL import Image
import os


def get_color(file_path) :
    im = Image.open(file_path,'r')
    if im.mode != "RGB":
        im = im.convert('RGB')
    pixel_values = list(im.getdata())

    color_dict = {}
    for color in pixel_values:
        if color in color_dict:
            color_dict[color] += 1
        else :
            color_dict[color] = 1
    
    print(im.mode)  
    print(color_dict,"\n")

def process_dict(dir_path) :
    print(os.listdir(os.getcwd()+dir_path))
    for filename in os.listdir(os.getcwd()+dir_path):
        file_path = os.getcwd()+dir_path+"/"+filename
        get_color(file_path)
        

#get_color("test_image.svg")
process_dict("/flags-normal")
