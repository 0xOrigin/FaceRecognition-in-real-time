from threading import Thread
from FaceRecognizer import FaceRecognizer
from Utilities import FrameUtilities
from DetectionRecorder import FacesDictionary, Actions


class FaceDetector:
    colors = {"red": (0, 0, 255), "green": (0, 255, 0)}

    def __init__(self, camera, hours_to_wait=0, minutes_to_wait=0, seconds_to_wait=0, window_name="Face Detector"):
        self.face_recognizer = FaceRecognizer()
        self.camera = camera
        self.window_name = self.form_window_name(window_name, self.camera.index)
        self.frame = camera.frame
        self.thread = Thread(target=self.detection_loop, args=())
        self.detected_faces = FacesDictionary()
        self.hours_to_wait = hours_to_wait
        self.minutes_to_wait = minutes_to_wait
        self.seconds_to_wait = seconds_to_wait
        self.__stopped = True
        self.__displayed = False

    def detection_loop(self):
        while not self.stopped() and not self.camera.stopped():
            self.detect_faces()

    def detect_faces(self):
        is_camera_online, frame = self.camera.read_frame()

        if is_camera_online and frame is not None:
            face_locations, face_names = self.face_recognizer.detect_known_faces(frame)
            for face_loc, name in zip(face_locations, face_names):
                current_color = self.colors["red"]

                if name != self.face_recognizer.unknown_face_name:
                    self.detection_action(name)
                    current_color = self.colors["green"]

                FrameUtilities.draw_text(frame, name, face_loc, current_color, font_scale=0.7, thickness=2)
                FrameUtilities.draw_rectangle(frame, face_loc, current_color, thickness=2)

            self.frame = frame
        else:
            print("Camera {} is not reachable".format(self.camera.index))
            self.stop()

    def detection_action(self, name):
        if not self.detected_faces.is_registered(name):
            Actions.register_face(name, self.camera.index)
        elif Actions.is_exceeded_waiting_time(name, self.hours_to_wait, self.minutes_to_wait, self.seconds_to_wait):
            Actions.toggle_status(name, self.camera.index)

    def start(self):
        if self.stopped():
            self.toggle_state()
            self.thread = Thread(target=self.detection_loop, args=())
            self.thread.start()
            self.set_display_status(False)
            print("Thread {} camera {} started".format(self.thread.name, self.camera.index))

    def stop(self):
        if not self.stopped():
            self.toggle_state()
            self.camera.stop()
            print("Thread {} camera {} stopped".format(self.thread.name, self.camera.index))

    def get_frame(self):
        return self.frame

    def toggle_state(self):
        self.__stopped = not self.__stopped

    def stopped(self):
        return self.__stopped

    def displayed(self):
        return self.__displayed

    def set_display_status(self, value):
        self.__displayed = value

    @staticmethod
    def form_window_name(window_name, camera_index):
        return window_name + " - Camera: " + str(camera_index)
