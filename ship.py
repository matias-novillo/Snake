from asteroid import Asteroid
from game_object import GameObject
from game_object_factory import GameObjectFactory
from health_bar import HealthBar
from mover import MoverVelocity
from projectile import Projectile


@GameObjectFactory.register("Ship")
class Ship(GameObject):
    """Space ship game object."""

    def __init__(self, image, projectile_type, fire_freq, mover, **kwargs):
        super().__init__(image, **kwargs)
        self.mover = mover
        self.projectile_type = projectile_type
        self.fire_freq = fire_freq
        self.time_since_last_fire = self.fire_freq

    def update(self, delta):
        """Updates the ship."""
        # Translate according to velocity
        self.pos, self.heading = self.mover.move(delta, self.pos, self.heading)
        # Now do the regular GameObject update
        super().update(delta)
        self.time_since_last_fire += delta

    def set_velocity(self, velocity):
        """Sets the ship's velocity."""
        self.mover.set_velocity(velocity)

    def fire(self):
        """Fires a Projectile at the target."""
        if self.time_since_last_fire > self.fire_freq and self.alive():
            projectile = GameObjectFactory.create(self.projectile_type)
            projectile.set_pos(self.pos)
            projectile.set_heading(self.heading)
            projectile.transform()

            group = self.groups()[0]
            group.add(projectile)

            self.time_since_last_fire = 0
