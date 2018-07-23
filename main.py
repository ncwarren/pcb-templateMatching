import cv2
import numpy as np
from argparse import ArgumentParser

# https://pythonprogramming.net/template-matching-python-opencv-tutorial/

if __name__ == "__main__":

    print('Initializing...')

    # Parse Arguments
    parser = ArgumentParser()
    parser.add_argument("-p", "--pcb", dest="pcb",
                    help="The PCB image to detect landmarks of",
                    metavar="QUEUE")
    parser.add_argument("-t", "--threshold", dest="threshold",
                help="File name containing names/pos of landmarks to template match. x,y | relative to project root",
                metavar="LENGTH")
    args = parser.parse_args()
    threshold = float(args.threshold)

    # Get templates for landmarks
    landmarkFile = open('./pcb/'+args.pcb+'.txt', 'r')
    landmarks = []
    for line in landmarkFile:
        # (x,y) \ ./landmarkLib/<type>/<name>.jpg
        line = line.rstrip('\n')
        pos, templatePath = line.split(' | ')

        nameArr = templatePath.split('/')
        name = nameArr[-1]
        nameArr = name.split('.')
        name = nameArr[0]
        template = cv2.imread(templatePath, 0)

        landmarks.append({'pos':pos,'template':template,'name':name})


    # Open PCB image file
    im = cv2.imread('./pcb/'+args.pcb+'.jpg')
    img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']


    detectedLandmarks = []
    for landmark in landmarks:
        print(landmark)
        template = landmark['template']
        w, h = template.shape[::-1]

        # Apply template Matching
        res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        possiblePt = []
        for pt in zip(*loc[::-1]):
            possiblePt.append(pt)
            cv2.rectangle(im, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)

        detectedLandmarks.append({'landmark':landmark['name'],
                                'expectedPos':landmark['pos'],
                                'actualPosArr':possiblePt})

    print('Wrapping up detection...')

    # cv2.startWindowThread()
    cv2.namedWindow("Detected")
    imSized = cv2.resize(im, (1040,780))
    cv2.imshow('Detected',imSized)
    # cv2.resizeWindow('Detected', 600,600)
    cv2.waitKey(0)
