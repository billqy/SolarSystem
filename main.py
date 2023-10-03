import pygame
import numpy
import math
import random
from scipy.interpolate import interp1d

# F = G(m1)(m2) / r^2   (r = distance between centers of mass)
# a = F/m (acceleration is the rate of change of velocity)

pygame.init()
XMAX = 700
YMAX = 700
screen = pygame.display.set_mode((XMAX, YMAX))

clock = pygame.time.Clock()
dt = 0
running = True

GRAVITY = 0.001   # 6.67 * math.pow(10, -11)
Bodies = []
Paths = []
path_creation_interval = 30  # 30 frames represents 0.5 seconds passed @60FPS.
path_max_lifetime = 180  # 180 frames represents 3 seconds passed @60FPS.


class Body:
    def __init__(self, xpos, ypos, radius, color, mass, velo):
        self.xpos = xpos
        self.ypos = ypos
        self.radius = radius
        self.color = color

        self.mass = mass
        self.velo = velo
        self.accel = [0, 0]

        self.path_frame_count = 0

    def update_values(self):
        self.path_frame_count += 1
        self.xpos += self.velo[0]
        self.ypos += self.velo[1]

        for other in Bodies:
            if other != self:
                xr = abs(other.xpos - self.xpos)
                yr = abs(other.ypos - self.ypos)
                gmm = GRAVITY * self.mass * other.mass
                constant = 1
                # r = math.sqrt(math.pow(xr, 2) + math.pow(yr, 2))
                x_force_applied = gmm / math.sqrt(math.pow(xr, 2) + math.pow(constant, 2))
                y_force_applied = gmm / math.sqrt(math.pow(yr, 2) + math.pow(constant, 2))

                if other.xpos > self.xpos:
                    self.accel[0] += (x_force_applied * dt) / self.mass
                elif other.xpos < self.xpos > 0:
                    self.accel[0] -= (x_force_applied * dt) / self.mass

                if other.ypos > self.ypos:
                    self.accel[1] += (y_force_applied * dt) / self.mass
                elif other.ypos < self.ypos:
                    self.accel[1] -= (y_force_applied * dt) / self.mass

        print(self.velo)
        self.velo[0] += self.accel[0] * dt
        self.velo[1] += self.accel[1] * dt

    def reset_path_count(self):
        self.path_frame_count = 0


class Path:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.radius = 2
        self.lifetime = path_max_lifetime

    def determine_color(self):
        default = 255
        adjusted = interp1d([0, path_max_lifetime], [0, default])
        new_val = adjusted(self.lifetime)
        new_color = (new_val, new_val, new_val)
        return new_color


for i in range(50):
    rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    velo = [random.randint(-1, 1) * random.random(), random.randint(-1, 1) * random.random()]
    mass = random.randint(30, 70)
    radius = mass/10
    planet = Body(random.randint(100, XMAX-100), random.randint(100, YMAX-100), radius, rgb, mass, velo)
    Bodies.append(planet)

# planet = Body(XMAX/2, YMAX/2, 5, "yellow1", 60, [0, 0])
# Bodies.append(planet)
# planet2 = Body((XMAX/2) - 100, (YMAX/2) - 10, 5, "turquoise4", 60, [0, -0.5])
# Bodies.append(planet2)
# planet3 = Body((XMAX/2) + 100, (YMAX/2) + 10, 5, "aquamarine", 60, [0, 0.5])
# Bodies.append(planet3)
# planet4 = Body(random.randint(100, XMAX-100), random.randint(100, YMAX-100), 5, "deeppink3", 60, [-1, 0])
# Bodies.append(planet4)
# planet5 = Body(random.randint(100, XMAX-100), random.randint(100, YMAX-100), 5, "aquamarine", 60, [1, 0])
# Bodies.append(planet5)

while running:
    # -- user events --
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")  # wipe away last frame

    # -- update frame --
    for path in Paths:
        path.lifetime -= 1
        if path.lifetime <= 0:
            Paths.remove(path)

        # draw paths
        pygame.draw.circle(screen, path.determine_color(), (path.xpos, path.ypos), path.radius)

    for body in Bodies:
        # update bodies
        body.update_values()
        # print(body.velo[0], body.velo[1])

        # create new paths, if applicable
        if body.path_frame_count >= path_creation_interval:
            newPath = Path(body.xpos, body.ypos)
            Paths.append(newPath)
            body.reset_path_count()

        # draw bodies
        pygame.draw.circle(screen, body.color, (body.xpos, body.ypos), body.radius)

    pygame.display.flip()  # display updates
    dt = clock.tick(60) / 1000

pygame.quit()
