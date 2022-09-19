import os
from Camera import Camera
from Utilities import FrameUtilities
from FaceRecognizer import FaceRecognizer
from DetectionRecorder import FacesDictionary, Actions


class FaceDetector:
    def __init__(self, images_path, cameras_indexes: set, window_name="Face Detector"):
        cameras_indexes = set(cameras_indexes)
        self.face_recognizer = FaceRecognizer(images_path)
        self.face_recognizer.load_encoding_images()
        self.cameras = [Camera(camera_index) for camera_index in cameras_indexes]
        self.window_name = window_name
        self.colors = {"red": (0, 0, 255), "green": (0, 255, 0)}
        self.current_color = self.colors["red"]
        self.detected_faces = FacesDictionary()
        self.number_of_minutes_to_wait = 0
        self.number_of_seconds_to_wait = 10
        self.stopped = False

    def get_absolute_path(self, relative_path):
        return os.path.abspath(os.path.join(self.face_recognizer.abs_path, relative_path))

    def detection_loop(self):
        if self.cameras:
            while not self.stopped:
                for camera in self.cameras:
                    if not camera.stopped:
                        self.detect_faces(camera)
                if FrameUtilities.is_exit_key_pressed():
                    self.stop()
        else:
            print("No cameras are available")
            self.stop()

    def detect_faces(self, camera):
        is_camera_online, frame = camera.read_frame()
        window_name = self.form_window_name(camera.index)
        FrameUtilities.create_window(window_name)

        if is_camera_online:
            face_locations, face_names = self.face_recognizer.detect_known_faces(frame)
            for face_loc, name in zip(face_locations, face_names):
                self.current_color = self.colors["red"]

                if name != "Unknown":
                    self.detection_action(name)

                FrameUtilities.draw_text(frame, name, face_loc, self.current_color, font_scale=0.7, thickness=2)
                FrameUtilities.draw_rectangle(frame, face_loc, self.current_color, thickness=2)
            FrameUtilities.show_frame(window_name, frame)
        else:
            print("Camera {} is not reachable".format(camera.index))
            camera.stop()
            if FrameUtilities.is_window_visible(window_name):
                FrameUtilities.destroy_window(window_name)
            if not any(camera.online for camera in self.cameras):
                self.stop()

    def detection_action(self, name):
        if not self.detected_faces.is_registered(name):
            Actions.register_face(name)
        elif Actions.is_exceeded_waiting_time(name, self.number_of_minutes_to_wait, self.number_of_seconds_to_wait):
            Actions.toggle_status(name)
        self.current_color = self.colors["green"]

    def add_face(self, image_path):
        self.face_recognizer.add_known_face_encoding(image_path)
        self.face_recognizer.add_known_face_name(image_path)
        self.start()

    def start(self):
        [camera.start() for camera in self.cameras]
        self.stopped = False
        self.detection_loop()

    def stop(self):
        self.stopped = True
        [camera.stop() for camera in self.cameras]

    def form_window_name(self, camera_index):
        return self.window_name + " - Camera: " + str(camera_index)

    def get_camera_obj(self, camera_index):
        return next(camera for camera in self.cameras if camera.index == camera_index)

    def retest_camera(self, camera_index):
        try:
            camera = self.get_camera_obj(camera_index)
            if camera.stopped:
                camera.set_camera_status()
                camera.stopped = False
        except StopIteration as ex:
            print("Camera {} is not found".format(camera_index))

    def add_camera(self, camera_index):
        try:
            camera = self.get_camera_obj(camera_index)
            print("Camera {} is already added".format(camera.index))
        except StopIteration as ex:
            new_camera = Camera(camera_index)
            new_camera.start()
            self.cameras.append(new_camera)

    def remove_camera(self, camera_index):
        try:
            camera = self.get_camera_obj(camera_index)
            camera.stop()
            self.cameras.remove(camera)
        except StopIteration as ex:
            print("Camera {} is not found".format(camera_index))

    def __del__(self):
        FrameUtilities.destroy_all_windows()
