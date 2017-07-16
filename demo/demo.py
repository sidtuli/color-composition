from PIL import Image
import os, json


def getcolor(file_path) :
    '''
    A method toreturn color info on an image
    '''
    im = Image.open(file_path,'r').copy()
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    
    result = im.getcolors(maxcolors=len(im.getdata()))
    im.close()
    return result

def stackbyrgba(original_img):
    '''
    Takes an image and then spits out an image with all the rgb values sorted horizontally
    '''
    im = Image.open(original_img,'r').copy()
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    pixellist = list(im.getdata())
    newpixels = list()
    for pixel in sorted(pixellist,key = lambda pixel:pixel[0]+pixel[1]+pixel[2]+pixel[3]):
        newpixels.append(pixel)

    
    restack = Image.new(im.mode,im.size)

    im.close()
    
    restack.putdata(newpixels)
    restack.save(original_img+"[rgba_stacked].png")
    restack.close()

    
def stackbyfrequency(original_img):
    '''
    Takes an image and then spits out an image with all the rgb values sorted horizontally by frequency
    '''
    im = Image.open(original_img,'r').copy()
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    colorlist = list(im.getcolors(maxcolors=len(im.getdata())))
    newpixels = list()
    for color in sorted(colorlist, key = lambda color: color[0]):
        newpixels += [color[1]] * color[0]
    
    restack = Image.new(im.mode,im.size)

    im.close()
    
    restack.putdata(newpixels)
    restack.save(original_img+"[freq_stacked].png")

    restack.close()
    

def extract_frames(img_path):
    '''
    A method to extract each frame of a gif into separate images
    '''
    # We do not use copy here as it would only copy the first frame of the gif
    im = Image.open(img_path,'r')
    
    try:
        while True:
            print("Saving frame #"+str(im.tell()+1)+" of file: " + str(img_path))
            # Take frame number and then save a  copy of the current frame
            frame_num = im.tell()
            curr_frame = im.copy()
            # Then we save the frame as a png while converting it to RGBA mode
            frame_export = Image.new("RGBA",curr_frame.size)
            frame_export.paste(curr_frame, (0,0), curr_frame.convert("RGBA"))
            frame_export.save(img_path+"[frame #"+str(frame_num+1)+"].png")
            frame_export.close()
            # Then move the image ahead one frame
            im.seek(im.tell()+1)
    except EOFError:
        print("End of Frames")
        pass
    
def process_dict(dir_path) :
    '''
    Goes through an entire directory to output a data file of 
    '''
    file = open("test.json","w")
    data = {}
    for filename in os.listdir(os.getcwd()+dir_path):
        file_path = os.getcwd()+dir_path+"/"+filename
        data[filename] = getcolor(file_path)
        stackbyfrequency(file_path)
        stackbyrgba(file_path)
        
    json.dump(data,file)
    file.close()
        


#process_dict("/test_images/flags")
#stackbyrgb(os.getcwd()+"/test_images/Sør-Trøndelag.png")
extract_frames(os.getcwd()+"/test_images/dark_souls.gif")
