import cv2
import random
import colorsys
import numpy as np
import tensorflow as tf
import pytesseract
from core.config import cfg
import re
import os
import matplotlib.pyplot as plt
import tensorflow.keras as keras
# import core.predicter as predicter
# from core.serial import grayscale_and_resize


def grayscale(img):
    def RGB2GRAY(img):
        gray_img = []
        for sets in img:
            gray_img.append(int(0.299*sets[0] + 0.587*sets[1] + 0.114*sets[2]))
        return gray_img
    pix_val = []
    # img = cv2.imread('small.jpg')
    for arr in img:
        for pix in arr:
            pix_val.append((pix[2], pix[1], pix[0]))
            
    # print(pix_val)
    
    gray_list = RGB2GRAY(pix_val)
    gray_arr = np.array(gray_list).reshape(img.shape[0],img.shape[1]).astype('uint8')
    
    return gray_arr
    
    

def resize3x3(img):
    w = 3*(img.shape[1]-1)
    h = 3*(img.shape[0]-1)
    # print(w, h)
    
    res = np.zeros((h, w))
    for y in range(h):
        for x in range(w):
            x1 = x // 3
            y1 = y // 3
            x2 = x1+1
            y2 = y1+1
            
            s1 = img[y1,x1] * (3*x2-x) * (3*y2-y)
            s2 = img[y1,x2] * (x-3*x1) * (3*y2-y)
            s3 = img[y2,x1] * (3*x2-x) * (y-3*y1)
            s4 = img[y2,x2] * (x-3*x1) * (y-3*y1)
            
            try:
                res[y,x] = np.int32(1/9 * (s1+s2+s3+s4))
            except Exception as e:
                print("ERROR")
                # print("x1: ", x1, "x2: ", x2, "y1: ", y1, "y2: ", y2)
                # print(x, y)
        
    return res.astype('uint8')

# If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

# function to recognize license plate numbers using Tesseract OCR
def recognize_plate(img, coords, ocr_model):
    # separate coordinates from box
    xmin, ymin, xmax, ymax = coords
    # get the subimage that makes up the bounded region and take an additional 5 pixels on each side
    box = img[int(ymin)-5:int(ymax)+5, int(xmin)-5:int(xmax)+5]


    
    # # grayscale region within bounding box
    # gray = cv2.cvtColor(box, cv2.COLOR_RGB2GRAY)
    # # resize image to three times as large as original for better readability
    # gray = cv2.resize(gray, None, fx = 3, fy = 3, interpolation = cv2.INTER_CUBIC)


    gray = grayscale_and_resize(box)
    # gray = grayscale(box)
    # gray = resize3x3(gray)

    
    # perform gaussian blur to smoothen image
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    #cv2.imshow("Gray", gray)
    #cv2.waitKey(0)
    # threshold the image using Otsus method to preprocess for tesseract
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    #cv2.imshow("Otsu Threshold", thresh)
    #cv2.waitKey(0)
    # create rectangular kernel for dilation
    rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    # apply dilation to make regions more clear
    dilation = cv2.dilate(thresh, rect_kern, iterations = 1)
    #cv2.imshow("Dilation", dilation)
    #cv2.waitKey(0)
    # find contours of regions of interest within license plate
    try:
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    except:
        ret_img, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # sort contours left-to-right
    sorted_contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])
    # create copy of gray image
    im2 = gray.copy()
    # create blank string to hold license plate number
    plate_num = ""
    # loop through contours and find individual letters and numbers in license plate
    for cnt in sorted_contours:
        x,y,w,h = cv2.boundingRect(cnt)
        height, width = im2.shape
        # if height of box is not tall enough relative to total height then skip
        if height / float(h) > 6: continue

        ratio = h / float(w)
        # if height to width ratio is less than 1.5 skip
        if ratio < 1.5: continue

        # if width is not wide enough relative to total width then skip
        if width / float(w) > 15: continue

        area = h * w
        # if area is less than 100 pixels skip
        if area < 100: continue

        # draw the rectangle
        rect = cv2.rectangle(im2, (x,y), (x+w, y+h), (0,255,0),2)
        # grab character region of image
        roi = thresh[y-5:y+h+5, x-5:x+w+5]

        if not is_black_on_white(roi):
            # perfrom bitwise not to flip image to black text on white background
            roi = cv2.bitwise_not(roi)
        # perform another blur on character region
        roi = cv2.medianBlur(roi, 5)

        try:
            def find_char(char_class):
                if char_class < 10:
                    return char_class
                elif char_class < 24:
                    return chr(ord('@')+char_class-9)
                else:
                    return chr(ord('@')+char_class-8)

            img = cv2.resize(roi, (100, 50))
            img = tf.keras.utils.normalize(img, axis=1).reshape(1, -1)
            predictions = ocr_model.predict(img)
            plate_num += str(find_char(np.argmax(predictions[0])))
        except:
            print('except')
            text = None
    if plate_num != None:
        print("License Plate #: ", plate_num)
    #cv2.imshow("Character's Segmented", im2)
    #cv2.waitKey(0)
    return plate_num

# function to regognize chars from sorter countours of LP
def find_character_contour(sorted_contours, im2, thresh):
    cnts = []

    for cnt in sorted_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        height, width = im2.shape
        # if height of box is not tall enough relative to total height then skip
        if height / float(h) > 5: continue  # REQ: float(h) > height / 5

        ratio = h / float(w)
        # if height to width ratio is less than 1.5 skip
        if ratio < 1.5: continue  # REQ: h > 1.5 * w

        # if width is not wide enough relative to total width then skip
        if width / float(w) > 15: continue  # REQ: float(w) > width / 15

        area = h * w
        # if area is less than 100 pixels skip
        if area < 100: continue  # REQ: area > 100

        # draw the rectangle
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # grab character region of image
        roi = thresh[y - 5:y + h + 5, x - 5:x + w + 5]
        # perfrom bitwise not to flip image to black text on white background
        roi = cv2.bitwise_not(roi)
        # perform another blur on character region
        roi = cv2.medianBlur(roi, 5)

        # cv2.imshow("roi",roi)

        cnts.append(cnt)

    return cnts


def add_missed_chars(sorted_contours, cnts, im2, thresh):
    for cnt in sorted_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        ratio = h / float(w)
        # if height to width ratio is less than 1.5 skip
        if ratio < 1.5: continue
        height_threshold = h / 10.0
        present = False
        add = False
        for cnt_stored in cnts:
            if np.array_equal(cnt, cnt_stored):
                present = True
                break
            X, Y, W, H = cv2.boundingRect(cnt_stored)
            if abs(y - Y) <= height_threshold and abs(h - H) <= height_threshold:
                add = True

        if present == False and add == True:
            roi2 = thresh[y - 5:y + h + 5, x - 5:x + w + 5]
            # perfrom bitwise not to flip image to black text on white background
            roi2 = cv2.bitwise_not(roi2)
            # perform another blur on character region
            roi2 = cv2.medianBlur(roi2, 5)

            # cv2.imshow("roi",roi2)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            cnts.append(cnt)


def remove_garbage_contours(plausible_characters):
    grouped_cnts = []
    for cnt in plausible_characters:
        x, y, w, h = cv2.boundingRect(cnt)
        height_threshold = h / 5.0

        grouped = False
        for group in grouped_cnts:
            if grouped:
                break
            for X, Y, W, H in group:
                if abs(y - Y) <= height_threshold and abs(h - H) <= height_threshold:
                    # append x,y,w,h to group
                    group.append((x, y, w, h))
                    grouped = True
                    break

        if not grouped:
            grouped_cnts.append([(x, y, w, h)])

    grouped_cnts_lengths = [len(x) for x in grouped_cnts]

    removables = []
    for i in range(len(grouped_cnts_lengths)):
        if grouped_cnts_lengths[i] == max(grouped_cnts_lengths):
            continue
        for x, y, w, h in grouped_cnts[i]:
            removables.append((x, y, w, h))

    removables_set = set(removables)
    for cnt in plausible_characters:
        x, y, w, h = cv2.boundingRect(cnt)
        if (x, y, w, h) in removables_set:
            plausible_characters.remove(cnt)


def save_cropped_char(path, rois):
    for roi in rois:
        file_names = os.listdir(path)
        file_numbers = [int(file[:-4]) for file in file_names]
        last_file = max(file_numbers)
        new_file_name = str(last_file + 1) + '.jpg'
        new_file_path = os.path.join(path, new_file_name)
        cv2.imwrite(new_file_path, roi)
        # cv2.waitKey(0)


def is_black_on_white(roi):
    w, h = roi.shape
    top_row_sum = np.sum(roi[0, :])
    left_col_sum = np.sum(roi[:, 0])
    bottom_row_sum = np.sum(roi[-1, :])
    right_col_sum = np.sum(roi[:, -1])
    avg_intensity = (top_row_sum + left_col_sum + bottom_row_sum + right_col_sum) / (2 * w + 2 * h)
    return avg_intensity > 127


def get_rois(cnts, thresh):
    rois = []
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)

        roi = thresh[y - 5:y + h + 5, x - 5:x + w + 5]

        if not is_black_on_white(roi):
            # perfrom bitwise not to flip image to black text on white background
            roi = cv2.bitwise_not(roi)
        # perform another blur on character region
        roi = cv2.medianBlur(roi, 5)
        rois.append(roi)

    return rois


def hconcat_resize(img_list, interpolation=cv2.INTER_CUBIC):
    # take minimum hights
    h_min = min(img.shape[0] for img in img_list)

    # image resizing
    im_list_resize = [cv2.resize(img, (int(img.shape[1] * h_min / img.shape[0]), h_min), interpolation=interpolation)
                      for img in img_list]

    # return final image
    return cv2.hconcat(im_list_resize)


def show_detected_rois(rois):
    rois_concat = hconcat_resize(rois)
    #cv2.imshow("all characters", rois_concat)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return rois_concat
    


def debug_contour_pos(plausible_characters):
    plausible_characters_pos = [cv2.boundingRect(cnt) for cnt in plausible_characters]
    print(plausible_characters_pos)


# function to recognize license plate numbers using Tesseract OCR
# def recognize_plate(img, coords):
#     # separate coordinates from box
#     xmin, ymin, xmax, ymax = coords
#     # get the subimage that makes up the bounded region and take an additional 5 pixels on each side
#     box = img[int(ymin) - 5:int(ymax) + 5, int(xmin) - 5:int(xmax) + 5]
# 
# 
#     #---------------------------- start of opencv code -------------------------------------#
# 
#     # grayscale region within bounding box
#     # gray = cv2.cvtColor(box, cv2.COLOR_RGB2GRAY)
#     # resize image to three times as large as original for better readability
#     # gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
# 
#     #---------------------------- end of opencv code ---------------------------------------#
# 
#     #----------------------------start of hw accel -----------------------------------------#
# 
#     gray = grayscale_and_resize(box)
#     #gray = grayscale(box)
#     #gray = resize3x3(gray)
# 
#     #---------------------------- end of hw accel ------------------------------------------#
# 
#     # perform gaussian blur to smoothen image
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     # cv2.imshow("Gray", gray)
#     # cv2.waitKey(0)
#     # threshold the image using Otsus method to preprocess for tesseract
#     ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
#     # cv2.imshow("Otsu Threshold", thresh)
#     # cv2.waitKey(0)
#     # create rectangular kernel for dilation
#     rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
#     # apply dilation to make regions more clear
#     # dilation = cv2.dilate(thresh, rect_kern, iterations = 1)
#     dilation = thresh
#     #cv2.imshow("Dilation", dilation)
#     #cv2.waitKey(0)
#     # find contours of regions of interest within license plate
#     try:
#         contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     except:
#         ret_img, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     # sort contours left-to-right
#     sorted_contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])
#     print('sorted contours len:', len(sorted_contours), ', countours len: ', len(contours))
# 
#     # create copy of gray image
#     im2 = gray.copy()
#     # create blank string to hold license plate number
#     plate_num = ""
#     # loop through contours and find individual letters and numbers in license plate
# 
#     plausible_characters = find_character_contour(sorted_contours, im2, thresh)
#     debug_contour_pos(plausible_characters)
# 
#     remove_garbage_contours(plausible_characters)
# 
#     add_missed_chars(sorted_contours, plausible_characters, im2, thresh)
#     plausible_characters = sorted(plausible_characters, key=lambda ctr: cv2.boundingRect(ctr)[0])
#     debug_contour_pos(plausible_characters)
# 
#     rois = get_rois(plausible_characters, thresh)
# 
#     # save_dir = r"C:\Users\Vijeeth Rakshakar\Documents\CPEN 391\Char recognition\cropped_chars_test"
#     # crop_filt = False
#     # if crop_filt:
#     #     save_cropped_char(save_dir, rois)
# 
#     roi = show_detected_rois(rois)
# 
#     try:
#         text = pytesseract.image_to_string(roi, config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8 --oem 3')
#         # clean tesseract text by removing any unwanted blank spaces
#         clean_text = re.sub('[\W_]+', '', text)
#         plate_num += clean_text
#     except:
#         text = None
#     if plate_num != None:
#         print("License Plate #: ", plate_num)
#     # print(cnts_pos)
#     #
#     # cv2.imshow("Character's Segmented", im2)
#     # cv2.waitKey(0)
# 
#     return plate_num

# function to read class name
def read_class_names(class_file_name):
    names = {}
    with open(class_file_name, 'r') as data:
        for ID, name in enumerate(data):
            names[ID] = name.strip('\n')
    return names

# helper function to convert bounding boxes from normalized ymin, xmin, ymax, xmax ---> xmin, ymin, xmax, ymax
def format_boxes(bboxes, image_height, image_width):
    for box in bboxes:
        ymin = int(box[0] * image_height)
        xmin = int(box[1] * image_width)
        ymax = int(box[2] * image_height)
        xmax = int(box[3] * image_width)
        box[0], box[1], box[2], box[3] = xmin, ymin, xmax, ymax
    return bboxes

def draw_bbox(image, bboxes, model, info = False, counted_classes = None, show_label=True, allowed_classes=list(read_class_names(cfg.YOLO.CLASSES).values()), read_plate = False):
    classes = read_class_names(cfg.YOLO.CLASSES)
    num_classes = len(classes)
    image_h, image_w, _ = image.shape
    hsv_tuples = [(1.0 * x / num_classes, 1., 1.) for x in range(num_classes)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))
    plate_number = ""

    random.seed(0)
    random.shuffle(colors)
    random.seed(None)

    out_boxes, out_scores, out_classes, num_boxes = bboxes
    for i in range(num_boxes):
        if int(out_classes[i]) < 0 or int(out_classes[i]) > num_classes: continue
        coor = out_boxes[i]
        fontScale = 0.5
        score = out_scores[i]
        class_ind = int(out_classes[i])
        class_name = classes[class_ind]
        if class_name not in allowed_classes:
            continue
        else:
            if read_plate:
                height_ratio = int(image_h / 25)
                plate_number = recognize_plate(image, coor, model)
                if plate_number != None:
                    cv2.putText(image, plate_number, (int(coor[0]), int(coor[1]-height_ratio)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.25, (255,255,0), 2)

            bbox_color = colors[class_ind]
            bbox_thick = int(0.6 * (image_h + image_w) / 600)
            c1, c2 = (coor[0], coor[1]), (coor[2], coor[3])
            cv2.rectangle(image, c1, c2, bbox_color, bbox_thick)

            if info:
                print("Object found: {}, Confidence: {:.2f}, BBox Coords (xmin, ymin, xmax, ymax): {}, {}, {}, {} ".format(class_name, score, coor[0], coor[1], coor[2], coor[3]))

            if show_label:
                bbox_mess = '%s: %.2f' % (class_name, score)
                t_size = cv2.getTextSize(bbox_mess, 0, fontScale, thickness=bbox_thick // 2)[0]
                c3 = (c1[0] + t_size[0], c1[1] - t_size[1] - 3)
                cv2.rectangle(image, c1, (np.float32(c3[0]), np.float32(c3[1])), bbox_color, -1) #filled

                cv2.putText(image, bbox_mess, (c1[0], np.float32(c1[1] - 2)), cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale, (0, 0, 0), bbox_thick // 2, lineType=cv2.LINE_AA)

            if counted_classes != None:
                height_ratio = int(image_h / 25)
                offset = 15
                for key, value in counted_classes.items():
                    cv2.putText(image, "{}s detected: {}".format(key, value), (5, offset),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
                    offset += height_ratio
    return image, plate_number
