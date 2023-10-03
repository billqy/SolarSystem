import pygame
import math
import random
from scipy.interpolate import interp1d
from win32gui import SetWindowPos

# F = G(m1)(m2) / r^2   (r = distance between centers of mass)
# a = F/m (acceleration is the rate of change of velocity)

GRAVITY = 0.1
Bodies = []
Paths = []
path_creation_interval = 5  # 5 frames represents 0.1 seconds passed @60FPS.
path_max_lifetime = 180  # 120 frames represents 2 seconds passed @60FPS.
sim_choice = int(input("Enter 1 or 2 to simulate Solar System(1) or or 3-Body(2) or Random(3): "))
if sim_choice == 3: object_count = int(input("Enter number of objects to simulate: "))

pygame.init()
XMAX = 800
YMAX = 700
screen = pygame.display.set_mode((XMAX, YMAX))
SetWindowPos(pygame.display.get_wm_info()['window'], -1, 0, 0, 0, 0, 1)
clock = pygame.time.Clock()
dt = 0
running = True

class Body:
    def __init__(self, xpos, ypos, radius, color, mass, velo):
        self.xpos = xpos
        self.ypos = ypos
        self.radius = radius
        self.color = color

        self.mass = mass
        self.velo = velo

        self.path_frame_count = 0

    def update_values(self):
        self.path_frame_count += 1

        for other in Bodies:
            if other != self:
                xr = abs(other.xpos - self.xpos)
                yr = abs(other.ypos - self.ypos)
                gmm = GRAVITY * self.mass * other.mass
                constant = 5
                r = math.sqrt(xr**2 + yr**2)
                line_force = gmm / math.sqrt(r**2 + constant**2)
                theta = math.atan2(yr, xr)
                x_force_applied = math.cos(theta) * line_force
                y_force_applied = math.sin(theta) * line_force

                if other.xpos > self.xpos:
                    self.velo[0] += (x_force_applied * dt) / self.mass
                elif other.xpos < self.xpos > 0:
                    self.velo[0] -= (x_force_applied * dt) / self.mass

                if other.ypos > self.ypos:
                    self.velo[1] += (y_force_applied * dt) / self.mass
                elif other.ypos < self.ypos:
                    self.velo[1] -= (y_force_applied * dt) / self.mass

        self.xpos += self.velo[0] * dt
        self.ypos += self.velo[1] * dt

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


if sim_choice == 3:  # User selected random simulation
    for i in range(object_count):
        rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        velo = [random.randint(-100, 100) * random.random(), random.randint(-100, 100) * random.random()]
        mass = random.randint(100, 10000)
        radius = 5
        planet = Body(random.randint(100, XMAX-100), random.randint(100, YMAX-100), radius, rgb, mass, velo)
        Bodies.append(planet)
elif sim_choice == 2:
    rgb1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    rgb2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    rgb3 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    mass = 100_000
    radius = 5
    planet1 = Body(XMAX/2, YMAX/2, radius, rgb1, mass, [0, 0])
    Bodies.append(planet1)
    planet2 = Body(XMAX/2 + 150, YMAX/2, radius, rgb2, mass, [0, 100])
    Bodies.append(planet2)
    planet3 = Body(XMAX/2 - 150, YMAX/2, radius, rgb3, mass, [0, -100])
    Bodies.append(planet3)
else:
    sun = Body(XMAX/2, YMAX/2, 10, "yellow1", 100_000, [0, 0])
    Bodies.append(sun)
    mercury = Body((XMAX/2) - 50, YMAX/2, 2, "antiquewhite4", 20, [0, -100])
    Bodies.append(mercury)
    venus = Body((XMAX/2) - 100, YMAX/2, 4, "chocolate", 40, [0, -100])
    Bodies.append(venus)
    earth = Body((XMAX/2) - 150, YMAX/2, 5, "cornflowerblue", 50, [0, -100])
    Bodies.append(earth)
    mars = Body((XMAX/2) - 200, YMAX/2, 3, "coral3", 30, [0, -100])
    Bodies.append(mars)
    jupiter = Body((XMAX/2) - 250, YMAX/2, 8, "cornsilk2", 80, [0, -100])
    Bodies.append(jupiter)
    saturn = Body((XMAX/2) - 300, YMAX/2, 7, "darkgoldenrod2", 70, [0, -100])
    Bodies.append(saturn)
    uranus = Body((XMAX/2) - 350, YMAX/2, 6, "cyan3", 60, [0, -100])
    Bodies.append(uranus)
    neptune = Body((XMAX/2) - 400, YMAX/2, 6, "deepskyblue4", 60, [0, -100])
    Bodies.append(neptune)


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
