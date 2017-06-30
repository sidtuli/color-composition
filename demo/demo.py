from PIL import Image
import os


def get_color(file_path) :
    im = Image.open(file_path,'r')
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    pixel_values = list(im.getdata())

    color_dict = {}
    for color in pixel_values:
        if color in color_dict:
            color_dict[color] += 1
        else :
            color_dict[color] = 1
    color_dict_str = ""
    for (color, count) in color_dict.items():
        color_dict_str += str(color) + " - " + str(count) +","
    #print(im.mode)  
    #print(color_dict,"\n")
    return color_dict_str

def process_dict(dir_path) :
    #print(os.listdir(os.getcwd()+dir_path))
    file = open("test.txt","w") 
    for filename in os.listdir(os.getcwd()+dir_path):
        file_path = os.getcwd()+dir_path+"/"+filename
        res = get_color(file_path)
        file.write(filename + " - ")
        file.write(res)
        file.write('\n')

    file.close()
        

#get_color("test_image.svg")
process_dict("/flags-normal")
