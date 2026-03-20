import cv2
import matplotlib.pyplot as plt
from matplotlib import colormaps
import numpy as np
import os

# These key functions are just taken out of my gui-analysis-notebook testing
# They are then used in the eye tracking application

def prepare_for_connected_components(image, light_mode=True):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)

    if light_mode:
        pre_dilated = cv2.bitwise_not(thresh)
    else:
        pre_dilated = thresh
    
    # as opposed to my gui-analysis-notebook testing I reduced dilation here to create smaller snappable keypoints for the cursor
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(6,6))
    dilated = cv2.dilate(pre_dilated,kernel,iterations = 1)
    
    return dilated

def extract_icons(image, light_mode=True, save_icons=True, icon_list="dataset-1", smallest_ratio=0.000005, largest_ratio=0.025):
    processed = prepare_for_connected_components(image, light_mode)
    
    analysis = cv2.connectedComponentsWithStats(processed, 4, cv2.CV_32S) # what is CV_32S? would be good to research more
    
    (totalLabels, label_ids, stats, centroids) = analysis
    
    img_h = image.shape[0]
    img_w = image.shape[1]
    
    img_area = img_h*img_w
    
    overlay = image.copy() # crete an overlay to place over the image
    cv2.rectangle(overlay, (0, 0), (img_w, img_h), (0, 0, 0), -1) # convert to a black overlay
    
    # add shading so icons are clearer to see
    alpha = 0.8 
    shaded = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0) 
    bounding_boxes = shaded.copy()
    
    centres_dataset = []
    
    for i in range(1, totalLabels):
        area = stats[i, cv2.CC_STAT_AREA]  
        
        if (area/img_area > smallest_ratio) and (area/img_area < largest_ratio):
            
            (cX, cY) = centroids[i]
            
            x = stats[i, cv2.CC_STAT_LEFT]
            y = stats[i, cv2.CC_STAT_TOP]
            w = stats[i, cv2.CC_STAT_WIDTH]
            h = stats[i, cv2.CC_STAT_HEIGHT]
            # area = stats[i, cv2.CC_STAT_AREA]
                
            cv2.rectangle(bounding_boxes, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            centres_dataset.append([cX, cY])
        
    return bounding_boxes, centres_dataset