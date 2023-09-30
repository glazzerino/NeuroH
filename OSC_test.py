import sys
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio
import cv2
import mediapipe as mp
import numpy as np
from pythonosc import udp_client
import argparse
import time

# from osc_observer import OSCServer
from typing import List, Any

address_list = ["/Interfaz*"]
address_handler_list = [None]

silhouette = [
    10,
    338,
    297,
    332,
    284,
    251,
    389,
    356,
    454,
    323,
    361,
    288,
    397,
    365,
    379,
    378,
    400,
    377,
    152,
    148,
    176,
    149,
    150,
    136,
    172,
    58,
    132,
    93,
    234,
    127,
    162,
    21,
    54,
    103,
    67,
    109,
]

lipsUpperInner = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308]
lipsLowerInner = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]

rightEyeUpper0 = [246, 161, 160, 159, 158, 157, 173]
rightEyeLower0 = [33, 7, 163, 144, 145, 153, 154, 155, 133]
rightEyeUpper1 = [247, 30, 29, 27, 28, 56, 190]
rightEyeLower1 = [130, 25, 110, 24, 23, 22, 26, 112, 243]
rightEyeUpper2 = [113, 225, 224, 223, 222, 221, 189]
rightEyeLower2 = [226, 31, 228, 229, 230, 231, 232, 233, 244]
rightEyeLower3 = [143, 111, 117, 118, 119, 120, 121, 128, 245]

leftEyeUpper0 = [466, 388, 387, 386, 385, 384, 398]
leftEyeLower0 = [263, 249, 390, 373, 374, 380, 381, 382, 362]
leftEyeUpper1 = [467, 260, 259, 257, 258, 286, 414]
leftEyeLower1 = [359, 255, 339, 254, 253, 252, 256, 341, 463]
leftEyeUpper2 = [342, 445, 444, 443, 442, 441, 413]
leftEyeLower2 = [446, 261, 448, 449, 450, 451, 452, 453, 464]
leftEyeLower3 = [372, 340, 346, 347, 348, 349, 350, 357, 465]

dispatcher = Dispatcher()


def save_data_handler(address: str, *args: List[Any]) -> None:
    global save_data_flag
    save_data_flag = True
    print(f"Received save data signal with address {address} and arguments {args}")


dispatcher.map("/Interfaz*", print)
dispatcher.map("/Interfaz/save", print)
dispatcher.map("/Interfaz/subject", print)
dispatcher.map("/Interfaz/scene", print)
dispatcher.map("/Interfaz/year", print)

dispatcher.map("/Interfaz/save_data", save_data_handler)

ip = "0.0.0.0"
port = 5005

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


async def loop():
    with mp_face_mesh.FaceMesh(
        static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5
    ) as face_mesh:
        while True:
            ret, frame = cap.read()
            if ret == False:
                break
            frame = cv2.flip(frame, 1)
            frameHeight, frameWidth, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)

            if results.multi_face_landmarks is not None:
                for faceLandmarks in results.multi_face_landmarks:
                    for landmark in faceLandmarks.landmark:
                        x, y = int(landmark.x * frameWidth), int(
                            landmark.y * frameHeight
                        )
                        cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

            cv2.imshow("Frame", frame)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
            await asyncio.sleep(0.01)
    cap.release()
    cv2.destroyAllWindows()


class OSCServer:
    def __init__(self, ip: str, port: int):
        self.save_data_flag = False
        self.ip = ip
        self.port = port
        self.dispatcher = Dispatcher()
        self.data_store = {}

        self.dispatcher.map("/Interfaz/save_data", self.save_data_handler)
        self.dispatcher.map("/Interfaz/*", self.general_handler)
        dispatcher.map("/Interfaz*", self.general_handler)
        dispatcher.map("/Interfaz/save", self.general_handler)
        dispatcher.map("/Interfaz/subject", self.general_handler)
        dispatcher.map("/Interfaz/scene", self.general_handler)
        dispatcher.map("/Interfaz/year", self.general_handler)

    def save_data_handler(self, address: str, *args: List[Any]) -> None:
        self.save_data_flag = not self.save_data_flag
        print(f"Received save data command from {address}")

    def general_handler(self, address: str, *args: List[Any]) -> None:
        self.data_store[address] = args
        print(f"Received data with address {address} and arguments {args}")

    async def loop(self):
        with mp_face_mesh.FaceMesh(
            static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5
        ) as face_mesh:
            while True:
                if self.save_data_flag:
                    # Access and save the data from the data_store attribute
                    self.save_data()
                ret, frame = cap.read()
                if ret == False:
                    break
                frame = cv2.flip(frame, 1)
                frameHeight, frameWidth, _ = frame.shape
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(frame_rgb)

                if results.multi_face_landmarks is not None:
                    for faceLandmarks in results.multi_face_landmarks:
                        for landmark in faceLandmarks.landmark:
                            x, y = int(landmark.x * frameWidth), int(
                                landmark.y * frameHeight
                            )
                            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

                cv2.imshow("Frame", frame)
                k = cv2.waitKey(1) & 0xFF
                if k == 27:
                    break
                await asyncio.sleep(0.01)
        cap.release()
        cv2.destroyAllWindows()

    def save_data(self):
        print(f"Saving data: {self.data_store}")

    async def init_main(self):
        server = AsyncIOOSCUDPServer(
            (self.ip, self.port), self.dispatcher, asyncio.get_event_loop())
        (
            transport,
            protocol,
        ) = (
            await server.create_serve_endpoint()
        )  # Create datagram endpoint and start serving
        await self.loop()  # Enter main loop of program
        transport.close()  # Clean up serve endpoint


# Usage
osc_server = OSCServer(ip="0.0.0.0", port=5005)
asyncio.run(osc_server.init_main())
