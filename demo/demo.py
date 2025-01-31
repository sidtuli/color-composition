from PIL import Image
import os, json, random

# **********************************************************************************************************************
#                                       **** Functions to process files and directories ****
# **********************************************************************************************************************

def process_dict(dir_path) :
    '''
    Goes through an entire directory to output a data file of all files within them
    '''
    json_file = open("test.json","w")
    data = {}
    files = os.listdir(os.getcwd()+dir_path)
    stuff = os.walk(os.getcwd()+dir_path)
    i = 0
    file_paths = []
    for root, dirs, files in stuff:
        data_prepend = root.split(os.sep)[-1]
        file_paths = file_paths + [(root+"/"+file,data_prepend+"/"+file) for file in files]
    
    for file_path in file_paths:
        data_name = file_path[1]
        data[data_name] = process_file(file_path[0])
    
    
    json.dump(data,json_file)
    json_file.close()

def process_file(file_path):
    '''
    Function to determine what is done with a specified file
    '''
    if can_open_image(file_path):
        if is_multi_frame(file_path):
            return getcolorgif(file_path)
        else:
            return getcolor(file_path)
    else:
        return "null"

# **********************************************************************************************************************
#                   **** Utility functions - checking properties of files and other useful methods ****
# **********************************************************************************************************************

def can_open_image(img_path):
    '''
    A function to check if file can be opened by PIL library
    '''
    try:
        im = Image.open(img_path)
        im.close()
        return True
    except OSError:
        print("Error opening file:" + img_path)
        return False

def is_multi_frame(img_path):
    '''
    A function to tell whether or not an image is animated
    '''
    im = Image.open(img_path,'r')
    test = (hasattr(im,"is_animated") and im.is_animated) or (hasattr(im,"n_frames") and im.n_frames > 1)
    im.close()
    return test

def extract_frames(img_path):
    '''
    A method to extract each frame of a gif into separate images
    '''
    # We do not use copy here as it would only copy the first frame of the gif
    im = Image.open(img_path,'r')
    print(im.info)
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

def handle_gif_info(img_info,n_frames):
    result_info = {}
    
    result_info["background"] = img_info["background"] if "duration" in img_info else 0
    result_info["transparency"] = img_info["transparency"] if "transparency" in img_info else 0
    result_info["duration"] = img_info["duration"] if "duration" in img_info else (10 * n_frames)
    result_info["loop"] = img_info["loop"] if "loop" in img_info else 0
    
    return result_info
    
def pixels_into_rows(pixels,width,height):
    rows = []
    for i in range(height):
        rows.append(pixels[i*width:(i+1)*width])
    return rows

def pixels_into_cols(pixels,width,height):
    rows = []
    for i in range(height):
        rows.append(pixels[i*width:(i+1)*width])
    cols = []
    for i in range(0,width):
        cols.append([row[i] for row in rows])
        
    return cols
# **********************************************************************************************************************
#                                       **** Functions to process colors for files ****
# **********************************************************************************************************************

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

# **********************************************************************************************************************
#                       **** Functions to "restack" images by sorting the pixels by rgba values ****
# **********************************************************************************************************************

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
            print("RGBA Stacking frame #"+str(im.tell()+1)+" of file: " + str(img_path))
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
    print(im.info)
    new_gif_info = handle_gif_info(im.info,im.n_frames)
    new_gif.save(img_path+"[rgba_restack].gif",save_all=True, append_images=new_frames, duration=new_gif_info["duration"], loop=new_gif_info["loop"], background=new_gif_info["background"])
    new_gif.close()
    im.close()

# **********************************************************************************************************************
#           **** Functions to "restack" images by sorting the pixels by frequency of rgba values ****
# **********************************************************************************************************************

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

def stackbyfrequencygif(img_path):
    '''
    Takes a gif and spits out a gif with every frame resorted by frequency of colors
    '''
    # We do not use copy here as it would only copy the first frame of the gif
    im = Image.open(img_path,'r')
    # Create gif image object
    new_gif = Image.new("RGBA",im.size)
    # Copy first frame from image
    first_frame = im.copy()
    first_frame = first_frame.convert("RGBA")
    # Sort pixels of first frame
    colorlist = list(first_frame.getcolors(maxcolors=len(first_frame.getdata())))
    newpixels = list()

    for color in sorted(colorlist, key = lambda color: color[0]):
        newpixels += [color[1]] * color[0]
    
    # Create object for new first frame of the gif
    new_first_frame = Image.new("RGBA",im.size)
    new_first_frame.putdata(newpixels)
    # Then this new frame is put into the gif image object
    new_gif.paste(new_first_frame,(0,0),new_first_frame.convert("RGBA"))
    new_frames = []
    try:
        while True:
            print("Frequency stacking frame #"+str(im.tell()+1)+" of file: " + str(img_path))
            # save a  copy of the current frame
            im.seek(im.tell()+1)
            curr_frame = im.copy()
            # Sort the frame's pixels
            curr_frame = curr_frame.convert('RGBA')
            
            colorlist = list(curr_frame.getcolors(maxcolors=len(curr_frame.getdata())))
            newpixels = list()

            for color in sorted(colorlist, key = lambda color: color[0]):
                newpixels += [color[1]] * color[0]
            restack = Image.new("RGBA",curr_frame.size)
            restack.putdata(newpixels)
            new_frames.append(restack)
            # Then move the image ahead one frame
            
    except EOFError:
        print("End of Frames")
        pass
    
    new_gif_info = handle_gif_info(im.info,im.n_frames)
    new_gif.save(img_path+"[freq_restack].gif",save_all=True, append_images=new_frames, duration=new_gif_info["duration"], loop=new_gif_info["loop"], background=new_gif_info["background"])
    new_gif.close()
    im.close()

# **********************************************************************************************************************
#                                       **** Functions to randomize pixels in images ****
# **********************************************************************************************************************
def randomizepixels(img_path):
    '''
    Takes an image and randomizes its pixels
    '''
    im = Image.open(img_path,'r').copy()
    
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    
    pixellist = list(im.getdata())

    random.shuffle(pixellist)

    rand_result = Image.new(im.mode,im.size)

    im.close()
    
    rand_result.putdata(pixellist)
    rand_result.save(img_path+"[random].png")
    rand_result.close()

def randomizepixelsgif(img_path):
    # We do not use copy here as it would only copy the first frame of the gif
    im = Image.open(img_path,'r')
    # Create gif image object
    new_gif = Image.new("RGBA",im.size)
    # Copy first frame from image
    first_frame = im.copy()
    first_frame = first_frame.convert("RGBA")
    # Sort pixels of first frame
    newpixels = list(first_frame.getdata())

    random.shuffle(newpixels)
    
    # Create object for new first frame of the gif
    new_first_frame = Image.new("RGBA",im.size)
    new_first_frame.putdata(newpixels)
    # Then this new frame is put into the gif image object
    new_gif.paste(new_first_frame,(0,0),new_first_frame.convert("RGBA"))
    new_frames = []
    try:
        while True:
            print("Randomizing frame #"+str(im.tell()+1)+" of file: " + str(img_path))
            # save a  copy of the current frame
            im.seek(im.tell()+1)
            curr_frame = im.copy()
            # Sort the frame's pixels
            curr_frame = curr_frame.convert('RGBA')
            newpixels = list(curr_frame.getdata())
            random.shuffle(newpixels)

            restack = Image.new("RGBA",curr_frame.size)
            restack.putdata(newpixels)
            new_frames.append(restack)
            # Then move the image ahead one frame
            
    except EOFError:
        print("End of Frames")
        pass
    
    new_gif_info = handle_gif_info(im.info,im.n_frames)
    new_gif.save(img_path+"[random].gif",save_all=True, append_images=new_frames, duration=new_gif_info["duration"], loop=new_gif_info["loop"], background=new_gif_info["background"])
    new_gif.close()
    im.close()

def partialrandomizepixels(img_path,proportion):
    '''
    Function to randomize a part of an image's pixels
    '''
    im = Image.open(img_path,'r').copy()
    
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    
    pixellist = list(im.getdata())

    pixel_num = len(pixellist)
    pixel_count = 0
    rand_dict = {}
    pixel_barrier = pixel_num * proportion
    rand_arr = []
    while pixel_count < pixel_barrier:
        curr = random.randint(0,pixel_num - 1)
        if curr not in rand_dict:
            rand_dict[curr] = -1
            pixel_count += 1
            rand_arr.append(curr)
    random.shuffle(rand_arr)
    i = 0
    for key in rand_dict:
        rand_dict[key] = rand_arr[i]
        temp = pixellist[key]
        pixellist[key] = pixellist[rand_arr[i]]
        pixellist[rand_arr[i]] = temp
        i += 1
    
    rand_result = Image.new(im.mode,im.size)

    im.close()
    
    rand_result.putdata(pixellist)
    rand_result.save(img_path+"[part-random].png")
    rand_result.close()

def partialrandomizepixelsgif(img_path,proportion):
    # We do not use copy here as it would only copy the first frame of the gif
    im = Image.open(img_path,'r')
    # Create gif image object
    new_gif = Image.new("RGBA",im.size)
    # Copy first frame from image
    first_frame = im.copy()
    first_frame = first_frame.convert("RGBA")
    # Sort pixels of first frame
    pixellist = list(first_frame.getdata())
    
    pixel_num = len(pixellist)
    pixel_count = 0
    rand_dict = {}
    pixel_barrier = pixel_num * proportion
    rand_arr = []
    while pixel_count < pixel_barrier:
        curr = random.randint(0,pixel_num - 1)
        if curr not in rand_dict:
            rand_dict[curr] = -1
            pixel_count += 1
            rand_arr.append(curr)
    random.shuffle(rand_arr)
    i = 0
    for key in rand_dict:
        rand_dict[key] = rand_arr[i]
        temp = pixellist[key]
        pixellist[key] = pixellist[rand_arr[i]]
        pixellist[rand_arr[i]] = temp
        i += 1
    
    # Create object for new first frame of the gif
    new_first_frame = Image.new("RGBA",im.size)
    new_first_frame.putdata(pixellist)
    # Then this new frame is put into the gif image object
    new_gif.paste(new_first_frame,(0,0),new_first_frame.convert("RGBA"))
    new_frames = []
    try:
        while True:
            print("Randomizing frame #"+str(im.tell()+1)+" of file: " + str(img_path))
            # save a  copy of the current frame
            im.seek(im.tell()+1)
            curr_frame = im.copy()
            # Sort the frame's pixels
            curr_frame = curr_frame.convert('RGBA')
            
            pixellist = list(curr_frame.getdata())
    
            pixel_num = len(pixellist)
            pixel_count = 0
            rand_dict = {}
            pixel_barrier = pixel_num * proportion
            rand_arr = []
            while pixel_count < pixel_barrier:
                curr = random.randint(0,pixel_num - 1)
                if curr not in rand_dict:
                    rand_dict[curr] = -1
                    pixel_count += 1
                    rand_arr.append(curr)
            random.shuffle(rand_arr)
            i = 0
            for key in rand_dict:
                rand_dict[key] = rand_arr[i]
                temp = pixellist[key]
                pixellist[key] = pixellist[rand_arr[i]]
                pixellist[rand_arr[i]] = temp
                i += 1
            restack = Image.new("RGBA",curr_frame.size)
            restack.putdata(pixellist)
            new_frames.append(restack)
            # Then move the image ahead one frame
            
    except EOFError:
        print("End of Frames")
        pass
    
    new_gif_info = handle_gif_info(im.info,im.n_frames)
    new_gif.save(img_path+"[part-random].gif",save_all=True, append_images=new_frames, duration=new_gif_info["duration"], loop=new_gif_info["loop"], background=new_gif_info["background"])
    new_gif.close()
    im.close()

# **********************************************************************************************************************
#                                                       **** Tests ****
# **********************************************************************************************************************
#partialrandomizepixelsgif(os.getcwd()+"/test_images/dark_souls.gif",0.5)
#partialrandomizepixels(os.getcwd()+"/test_images/Sør-Trøndelag.png",.5)
#randomizepixelsgif(os.getcwd()+"/test_images/dark_souls.gif")
#extract_frames(os.getcwd()+"/test_images/dark_souls.gif[random].gif")
#randomizepixels(os.getcwd()+"/test_images/Sør-Trøndelag.png")
#stackbyfrequency(os.getcwd()+"/test_images/Sør-Trøndelag.png")
#process_dict("/test_images")
#stackbyrgba(os.getcwd()+"/test_images/Sør-Trøndelag.png")
#extract_frames(os.getcwd()+"/test_images/dark_souls.gif")
#stackbyrgbagif(os.getcwd()+"/test_images/spinning_cubes.gif")
#stackbyfrequencygif(os.getcwd()+"/test_images/spinning_cubes.gif")
#extract_frames(os.getcwd()+"/test_images/spinning_cubes.gif[freq_restack].gif")
#extract_frames(os.getcwd()+"/test_images/dark_souls.gif[rgba_restack].gif")
#can_open_image(os.getcwd()+"/test_images/not2.svg")
