import re
from pprint import pprint
from difflib import SequenceMatcher
import cv2
from matplotlib import pyplot as plt
import easyocr

states_list = [
    "ALABAMA",
    "ALASKA",
    "ARIZONA",
    "ARKANSAS",
    "CALIFORNIA",
    "COLORADO",
    "CONNECTICUT",
    "DELAWARE",
    "FLORIDA",
    "GEORGIA",
    "HAWAII",
    "IDAHO",
    "ILLINOIS",
    "INDIANA",
    "IOWA",
    "KANSAS",
    "KENTUCKY",
    "LOUISIANA",
    "MAINE",
    "MARYLAND",
    "MASSACHUSETTS",
    "MICHIGAN",
    "MINNESOTA",
    "MISSISSIPPI",
    "MISSOURI",
    "MONTANA",
    "NEBRASKA",
    "NEVADA",
    "NEW HAMPSHIRE",
    "NEW JERSEY",
    "NEW MEXICO",
    "NEW YORK",
    "NORTH CAROLINA",
    "NORTH DAKOTA",
    "OHIO",
    "OKLAHOMA",
    "OREGON",
    "PENNSYLVANIA",
    "RHODE ISLAND",
    "SOUTH CAROLINA",
    "SOUTH DAKOTA",
    "TENNESSEE",
    "TEXAS",
    "UTAH",
    "VERMONT",
    "VIRGINIA",
    "WASHINGTON",
    "WEST VIRGINIA",
    "WISCONSIN",
    "WYOMING"
]

kids_dict = {'SBN-8107': 'Gen',
             'PDL-5962': 'The Rabii',
             'SBC-5904': 'Terraform05'}


def identify_plate(image, kids_dict):
    rd = easyocr.Reader(['en'])
    image_text = rd.readtext(image)

    identified_list = []
    for i in image_text:
        identified_list.append(i[1])

    valid_options = []
    for i in identified_list:
        i = i.upper()
        if len(i) not in range(5, 10):
            continue
        if i in states_list:
            continue
        if re.match(re.compile("[a-zA-Z0-9. ]*"), i):
            valid_options.append(i)

    plate = None
    not_plate_options = []
    for i in valid_options:
        if re.match(r'^[A-Z]{3}-\d{4}$', i) and i in kids_dict.keys():
            plate = i
            break
        else:
            not_plate_options.append(i)

    if plate == None:
        option_correlations = []
        for i in not_plate_options:
            for key in kids_dict.keys():
                rat = SequenceMatcher(None, i, key).ratio()
                if rat > .7:
                    option_correlations.append((key, rat))

        print('Found Options: ', option_correlations)
        plate = max(option_correlations, key=lambda x: x[1])[0]
        print('highest match plate: ', plate)

    pprint(kids_dict)
    print('\n', 'Text Found: ', identified_list)
    print('\n', 'Valid Options: ', valid_options)
    print('\n', 'Chosen plate: ', plate)
    print('\n', 'Kid: ', kids_dict[plate])

    return plate, kids_dict[plate]


kid_jpg = 'ben'
image = cv2.imread(f'{kid_jpg}.jpg')

plate, kid = identify_plate(image, kids_dict)
print('\n', '=' * 50, '\n')
print('Plate: ', plate)
print('Kid: ', kid)
