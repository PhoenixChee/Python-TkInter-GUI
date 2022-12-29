from GUI import data
from PIL import Image, ImageTk

import cv2

camOn = False
currentCamSettings = {}
currentImageSettings = {}


def switchCamera(frame, toggle):
    global camOn, cap

    # Camera Port
    cap = cv2.VideoCapture(data['camSettings']['port'])

    # Configure Camera Settings
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, data['camSettings']['resolutionWidth'])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, data['camSettings']['resolutionHeight'])
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FPS, data['camSettings']['targetFPS'])

    if toggle.get() == 1:
        camOn = True
        showFrames(frame)
    elif toggle.get() == 0:
        camOn = False
        cap.release()
        frame.configure(image='')


def showFrames(frame):
    if camOn:
        # Capture Video Frames & Convert to OpenCV (BGR) to PIL (RGB) Color Convention Format
        cv2Image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
        cv2Image = cv2.resize(cv2Image, (data['imageSettings']['width'], data['imageSettings']['height']))
        pilImage = Image.fromarray(cv2Image)

        # Configure Target Frame as PIL Image
        imgtk = ImageTk.PhotoImage(image=pilImage)
        frame.imgtk = imgtk
        frame.configure(image=imgtk)
        frame.after(int(1000/data['imageSettings']['targetFPS']), lambda: showFrames(frame))


def camSettings():
    currentCamSettings['widthResolution'] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    currentCamSettings['heightResolution'] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    currentCamSettings['targetFPS'] = int(cap.get(cv2.CAP_PROP_FPS))
    
    return currentCamSettings


def imageSettings():
    currentImageSettings['imageWidth'] = data['imageSettings']['width']
    currentImageSettings['imageHeight'] = data['imageSettings']['height']
    currentImageSettings['imageFPS'] = data['imageSettings']['targetFPS']

    return currentImageSettings


print('Imported LiveCam.py')
