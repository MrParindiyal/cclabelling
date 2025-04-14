# import libs
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
import distinctipy

def cclabeling(path):
  # Read image
  img = cv.imread(path)
  # Convert it to grayscale image
  gray = cv.imread(path, cv.IMREAD_GRAYSCALE)
  # Convert it to binary image
  ret,thresh = cv.threshold(gray,100,255,cv.THRESH_BINARY)  

  ###################
  # Label the image #
  ###################
  # identify the dimensions of image to traverse it
  rows, cols = thresh.shape[0], thresh.shape[1]
  # initialise label value to 0
  label = 0
  # dictionary to maintain relation between labels if it exists 
  equivalency_dict = {}
  # traverse the image row-wise
  for i in range(rows):
    for j in range(cols):
      # mark the pixel and it's top and left neighbour
      curr_pixel = thresh[i][j]
      top = thresh[i-1][j] if i > 0 else 0
      left = thresh[i][j-1] if j > 0 else 0
      
      # if the current pixel is part of foreground
      if curr_pixel == 255:
        # if the pixel is not connected to any component 
        if top == 0 and left == 0:
          # update label when new component discovered
          label += 1
          # mark the pixel with label
          thresh[i][j] = label
          # add the relation to dict
          equivalency_dict[label] = label

        elif top != 0 and left == 0:
          thresh[i][j] = top
              
        elif top == 0 and left != 0:
          thresh[i][j] = left

        else:  # Both top and left are nonzero
          min_label = min(top, left)
          max_label = max(top, left)
          # label the pixel with minimum value
          thresh[i][j] = min_label
          # add the relation between the max_label and min_label into dict
          if equivalency_dict[int(max_label)] > int(min_label):
            equivalency_dict[int(max_label)] = int(min_label)

  # find minimal equivalence_dict from equivalence_dict
  # function to find root label
  def find_root(label, eq_dict):
      while eq_dict[label] != label:
          label = eq_dict[label]
      return label

  # create minimal equivalency dict
  minimal_equivalency_dict = {}
  for key in equivalency_dict:
      root = find_root(key, equivalency_dict)
      minimal_equivalency_dict[key] = root

  # also ensure that all root values point to themselves
  for val in minimal_equivalency_dict.values():
      minimal_equivalency_dict[val] = val

  # create a dynamic color map for the image
  unique_labels = np.unique(list(minimal_equivalency_dict.values()))
  colors = distinctipy.get_colors(len(unique_labels))
  color_map = {}
  for i in range(len(unique_labels)):
    color_map[unique_labels[i]] = colors[i]

  # convert single channel to 3-channel image
  thresh = cv.merge((thresh.copy(), thresh.copy(), thresh.copy()))
  thresh = thresh.astype(np.float64)

  # re-traverse the image to update the label based on minimal equivalency_dict
  for i in range(rows):
    for j in range(cols):
      # mark the pixels
      curr_pixel = thresh[i][j][1]
      top = thresh[i-1][j][1] if i > 0 else 0
      left = thresh[i][j-1][1] if j > 0 else 0
      
      # if the current pixel is part of foreground
      if curr_pixel != 0:
        # update the label
        connected_label = color_map[minimal_equivalency_dict[curr_pixel]]
        thresh[i][j] = connected_label
  # convert the float values to standard 8-bit values
  thresh = (np.array(thresh) * 255).astype(np.uint8)
  
  # show the original and final image
  og_image_path = '../images/og_image.jpg'
  labeled_image_path = '../images/labeled_image.jpg'
  plt.imsave(og_image_path , img)
  plt.imsave(labeled_image_path, thresh)

  return [og_image_path, labeled_image_path]
