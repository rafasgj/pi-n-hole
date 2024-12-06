"""Implement a Touch Button for TTP223 module."""

import time

import gpiod
from gpiod.line import Direction, Value


class TouchButton:
    """Touch button abstraction."""

    def __init__(self, pin):
        """Initialize object."""
        self.touch_pin = pin
        for chipnum in range(10):
            device = f"/dev/gpiochip{chipnum}"
            if gpiod.is_gpiochip_device(device):
                break
        else:
            raise RuntimeError("Could not find gpio chip.")
        self.device = device

    def event_loop(
        self, pressed=lambda: None, released=lambda: None, down=lambda: None
    ):
        """Start button event loop."""
        try:
            previous = Value.INACTIVE
            with gpiod.request_lines(
                self.device,
                consumer="touch button",
                config={
                    self.touch_pin: gpiod.LineSettings(
                        direction=Direction.INPUT
                    )
                },
            ) as touch_line:
                while True:
                    status = touch_line.get_value(self.touch_pin)
                    if status != previous:
                        if status == Value.ACTIVE:
                            pressed()
                        else:
                            released()
                    if status == Value.ACTIVE:
                        down()
                    previous = status
                    time.sleep(0.0005)  # 2000 Hz
        except Exception as ex:  # pylint: disable=broad-except
            print(f"Error: {ex}")


if __name__ == "__main__":
    TouchButton(23).event_loop(released=lambda: print("Released"))
