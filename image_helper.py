''' Helper functions for interacting with light field images. '''

import numpy

from PIL import Image

def demosaic(raw_image, kernel_width, kernel_height):
    '''
    Demosaics the provided raw image. Demosaicing means that it
    breaks the raw image down into its component sub-images.

    @param raw_image Image to be demosaiced
    @paramType PIL.Image
    @param kernel_width # lenslets in a row aka angular resolution along the X-axis ;)
    @paramType int
    @param kernel_height # lenslets in a column aka angular resolution along the Y-axis ;)
    @paramType in
    @returns list of sub-images created by demosaicing the raw image
    @returnType list of PIL.Image
    '''
    assert raw_image is not None
    assert kernel_width > 0, kernel_width
    assert kernel_height > 0, kernel_height
    
    print "Loading raw image data..."
    sub_images     = []
    raw_image_data = raw_image.getdata()

    print "Calculating the dimensions of the sub-images..."
    (raw_image_width, raw_image_height) = raw_image.size
    sub_image_width  = raw_image_width / kernel_width
    sub_image_height = raw_image_height / kernel_height

    print "Raw Image Format: %s" % raw_image.format
    print "Raw Image Size:   (%s, %s)" % raw_image.size
    print "Sub Image Size:   (%s, %s)" % (sub_image_width, sub_image_height)

    # For each lenslet column
    for lenslet_x_iter in range(kernel_width):
        print "Demosaicing sub-image %s/%s..." % (lenslet_x_iter * kernel_width, kernel_width * kernel_height)

        # For each lenslet in the column
        for lenslet_y_iter in range(kernel_height):
       
            sub_image_data = []
 
            for y_iter in range(sub_image_height):
 
                y_pos = lenslet_y_iter + y_iter * kernel_height
            
                for x_iter in range(sub_image_width):
       
                    x_pos = lenslet_x_iter + x_iter * kernel_width
                   
                    if y_pos >= raw_image_height or x_pos >= raw_image_width:
                        #print "Past bounds!"
                        continue
 
                    #print "Sampling at (%s, %s) = pixel %s..." % (x_pos, y_pos, y_pos * raw_image_width + x_pos)
                    sub_image_data.append(raw_image_data[y_pos * raw_image_width + x_pos])

            sub_image = Image.new("RGB", (sub_image_width, sub_image_height))
            sub_image.putdata(sub_image_data)
            sub_images.append(sub_image)

    return sub_images

def demosaic_1(raw_image, kernel_width, kernel_height):
    '''
    Demosaics the provided raw image. Demosaicing means that it
    breaks the raw image down into its component sub-images.

    @param raw_image Image to be demosaiced
    @paramType PIL.Image
    @param kernel_width # lenslets in a row aka angular resolution along the X-axis ;)
    @paramType int
    @param kernel_height # lenslets in a column aka angular resolution along the Y-axis ;)
    @paramType in
    @returns list of sub-images created by demosaicing the raw image
    @returnType list of PIL.Image
    '''
    assert raw_image is not None
    assert kernel_width > 0, kernel_width
    assert kernel_height > 0, kernel_height

    sub_images = []

    print "Calculating the dimensions of the sub-images..."
    (raw_image_width, raw_image_height) = raw_image.size
    sub_image_width  = raw_image_width / kernel_width
    sub_image_height = raw_image_height / kernel_height

    print "Raw Image Format: %s" % raw_image.format
    print "Raw Image Size:   (%s, %s)" % raw_image.size
    print "Sub Image Size:   (%s, %s)" % (sub_image_width, sub_image_height)

    # For each lenslet column
    for x_iter in range(kernel_width):

        # Calculate the left and right boundaries of the sub-image
        left = x_iter * sub_image_width
        right = left + sub_image_width

        # For each lenslet in the column
        for y_iter in range(kernel_height):
        
            # Calculate the top and bottom boundaries of the sub-image
            top    = y_iter * sub_image_height
            bottom = top + sub_image_height

            print "Extracting the sub-image..."
            print "Sub-Image Bounds: (%s, %s) (%s, %s)" % (left, bottom, right, top)
            sub_image = raw_image.crop((left, top, right, bottom))
            sub_images.append(sub_image)

    return sub_images
