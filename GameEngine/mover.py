import pygame

from game_object_factory import GameObjectBase
from game_object_factory import GameObjectFactory


class Mover(GameObjectBase):
    """Base class for game objects that move."""

    def move(self, delta, pos, heading):
        pass


@GameObjectFactory.register("MoverVelocity")
class MoverVelocity(Mover):
    """Velocity-based mover."""

    def __init__(self, velocity_decay_factor, velocity, max_velocity, angular_velocity):
        self.velocity = velocity
        self.velocity_decay_factor = velocity_decay_factor
        self.max_velocity = max_velocity
        self.angular_velocity = angular_velocity

    def move(self, delta, pos, heading):
        """Computes movement from the given parameters."""
        delta_pos = pygame.math.Vector2()
        delta_pos.from_polar((delta / -1000.0 * self.velocity, 90.0 - heading))
        self.velocity = self.velocity * self.velocity_decay_factor
        return (pos + delta_pos, heading)

    def set_velocity(self, velocity):
        self.velocity = velocity
