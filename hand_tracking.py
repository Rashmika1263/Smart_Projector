import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_holistic = mp.solutions.holistic
import numpy as np

# For webcam input:
cap = cv2.VideoCapture(2)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    refine_face_landmarks=False) as holistic:


        while cap.isOpened():
          success, image = cap.read()
          if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        
          # To improve performance, optionally mark the image as not writeable to
          # pass by reference.
          image.flags.writeable = False
          hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
          image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
          holistic_results = holistic.process(image)
          results = hands.process(image)

        #   lower_red = np.array([30,150,50])
        #   upper_red = np.array([255,255,180])
        #   mask = cv2.inRange(hsv, lower_red, upper_red)
        #   res = cv2.bitwise_and(image,image, mask= mask)
        #   edges = cv2.Canny(image,100,200)
        #   cv2.imshow('Edges',edges)

          # Draw the hand annotations on the image.
          image.flags.writeable = True
          image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


          mp_drawing.draw_landmarks(
            image,
            holistic_results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles
            .get_default_pose_landmarks_style())
            
          if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
              mp_drawing.draw_landmarks(
                  image,
                  hand_landmarks,
                  mp_hands.HAND_CONNECTIONS,
                  mp_drawing_styles.get_default_hand_landmarks_style(),
                  mp_drawing_styles.get_default_hand_connections_style())
          # Flip the image horizontally for a selfie-view display.
          cv2.imshow('MediaPipe Hands',image)
          if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()