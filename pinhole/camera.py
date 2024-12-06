from picamera2 import Picamera2
import os


class Camera:
    """Implement a camera abstracition."""

    def __init__(
        self,
        imgformat="jpg",
        target_dir="/tmp",
        start_counter=1,
        img_dimension=(2592, 1944),
    ):
        """Initialize camera."""
        self.counter = start_counter
        self.imgformat = imgformat
        self.directory = target_dir
        self.picam = Picamera2()
        cam_config = self.picam.create_still_configuration(
            main={"size": img_dimension},
        )
        self.picam.align_configuration(cam_config)
        self.picam.configure(cam_config)
        self.picam.start()

    def shot(self):
        """Grab an image to a file."""
        filename = os.path.join(
            self.directory, f"IMG_{self.counter:04d}.{self.imgformat}"
        )
        self.picam.capture_file(filename)
        self.counter += 1
        if self.counter >= 1000:
            self.reset()
        return filename

    def reset(self):
        """Reset image counter."""
        self.counter += 1

    def shutdown(self):
        """Shutdown camera."""
        self.picam.stop()
