from math import pi

from graphics.core.scene_graph import Group

class CameraRig(Group):
    """A camera that can look up and down while attached to a movable base."""
    def __init__(self, camera, inverted=True, units_per_second=1.5, 
                 degrees_per_second=60):
        super().__init__()

        # initialize and attach camera
        self._camera = camera
        self.add(self._camera)

        self._move_speed = units_per_second
        self._rotate_speed = degrees_per_second

        self.KEY_MOVE_FORWARD = 'w'
        self.KEY_MOVE_BACKWARD = 's'
        self.KEY_MOVE_LEFT = 'a'
        self.KEY_MOVE_RIGHT = 'd'
        self.KEY_MOVE_UP = 'e'
        self.KEY_MOVE_DOWN = 'q'
        self.KEY_TURN_LEFT = 'j'
        self.KEY_TURN_RIGHT = 'l'
        if inverted:
            self.KEY_LOOK_UP = 'k'
            self.KEY_LOOK_DOWN = 'i'
        else:
            self.KEY_LOOK_UP = 'i'
            self.KEY_LOOK_DOWN = 'k'

    def update(self, input, delta_time):
        move_amount = self._move_speed * delta_time
        rotate_amount = self._rotate_speed / 180 * pi * delta_time

        # moving the body in all directions
        if input.iskeypressed(self.KEY_MOVE_FORWARD):
            self.translate(0, 0, -move_amount)
        if input.iskeypressed(self.KEY_MOVE_BACKWARD):
            self.translate(0, 0,  move_amount)
        if input.iskeypressed(self.KEY_MOVE_LEFT):
            self.translate(-move_amount, 0, 0)
        if input.iskeypressed(self.KEY_MOVE_RIGHT):
            self.translate( move_amount, 0, 0)
        if input.iskeypressed(self.KEY_MOVE_UP):
            self.translate(0,  move_amount, 0)
        if input.iskeypressed(self.KEY_MOVE_DOWN):
            self.translate(0, -move_amount, 0)

        # turn the body left and right
        if input.iskeypressed(self.KEY_TURN_RIGHT):
            self.rotate_y(-rotate_amount)
        if input.iskeypressed(self.KEY_TURN_LEFT):
            self.rotate_y( rotate_amount)

        # turn the camera to look up or down
        if input.iskeypressed(self.KEY_LOOK_UP):
            self._camera.rotate_x( rotate_amount)
        if input.iskeypressed(self.KEY_LOOK_DOWN):
            self._camera.rotate_x(-rotate_amount)