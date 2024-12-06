"""Program entry-point"""

import os
import sys

from pinhole.camera import Camera
from pinhole.touch import TouchButton

__version__ = "0.1.0"


def main():
    if len(sys.argv) > 1:
        IMAGEDIR = sys.argv[1]
    else:
        IMAGEDIR = os.path.join(os.environ.get("HOME", ""), "Pictures")

    os.makedirs(IMAGEDIR, exist_ok=True)

    for num in range(1, 10000):
        filename = f"IMG_{num:04d}.jpg"
        if not os.path.isfile(os.path.join(IMAGEDIR, filename)):
            break

    pinhole = Camera(target_dir=IMAGEDIR, start_counter=num)
    try:
        TouchButton(23).event_loop(released=pinhole.shot)
    except KeyboardInterrupt:  # pylint: disable=broad-except
        pass  # We know we need to shutdown.
    pinhole.shutdown()


if __name__ == "__main__":
    main()
