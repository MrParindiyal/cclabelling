import cv2
import distinctipy
import logging
import matplotlib.pyplot as plt
import numpy as np


logging.getLogger(__name__)


def labeller(input_path, output_path):
    img = cv2.imread(input_path)

    R_channel = 2; G_channel = 1; B_channel = 0

    # Here, curr_label can also start from 1, but I'm using 2 so as to avoid any 
    # confusions in the labelling matrix, as active pixels are also using 1 initially
    curr_label = 2

# ===============================================

    # def greyscale(image):
    #     img2 = image.copy()
    #     for row in range(img2.shape[0]):
    #         for col in range(img2.shape[1]):
    #             if min(img2[row][col].sum() / 3, 255) <= 255:
    #                 img2[row][col] = np.array([(np.uint8(img2[row][col].sum() / 3))] * 3)
                
    #             else:
    #                 img2[row][col] = np.array([(np.uint8(255))] * 3)

    #     return img2


    # def binarizer(image0, threshold):
    #     image = image0.copy()
    #     for r in range(image.shape[0]):
    #         for c in range(image.shape[1]):
    #             if image[r][c][0] <= threshold:
    #                 image[r][c] = np.array([np.uint8(0)] * 3)
                
    #             else:
    #                 image[r][c] = np.array([np.uint8(255)] * 3)

    #     return image


    # img_greyed = greyscale(img)
    # img_bin = binarizer(img_greyed, threshold = 128)
    # img = img_bin.copy()

# ===============================================

    # A label matrix for image. The background is initialized as 0s and any white pixel is
    # marked as 1. To check if a pixel is white we check any of its BRG channel. Since we started
    # a binary image in the first place, a pixel can either be [0, 0, 0] or [255, 255, 255]
    # For a more flexible approach, we would need to first convert an image into greyscale,
    # then into a binary image with a single grey channel using some threshold.
    # But here, we are assuming given image is binary with 3 channels for simplicity.
    label = [[0 for _ in range(img.shape[1])] for _ in range(img.shape[0])] # init label matrix

    # set pixel to 1 wherever a pixel is in foreground in given imag.
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            try:
                if img[i][j][B_channel]:
                    label[i][j] = 1

            except Exception as e:
                logging.exception(f"{e} at {i}, {j}")

    # List to storing relation sets of format {x, y} where x and y are label values
    # for same object in foreground 
    objs = [] 

    # iterating each value in label matrix
    for row in range(len(label)):
        for col in range(len(label[0])):
            
            # if pixel is active and not in 1st row/col
            if label[row][col] and row and col:

                # if pixel on top and left are inactive, assign new label
                if not label[row - 1][col] and not label[row][col - 1]:
                    label[row][col] = curr_label
                    curr_label += 1 # and increment for furture use

                # otherwise, either top or left pixel is active
                else: 

                    # if top and left pixel are active, we append them into objs as a set
                    # TODO
                    # can't we simply append if both top and left are active?
                    if label[row][col - 1] != label[row - 1][col] and label[row][col - 1] and label[row - 1][col]:
                        objs.append({label[row][col - 1], label[row - 1][col]})

                    elif label[row][col - 1] == label[row - 1][col] and label[row][col - 1] and label[row - 1][col]:
                        objs.append({label[row][col - 1], label[row - 1][col]})


                    if label[row - 1][col]:					# if top pixel is active, we assign that label value
                        label[row][col] = label[row - 1][col]
                    else:             						# otherwise assign left pixel label value
                        label[row][col] = label[row][col - 1]

                    # to avoid label value inflation, we check if left pixel is lower label value
                    # than current pixel, then assign it (in case previously it was assigned top pixel's label)
                    if label[row][col - 1] and label[row][col - 1] < label[row][col]:
                        label[row][col] = label[row][col - 1]


            # in case the pixel is in 1st row
            elif col and not row and label[row][col]:
                if label[row][col - 1]:     					# and pixel to left is active
                    label[row][col] = label[row][col - 1]		# we assign left pixel's label
                    if {label[row][col - 1], label[row][col]} not in objs:	# if set is not in objs list,
                        objs.append({label[row][col - 1], label[row][col]})	# append it.

                else:								# this means 1st row but left pixel is inactive
                    label[row][col] = curr_label	# in that case, assign new label
                    curr_label += 1
                    if {label[row][col], label[row][col]} not in objs:		# and insert self set into objs, otherwise objects with
                        objs.append({label[row][col], label[row][col]})		# only single pure label values won't be detected anywhere

            # in case pixel is in 1st col
            elif not col and label[row][col]:						
                if label[row - 1][col]:						# and pixel on top is active
                    label[row][col] = label[row - 1][col] 	# then assign top pixel's label
                    if {label[row - 1][col], label[row][col]} not in objs:	# append set to objs if not present already
                        objs.append({label[row - 1][col], label[row][col]})
                
                else:								# this means 1st col but top pixel is inactive
                    label[row][col] = curr_label
                    curr_label += 1
                    if {label[row][col], label[row][col]} not in objs:		# insert self set into objs, otherwise objects with
                        objs.append({label[row][col], label[row][col]})		# only single pure label values won't be detected anywhere


    objs_set = list(set(frozenset(item) for item in objs))

    final_objs = []

    # TODO 
    # is this even used anywhere? #danglingList
    objs2 = [set(x) for x in objs_set] # convert frozensets back to sets

    # while there are sets in objs_sets
    while objs_set:
        curr_obj = objs_set.pop()		# pop out a random set
        merged = True					# set flag 'merged' to true
        
        while merged:			# loop till flag is not back to false
            merged = False		# set flag to false (default case)
            rest = []			# a temp list for storing remaining joint sets
            
            for other in objs_set:						# iterate over every set
                if not curr_obj.isdisjoint(other):		# if the 'other' set is joint
                    curr_obj |= other					# take its union with curr_obj set
                    merged = True						# 'other' was merged, hence the flag is ON again
                    
                else:						# in case 'other' was disjoint with 'curr_obj'
                    rest.append(other)		# append it to rest list
            
            # now all DIRECTLY joint sets with 'curr_obj' are merged, so we now update objs_set with rest
            objs_set = rest		
            # after this, we reiterate the list to pick up any remaining joint sets. if no merges
            # are made in a pass, we know that all the labels of an object are successfully found
            # and merged. This while loop will break due to merged flag not getting ON

        # Thus we add this as a frozenset to final_objs list
        final_objs.append(frozenset(curr_obj))


    # TODO 
    # (objidx) % len(colors_bgr) is no longer required ?
    def get_color(label):
        for objidx in range(len(final_objs)):
            if label in final_objs[objidx]:
                return colors_bgr[(objidx) % len(colors_bgr)]

        return [0, 0, 0]


    # Generate as many distinct colors as there are objects in image
    colors_bgr = distinctipy.get_colors(len(final_objs))

    # Convert RGB tuples into list
    colors_bgr = [list(y) for y in colors_bgr]

    # Then scale the values from 0 - 1 to 0 - 255 and clip at 255
    colors_bgr = [[min(channel * 255, 255) for channel in pixel] for pixel in colors_bgr]

    # Convert list and floats to numpy array-like and uint8 type, respectively.
    colors_bgr = [np.array(np.uint8(x)) for x in colors_bgr]

    
    # iterate all label values in label matrix
    for row in range(len(label)):
        for col in range(len(label[0])):
            
            # if label is non-zero (active)
            if label[row][col]:

                # check the set in final_objs for a match
                for obj in final_objs:
                    
                    # if the label is found in set, we fetch the min. value from that set
                    if label[row][col] in obj:
                        label[row][col] = min(obj)

                    # otherwise we move on to next set
    

    # reiterate the label matrix and change the corresponding pixel in the 
    # copy of given image, by passing label value to get_color function 

    for row in range(len(label)):
        for col in range(len(label[0])):
            if label[row][col] != 0:
                img[row][col] = get_color(label[row][col])


    plt.imsave(f"{output_path}", img)