#!/usr/bin/python

import sys

from PIL import Image

from image_helper import demosaic, demosaic_1

def test(raw_image_file, kernel_width, kernel_height):
    '''
    Tests some stuff!
    '''
    print "Raw Image File:        %s" % raw_image_file
    print "Raw Image Kernel Size: (%s, %s)" % (kernel_width, kernel_height)

    print "Loading the raw image we want to play with..."
    raw_image = Image.open(raw_image_file)

    print "Breaking the raw image down into its component sub-images..."
    sub_images = demosaic_1(raw_image, kernel_width, kernel_height)
    #sub_images = demosaic(raw_image, kernel_width, kernel_height)    

    print "Saving the sub-images..."
    for sub_image_iter in range(len(sub_images)):
        
        sub_image = sub_images[sub_image_iter]
        sub_image.save(str(sub_image_iter) + '_' + raw_image_file)

    print "Constructing tiled master image..."
    master_image = Image.new("RGB", raw_image.size)
    for x_iter in range(kernel_width):
        print "Pasting %s/%s..." % (x_iter * kernel_height, kernel_width * kernel_height)        

        for y_iter in range(kernel_height):
            width, height = sub_images[0].size

            master_image.paste(sub_images[y_iter * kernel_width + x_iter], (x_iter * width, y_iter * height))
            master_image.save("master_image.jpg")

if __name__ == '__main__':

    # Inspect the command line arguments
    if len(sys.argv) != 4:

        print "Usage: test.py [raw_image_file] [kernel_width] [kernel_height]"
        sys.exit()

    test(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
