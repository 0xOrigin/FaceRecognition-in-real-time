import os
os.environ["OPENCV_LOG_LEVEL"] = "SILENT"
import cv2
from FaceRecognizer import FaceRecognizer


class FaceDetector:
    def __init__(self, images_path, camera_index=0):
        self.face_recognizer = FaceRecognizer(images_path)
        self.face_recognizer.load_encoding_images()
        self.cap = cv2.VideoCapture(camera_index)
        self.color_of_rectangle = (0, 0, 200)
        

    def get_absolute_path(self, relative_path):
        return os.path.abspath(os.path.join(self.face_recognizer.abs_path, relative_path))


    def detection_loop(self):
        while True:
            self.detect_faces()
            key = cv2.waitKey(1)
            if key == 27: # ESC
                break


    def detection_action(self, name):
        print("Hello {}".format(name))
        self.color_of_rectangle = (0, 200, 0)


    def detect_faces(self):
        ret, frame = self.cap.read()
        face_locations, face_names = self.face_recognizer.detect_known_faces(frame)

        for face_loc, name in zip(face_locations, face_names):

            top, left, right, bottom = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            self.color_of_rectangle = (0, 0, 200)
            if name != "Unknown":
                self.detection_action(name)
                
            cv2.putText(frame, name, (bottom, top - 10), cv2.FONT_HERSHEY_DUPLEX, 1, self.color_of_rectangle, 2)
            cv2.rectangle(frame, (bottom, top), (left, right), self.color_of_rectangle, 4)

        cv2.imshow("Face Detector", frame)


    def add_face(self, image_path):
        self.face_recognizer.add_known_face_encoding(image_path)
        self.face_recognizer.add_known_face_name(image_path)
        self.detection_loop()


    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()