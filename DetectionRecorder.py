from threading import Lock
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


@dataclass
class Status(Enum):
    Present = 0
    Departed = 1


class FacesDictionary:
    __instance = None
    __acquire_lock = Lock()
    dictionary = {}

    def __new__(cls, *args, **kwargs):
        with FacesDictionary.__acquire_lock:
            if cls.__instance is None:
                cls.__instance = super(FacesDictionary, cls).__new__(cls)
        return cls.__instance

    def add(self, face_name, time: datetime):
        self.dictionary[face_name] = (Status.Present.name, time)

    def toggle_status(self, face_name, time: datetime):
        self.dictionary[face_name] = ((Status.Present.name, time) if self.dictionary[face_name][0] == Status.Departed.name else (Status.Departed.name, time))

    def is_registered(self, face_name):
        return face_name in self.dictionary


class Actions:

    @staticmethod
    def register_face(face_name):
        FacesDictionary().add(face_name, datetime.now())
        print("Welcome: {}".format(face_name))

    @staticmethod
    def is_exceeded_waiting_time(face_name, minutes, seconds):
        return datetime.now() - FacesDictionary().dictionary[face_name][1] >= timedelta(minutes, seconds)

    @staticmethod
    def toggle_status(face_name):
        FacesDictionary().toggle_status(face_name, datetime.now())
        if FacesDictionary().dictionary[face_name][0] == Status.Present.name:
            print("Welcome: {} {}".format(face_name, datetime.now()))
        else:
            print("Goodbye: {} {}".format(face_name, datetime.now()))
