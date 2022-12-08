from GUI import *
from PIL import Image, ImageTk

import cv2


def switchCamera(frame, toggle):
    global camOn, cam
    cam = cv2.VideoCapture(data['camSettings']['port'])

    if toggle.get() == 1:
        camOn = True
        showFrames(frame)
        print("Show Camera On Display: Enabled")
    elif toggle.get() == 0:
        camOn = False
        cam.release()
        frame.configure(image='')
        print("Show Camera On Display: Disabled")


def showFrames(frame):
    global camOn, cam
    if camOn:
        cv2image = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        frame.imgtk = imgtk
        frame.configure(image=imgtk)
        frame.after(data['camSettings']['refreshRate'], lambda: showFrames(frame))


print('Imported LiveCam.py')
