import cv2
import mediapipe as mp
import numpy as np
from pythonosc import udp_client
import argparse

IP = "10.12.181.191"  # Escribe el IP aquí
PORT1 = 10000  # Escribe el primer puerto aquí
#PORT2 = 10001  # Escribe el segundo puerto aquí

silhouette= [
    10,  338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
    397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
    172, 58,  132, 93,  234, 127, 162, 21,  54,  103, 67,  109]

lipsUpperInner= [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308]
lipsLowerInner= [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]

rightEyeUpper0 = [246, 161, 160, 159, 158, 157, 173]
rightEyeLower0= [33, 7, 163, 144, 145, 153, 154, 155, 133]
rightEyeUpper1= [247, 30, 29, 27, 28, 56, 190]
rightEyeLower1= [130, 25, 110, 24, 23, 22, 26, 112, 243]
rightEyeUpper2= [113, 225, 224, 223, 222, 221, 189]
rightEyeLower2= [226, 31, 228, 229, 230, 231, 232, 233, 244]
rightEyeLower3= [143, 111, 117, 118, 119, 120, 121, 128, 245]
  
leftEyeUpper0= [466, 388, 387, 386, 385, 384, 398]
leftEyeLower0= [263, 249, 390, 373, 374, 380, 381, 382, 362]
leftEyeUpper1= [467, 260, 259, 257, 258, 286, 414]
leftEyeLower1= [359, 255, 339, 254, 253, 252, 256, 341, 463]
leftEyeUpper2= [342, 445, 444, 443, 442, 441, 413]
leftEyeLower2= [446, 261, 448, 449, 450, 451, 452, 453, 464]
leftEyeLower3= [372, 340, 346, 347, 348, 349, 350, 357, 465]


# First Client - 5000
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default=IP, help="The ip of the OSC server")
parser.add_argument("--port", type=float, default=PORT1, help="The port the OSC server is listening on (1)")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.5) as face_mesh:

    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        frame = cv2.flip(frame,1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)
        
        if results.multi_face_landmarks is not None:

          
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(frame, face_landmarks,
                    mp_face_mesh.FACEMESH_CONTOURS,
                    mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1))
        

        #to touchDesigner
        #silhouette
        for sil in silhouette:
            client.send_message("/silhouette."+str({sil})+".x", round(float(face_landmarks.landmark[sil].x),5))
            client.send_message("/silhouette."+str({sil})+".y", round(float(face_landmarks.landmark[sil].y),5))

        # #lipsUpperInner
        for lips in lipsUpperInner:
            client.send_message("/lipsUpperInner."+str({lips})+".x", round(float(face_landmarks.landmark[lips].x),5))
            client.send_message("/lipsUpperInner."+str({lips})+".y", round(float(face_landmarks.landmark[lips].y),5))
        
        #lipsLowerInner
        for lips in lipsLowerInner:
            client.send_message("/lipsLowerInner."+str({lips})+".x", round(float(face_landmarks.landmark[lips].x),5))
            client.send_message("/lipsLowerInner."+str({lips})+".y", round(float(face_landmarks.landmark[lips].y),5))
               
        #rightEyeUpper0
        for eye in rightEyeUpper0:
            client.send_message("/rightEyeUpper0."+str({eye})+".x", round(float(face_landmarks.landmark[eye].x),5))
            client.send_message("/rightEyeUpper0."+str({eye})+".y", round(float(face_landmarks.landmark[eye].y),5))
               
        #rightEyeLower0
        for sil in rightEyeLower0:
            client.send_message("/rightEyeLower0."+str({sil})+".x", round(float(face_landmarks.landmark[sil].x),5))
            client.send_message("/rightEyeLower0."+str({sil})+".y", round(float(face_landmarks.landmark[sil].y),5))
               
        #rightEyeUpper1
        for sil in rightEyeUpper1:
            client.send_message("/rightEyeUpper1."+str({sil})+".x", round(float(face_landmarks.landmark[sil].x),5))
            client.send_message("/rightEyeUpper1."+str({sil})+".y", round(float(face_landmarks.landmark[sil].y),5))
               
        #rightEyeLower1
        for sil in rightEyeLower1:
            client.send_message("/rightEyeLower1."+str({sil})+".x", round(float(face_landmarks.landmark[sil].x),5))
            client.send_message("/rightEyeLower1."+str({sil})+".y", round(float(face_landmarks.landmark[sil].y),5))
               
        #rightEyeUpper2
        for sil in rightEyeUpper2:
            client.send_message("/rightEyeUpper2."+str({sil})+".x", round(float(face_landmarks.landmark[sil].x),5))
            client.send_message("/rightEyeUpper2."+str({sil})+".y", round(float(face_landmarks.landmark[sil].y),5))
               
        #rightEyeLower2
        for sil in rightEyeLower2:
            client.send_message("/rightEyeLower2."+str({sil})+".x", round(float(face_landmarks.landmark[sil].x),5))
            client.send_message("/rightEyeLower2."+str({sil})+".y", round(float(face_landmarks.landmark[sil].y),5))

          #rightEyeLower3
        for sil in rightEyeLower3:
            client.send_message("/rightEyeLower3."+str({sil})+".x", round(float(face_landmarks.landmark[sil].x),5))
            client.send_message("/rightEyeLower3."+str({sil})+".y", round(float(face_landmarks.landmark[sil].y),5))

          #leftEyeUpper0
        for sil in leftEyeUpper0:
            client.send_message("/leftEyeUpper0."+str({sil})+".x", round(float(face_landmarks.landmark[sil].x),5))
            client.send_message("/leftEyeUpper0."+str({sil})+".y", round(float(face_landmarks.landmark[sil].y),5))

          #leftEyeLower0
        for sil in leftEyeLower0:
            client.send_message("/leftEyeLower0."+str({sil})+".x", round(float(face_landmarks.landmark[sil].x),5))
            client.send_message("/leftEyeLower0."+str({sil})+".y", round(float(face_landmarks.landmark[sil].y),5))

          #leftEyeUpper1
        for sil in leftEyeUpper1:
            client.send_message("/leftEyeUpper1."+str({sil})+".x", round(float(face_landmarks.landmark[sil].x),5))
            client.send_message("/leftEyeUpper1."+str({sil})+".y", round(float(face_landmarks.landmark[sil].y),5))

          #leftEyeLower1
        for sil in leftEyeLower1:
            client.send_message("/leftEyeLower1."+str({sil})+".x", round(float(face_landmarks.landmark[sil].x),5))
            client.send_message("/leftEyeLower1."+str({sil})+".y", round(float(face_landmarks.landmark[sil].y),5))

          #leftEyeUpper2
        for sil in rightEyeLower2:
            client.send_message("/leftEyeUpper2."+str({sil})+".x", round(float(face_landmarks.landmark[sil].x),5))
            client.send_message("/leftEyeUpper2."+str({sil})+".y", round(float(face_landmarks.landmark[sil].y),5))

           #leftEyeLower2
        for sil in leftEyeLower2:
            client.send_message("/leftEyeLower2."+str({sil})+".x", round(float(face_landmarks.landmark[sil].x),5))
            client.send_message("/leftEyeLower2."+str({sil})+".y", round(float(face_landmarks.landmark[sil].y),5))

           #leftEyeLower3
        for sil in rightEyeLower2:
            client.send_message("/leftEyeLower3."+str({sil})+".x", round(float(face_landmarks.landmark[sil].x),5))
            client.send_message("/leftEyeLower3."+str({sil})+".y", round(float(face_landmarks.landmark[sil].y),5))
               
        
       
        cv2.imshow("Frame", frame)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

cap.release()
cv2.destroyAllWindows()