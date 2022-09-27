from Camera import Camera


class CamerasControl:
    cameras = dict()

    def __init__(self, cameras_indexes: set):
        for camera_index in cameras_indexes:
            self.cameras[camera_index] = Camera(camera_index)

    def add_camera(self, camera_index):
        camera = self.cameras.get(camera_index, None)
        if camera is None:
            self.cameras[camera_index] = Camera(camera_index)
            self.cameras[camera_index].start()
        else:
            print("Camera {} is already added".format(camera.index))

    def retest_camera(self, camera_index):
        camera = self.cameras.get(camera_index, None)
        if camera is None:
            print("Camera {} is not found".format(camera_index))
        else:
            if self.cameras[camera_index].stopped():
                self.cameras[camera_index].start()

    def remove_camera(self, camera_index):
        camera = self.cameras.get(camera_index, None)
        if camera is None:
            print("Camera {} is not found".format(camera_index))
        else:
            self.cameras[camera_index].stop()
            self.cameras.pop(camera_index)

    def start(self):
        [camera.start() for camera in self.cameras.values()]

    def stop(self):
        [camera.stop() for camera in self.cameras.values()]

    def empty(self):
        return len(self.cameras) == 0
