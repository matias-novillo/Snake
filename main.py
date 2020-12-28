import pygame


def main():
    pygame.init()

    size = (1280, 720)
    background = 50, 50, 50

    # Create world
    screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE)
    world_rect = pygame.Rect(0, 0, size[0] * 2, size[1] * 2)
    screen_rect = screen.get_rect()

    # Create player
    explosion_atlas = Atlas("Assets/Explosions/explosion1.png", (256, 256))
    ship_image = pygame.image.load("Assets/SpaceShooterRedux/PNG/playerShip2_blue.png").convert()
    player = Ship(ship_image, explosion_atlas, 0.5)
    player.set_pos(pygame.Vector2(screen_rect.width / 2.0, screen_rect.height / 2.0))
    player.set_scale(0.8)
    player.transform()
    linear_velocity = 200.0
    angular_velocity = 1.5

    # Create a turret
    turret_image = pygame.image.load("Assets/SpaceShooterRedux/PNG/Parts/turretBase_big.png").convert()
    projectile_image = pygame.image.load("Assets/SpaceShooterRedux/PNG/Lasers/laserRed06.png").convert()
    turret = Turret(turret_image, projectile_image)
    turret.set_pos(pygame.Vector2(screen_rect.width * 0.75, screen_rect.height * 0.75))
    turret.transform()
    turret.set_target(player)

    # Add player and turret to group of game objects
    game_objects = CameraAwareGroup(player, world_rect, screen_rect, True)
    game_objects.add(turret)
    game_objects.move_to_back(turret)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Exit
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Handle input for movement
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_s]:
            player.set_heading(player.heading + angular_velocity)
        if pressed_keys[pygame.K_f]:
            player.set_heading(player.heading - angular_velocity)
        if pressed_keys[pygame.K_e]:
            player.set_velocity(linear_velocity)
        if pressed_keys[pygame.K_d]:
            player.set_velocity(player.velocity * 0.8)

        # Update groups
        game_objects.update(clock.get_time())

        # Render
        screen.fill(background)
        game_objects.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    from sys import path
    path.append(r"./GameEngine")
    from ship import Ship
    from camera_aware_group import CameraAwareGroup
    from turret import Turret
    from atlas import Atlas

    main()
