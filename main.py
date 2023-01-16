import math
import pygame
import random
import particle
import element
import numpy as np

WIDTH = 699
HEIGHT = 699
FPS = 30
PARTICLE_SIZE = 5
NUM_PARTICLES = 500
MAX_ATTRACT_DIST = 40
MIN_ATTRACT_DIST = 15
COOlING = 0.8
NUM_ELEMENTS = 5

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("particle")

def update(particles, element_handler):
    bx = int(WIDTH/MAX_ATTRACT_DIST)
    by = int(HEIGHT/MAX_ATTRACT_DIST)

    bins = updateBins(particles, bx, by)

    for i in range(bx):
        for j in range(by):
            for particle1 in bins[i][j]:
                for dx in {-1, 0, 1}:
                    for dy in {-1, 0, 1}:
                        try:
                            for particle2 in bins[i + dx][j + dy]:
                                # relative angle/distance between particle 1 and 2.
                                xdist = particle1.x - particle2.x
                                ydist = particle1.y - particle2.y

                                dist = math.hypot(xdist, ydist)

                                if dist <= MAX_ATTRACT_DIST:
                                    # adds interaction
                                    angle = math.atan2(ydist, xdist)
                                    angle2 = math.atan2(-ydist, -xdist)

                                    particle1.interactions += 1
                                    particle2.interactions += 1

                                    #force between 1 and 2, and 2 and 1
                                    force1 = np.interp(dist, element_handler.map[particle1.element-1][particle2.element-1][0], element_handler.map[particle1.element-1][particle2.element-1][1])
                                    force2 = np.interp(dist, element_handler.map[particle2.element-1][particle1.element-1][0], element_handler.map[particle2.element-1][particle1.element-1][1])

                                    #force1, force2 = 1, 1

                                    # add force
                                    particle1.xforce += math.cos(angle) * force1
                                    particle1.yforce += math.sin(angle) * force1
                                    particle2.xforce += math.cos(angle2) * force2
                                    particle2.yforce += math.sin(angle2) * force2
                        except IndexError:
                            continue

    # slows down all particles
    for particle in particles:
        if particle.xforce != 0:
            particle.xforce = particle.xforce * COOlING
        if particle.yforce != 0:
            particle.yforce = particle.yforce * COOlING

        particle.x += particle.xforce
        particle.y += particle.yforce

        #wrap
        if particle.x > WIDTH:
            particle.x = 0
        elif particle.x < 0:
            particle.x = WIDTH

        if particle.y > HEIGHT:
            particle.y = 0
        elif particle.y < 0:
            particle.y = HEIGHT

    return particles


def updateBins(particles,bxnum,bynum):
    bins = [0] * bxnum

    for x in range(len(bins)):
        bins[x] = [0] * bynum
        for y in range(len(bins[x])):
            bins[x][y] = []

    for particle in particles:
        bx = math.floor(particle.x / int(WIDTH/MAX_ATTRACT_DIST))
        by = math.floor(particle.y / int(WIDTH/MAX_ATTRACT_DIST))

        # edge case, bx = 10/by = 10
        if bx >= bxnum:
            bx = bxnum-1
        if by >= bynum:
            by = bynum-1

        bins[bx][by].append(particle)

    return bins


def draw(particles):
    WIN.fill((0, 0, 0))
    for particle in particles:
        pygame.draw.circle(WIN, particle.display_color(), (particle.x, particle.y), particle.size)
        particle.interactions = 0


element_handler = element.Element_Handler(NUM_ELEMENTS, MIN_ATTRACT_DIST, MAX_ATTRACT_DIST)
element_handler.setup()

particles = []
for i in range(NUM_PARTICLES):
    particles.append(particle.Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT), PARTICLE_SIZE, element_handler.assign_element()))
    particles[i].element_attributes(element_handler)

run = True
clock = pygame.time.Clock()

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    particles = update(particles, element_handler)
    draw(particles)

    pygame.display.update()
