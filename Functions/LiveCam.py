from GUI import *
from PIL import Image, ImageTk

import cv2

camOn = False


def switchCamera(frame, toggle):
    global camOn, cam

    # Camera Port
    cam = cv2.VideoCapture(data['camSettings']['port'],  cv2.CAP_DSHOW)

    # Configure Camera Settings
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, data['camSettings']['resolutionWidth'])
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, data['camSettings']['resolutionHeight'])
    cam.set(cv2.CAP_PROP_FPS, data['camSettings']['targetFPS'])

    if toggle.get() == 1:
        camOn = True
        camSettings()
        showFrames(frame)
    elif toggle.get() == 0:
        camOn = False
        cam.release()
        frame.configure(image='')


def showFrames(frame):
    if camOn:
        # Capture Video Frames & Convert to OpenCV (BGR) to PIL (RGB) Color Convention Format
        cv2Image = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2RGB)
        cv2Image = cv2.resize(cv2Image, (data['imageSettings']['width'], data['imageSettings']['height']))
        pilImage = Image.fromarray(cv2Image)

        # Configure Target Frame as PIL Image
        imgtk = ImageTk.PhotoImage(image=pilImage)
        frame.imgtk = imgtk
        frame.configure(image=imgtk)
        frame.after(int(1000/data['imageSettings']['targetFPS']), lambda: showFrames(frame))


def camSettings():
    if camOn:
        widthResolution = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        heightResolution = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        targetFPS = int(cam.get(cv2.CAP_PROP_FPS))

        return widthResolution, heightResolution, targetFPS


def imageSettings():
    if camOn:
        imageWidth = data['imageSettings']['width']
        imageHeight = data['imageSettings']['height']
        imageFPS = data['imageSettings']['targetFPS']

        return imageWidth, imageHeight, imageFPS


print('Imported LiveCam.py')
