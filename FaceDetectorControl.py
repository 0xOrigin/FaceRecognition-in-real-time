from CamerasControl import CamerasControl
from FaceDetector import FaceDetector
from FaceRecognizer import FaceRecognizer
from Utilities import FrameUtilities


class FaceDetectorControl:

    def __init__(self, images_path, cameras_indexes: set, window_name="Face Detector"):
        self.face_recognizer = FaceRecognizer()
        self.face_recognizer.load_encoding_images(images_path)
        self.cameras_control = CamerasControl(set(cameras_indexes))
        self.window_name = window_name
        self.detectors = dict()
        self.hours_to_wait = 0
        self.minutes_to_wait = 0
        self.seconds_to_wait = 10

    def add_face(self, image_path):
        self.face_recognizer.add_face(image_path)

    def start_detector(self, camera):
        self.detectors[camera.index] = FaceDetector(camera, self.hours_to_wait, self.minutes_to_wait,
                                                    self.seconds_to_wait, self.window_name)
        self.detectors[camera.index].start()

    def start(self):
        self.cameras_control.start()
        for camera in self.cameras_control.cameras.values():
            self.start_detector(camera)
        self.display()

    def stop(self):
        [detector.stop() for detector in self.detectors.values()]
        self.cameras_control.stop()

    def display(self):
        while True:
            for detector in self.detectors.values():
                if not detector.camera.stopped():
                    FrameUtilities.show_frame(detector.window_name, detector.get_frame())
                    detector.set_display_status(True)
                elif detector.displayed():
                    FrameUtilities.destroy_window(detector.window_name)
                    detector.set_display_status(False)

                if FrameUtilities.is_exit_key_pressed():
                    FrameUtilities.destroy_window(detector.window_name)
                    detector.stop()

            if all(detector.stopped() for detector in self.detectors.values()):
                FrameUtilities.destroy_all_windows()
                break
