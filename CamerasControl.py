from Camera import Camera


class CamerasControl:

    def __init__(self, cameras_indexes: set):
        self.cameras = [Camera(camera_index) for camera_index in cameras_indexes]

    def get_camera_obj(self, camera_index):
        return next(camera for camera in self.cameras if camera.index == camera_index)

    def add_camera(self, camera_index):
        try:
            camera = self.get_camera_obj(camera_index)
            print("Camera {} is already added".format(camera.index))
        except StopIteration as ex:
            new_camera = Camera(camera_index)
            new_camera.start()
            self.cameras.append(new_camera)

    def retest_camera(self, camera_index):
        try:
            camera = self.get_camera_obj(camera_index)
            if camera.stopped():
                camera.set_camera_status()
                camera.start()
        except StopIteration as ex:
            print("Camera {} is not found".format(camera_index))

    def remove_camera(self, camera_index):
        try:
            camera = self.get_camera_obj(camera_index)
            camera.stop()
            self.cameras.remove(camera)
        except StopIteration as ex:
            print("Camera {} is not found".format(camera_index))

    def start(self):
        [camera.start() for camera in self.cameras]

    def stop(self):
        [camera.stop() for camera in self.cameras]

    def empty(self):
        return len(self.cameras) == 0
