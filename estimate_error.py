#!/usr/bin/python

import logging
import math
import random
import sys

def estimate_error(angular_resolution, depth, noise):
    '''
    Estimates the depth estimate's error as a function of angular resolution, depth, and noise.

    @param angular_resolution Angle between the representative pixels on the image plane in radians
    @paramType float
    @param depth Distance of the source pixel from the image plane in meters
    @paramType float
    @param noise Worst-case error in the distance between the representative pixels on the image plane in meters
    @paramType float
    @returns Depth estimate error
    @returnType float
    '''
    # Calculate the initial pixel positions given the angular resolution
    pixel0 = -math.tan(angular_resolution) * depth
    pixel1 = 0

    # Add noise in the lenslet position to the pixel positions
    pixel0 += random.uniform(0, noise)
    pixel1 += random.uniform(0, noise)

    # Estimate the depth given the noisey pixel positions
    depth_estimate = math.tan(math.pi / 4) * math.fabs(pixel1 - pixel0)

    # Calculate the error in the depth estimate
    estimate_error = math.fabs(depth_estimate - depth)

    logging.debug("Angular Resolution: %s", angular_resolution)
    logging.debug("Depth:              %s", depth)
    logging.debug("Noise:              %s", noise)
    logging.debug("Pixel 0:            %s", pixel0)
    logging.debug("Pixel 1:            %s", pixel1)
    logging.debug("Depth Estimate:     %s", depth_estimate)
    logging.debug("Error:              %s", estimate_error)

    return estimate_error

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "debug":
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    depths       = [1, 5, 10, 25, 50, 100, 1000, 4000]
    noises       = [0.1, 0.75, 0.5, 0.25, 0.1, 0.05, 0.01, 0.001, 0.0001]
    sensor_width = 0.0359
    
    # For each depth distance of interest
    for depth in depths:
        logging.info("Performing error sensitivity analysis for depth %s...", depth)        

        # Determine the maximum possible spatial resolution
        max_angular_resolution = math.atan(sensor_width * 0.5 / depth)
        logging.info("Maximum possible angular resolution: %s", max_angular_resolution)

        # For each angular resolution
        for angular_resolution_iter in range(100):
            angular_resolution = angular_resolution_iter * max_angular_resolution / 100
            logging.info("Performing error sensitivity analysis for angular resolution %s...", angular_resolution)

            # For each noise value
            for noise in noises:
                logging.info("Noise (%% of sensor width): %s", noise)

                # Noise is applied randomly so take a definitive sample
                error = 0
                for iter in range(100):
                    error += estimate_error(angular_resolution, depth, noise * sensor_width)
                    
                error /= 100
                print "Error: ", error

        
    estimate_error(1, 10, 0.001)
