import cv2
wCam, hCam = 640, 480

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)

all_coordinates = []



def mouse_click(event, x, y, flags, param):
    a = []
    if event == cv2.EVENT_LBUTTONDOWN:
        a.append(x)
        a.append(y)
        all_coordinates.append(a)
        if len(all_coordinates) == 4:
            print(all_coordinates)

def getCoordinates():
    while True:
        single_coordinate = []
        success, img = cap.read()
        cv2.imshow('image', img)
        single_coordinate.append(cv2.setMouseCallback('image', mouse_click))
        cv2.waitKey(1)

print(getCoordinates())
