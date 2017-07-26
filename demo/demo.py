from PIL import Image
import os, json


def getcolor(img_path):
    '''
    A method to return color info on an image
    '''
    # Obtain a copy of the image given
    im = Image.open(img_path,'r').copy()
    # Assure that the copy is in RGBA mode to read color values
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    # Get colors from image to return and then close image pointer
    result = im.getcolors(maxcolors=len(im.getdata()))
    im.close()
    return result

def getcolorgif(img_path):
    '''
    Method to obtain color info on the frames of a gif
    '''
    im = Image.open(img_path,"r")
    frames = []
    try:
        while True:
            print("Saving frame #"+str(im.tell()+1)+" of file: " + str(img_path))
            # Take frame number and then save a  copy of the current frame
            frame_num = im.tell()
            curr_frame = im.copy()
            # Then we save the frame as a png while converting it to RGBA mode
            curr_frame = curr_frame.convert("RGBA")
            frames.append(curr_frame.getcolors(maxcolors=len(curr_frame.getdata())))
            curr_frame.close()
            # Then move the image ahead one frame
            im.seek(im.tell()+1)
    except EOFError:
        print("End of Frames")
        pass
    return frames

def stackbyrgba(img_path):
    '''
    Takes an image and then spits out an image with all the rgb values sorted horizontally
    '''
    # Read copy of image and convert it intoRGBA mode
    im = Image.open(img_path,'r').copy()
    
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    # Get pixels of original image and then iterate them as "sorted" by sum of rgba values
    pixellist = list(im.getdata())
    pixellist.sort(key = lambda pixel:pixel[0]+pixel[1]+pixel[2]+pixel[3])
    
    # Make a new image with specifications of old and then put in new list of "sorted" pixels
    restack = Image.new(im.mode,im.size)

    im.close()
    
    restack.putdata(pixellist)
    restack.save(img_path+"[rgba_stacked].png")
    restack.close()

    
def stackbyfrequency(original_img):
    '''
    Takes an image and then spits out an image with all the rgb values sorted horizontally by frequency
    '''
    # Open an image copy and then convert it to RGBA mode
    im = Image.open(original_img,'r').copy()
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    # Get a list of all colors used from original image
    colorlist = list(im.getcolors(maxcolors=len(im.getdata())))
    newpixels = list()
    # Then sort the pixels by their frequency count in the image for each color
    for color in sorted(colorlist, key = lambda color: color[0]):
        newpixels += [color[1]] * color[0]

    # Create a new image with olg image designs and new list of pixels
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
    im.close()

def stackbyrgbagif(img_path):
    '''
    Restack each image in a gif by rgba value and then make a new gif from those images
    '''
    # We do not use copy here as it would only copy the first frame of the gif
    im = Image.open(img_path,'r')
    # Create gif image object
    new_gif = Image.new("RGBA",im.size)
    # Copy first frame from image
    first_frame = im.copy()
    first_frame = first_frame.convert("RGBA")
    # Sort pixels of first frame
    pixellist = list(first_frame.getdata())
    pixellist.sort(key = lambda pixel:pixel[0]+pixel[1]+pixel[2]+pixel[3])
    # Create object for new first frame of the gif
    new_first_frame = Image.new("RGBA",im.size)
    new_first_frame.putdata(pixellist)
    # Then this new frame is put into the gif image object
    new_gif.paste(new_first_frame,(0,0),new_first_frame.convert("RGBA"))
    new_frames = []
    try:
        while True:
            print("Saving frame #"+str(im.tell()+1)+" of file: " + str(img_path))
            # save a  copy of the current frame
            im.seek(im.tell()+1)
            curr_frame = im.copy()
            # Sort the frame's pixels
            curr_frame = curr_frame.convert('RGBA')
            pixellist = list(curr_frame.getdata())
            pixellist.sort(key = lambda pixel:pixel[0]+pixel[1]+pixel[2]+pixel[3])
            restack = Image.new("RGBA",curr_frame.size)
            restack.putdata(pixellist)
            new_frames.append(restack)
            # Then move the image ahead one frame
            
    except EOFError:
        print("End of Frames")
        pass
    #new_gif = Image.new("RGBA",im.size)
    
    new_gif.save(img_path+"[rgba_restack].gif",save_all=True, append_images=new_frames)
    new_gif.close()
    im.close()

def is_multi_frame(img_path):
    '''
    A function to tell whether or not an image is animated
    '''
    im = Image.open(img_path,'r')
    test = (hasattr(im,"is_animated") and im.is_animated) or (hasattr(im,"n_frames") and im.n_frames > 1)
    im.close()
    return test
    
    
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
#stackbyrgba(os.getcwd()+"/test_images/Sør-Trøndelag.png")
#extract_frames(os.getcwd()+"/test_images/dark_souls.gif")
#stackbyrgbagif(os.getcwd()+"/test_images/dark_souls.gif")
#extract_frames(os.getcwd()+"/test_images/dark_souls.gif[rgba_restack].gif")
print(getcolorgif(os.getcwd()+"/test_images/dark_souls.gif"))
