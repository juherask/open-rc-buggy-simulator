# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 15:05:41 2016

@author: jussi
"""

import pygame
from math import sqrt, pi, cos, asin
import numpy as np

X = 0
Y = 1

BLACK = (20, 20, 20)
LIGHT_GREY = (200, 200, 200)
DARK_GREY = (150, 150, 150)
DASH_GREY = (100, 100, 100)
RED = (200, 100, 80)

SPRING_WIDTH_MULTIPLIER = 20 # bigger is smaller
SPRING_COILS = 8
GRAB_DISC_RADIUS = 10
SIZE = [640, 480]
HINGE_POSITION = [SIZE[X]/4, SIZE[Y]/2]

def calculate_shock_response(d, h, a, k, lim_up, lim_down, steps = 20):
    """get two sets of vectors, 
    
    d = horizontal distance from the hinge pin
    h = vertical distance from the hinge pin
        
    a = arm length 
    
    k shock lower mount position at the arm (ratio, eg. 0.5 = half way)

    the u, that is height of the wheel goes from     
    lim_down to lim_up, (u=0, the arm is level)
    """

    c = sqrt(d**2+h**2)

    datapoints_spring = []
    datapoints_damper = []
    
    prev_l = None
    for u in np.linspace(lim_down, lim_up, num=steps):
        #l = sqrt( c**2+a**2 * k**2-2 * a * c * k * sin(asin(d/c)*asin(u/a)) )
        l = sqrt( c**2+(a*k)**2 - 2 * a * k * c * cos(pi/2-asin(d/c)-asin(u/a)) )
        datapoints_spring.append( (l,u) )
        if prev_l:
            datapoints_damper.append( (abs(l-prev_l), u) )
        prev_l = l
    return datapoints_spring, datapoints_damper

def d(pos1, pos2):
    return sqrt( (pos1[X]-pos2[X])**2 + (pos1[Y]-pos2[Y])**2 )
    
def get_unit_vector(pos1, pos2):
    direction = [pos2[X]-pos1[X], pos2[Y]-pos1[Y]]
    nlen = sqrt(direction[X]**2+direction[Y]**2)
    return [direction[X]/nlen, direction[Y]/nlen]
    
def draw_shock(screen, from_pos, to_pos, nbr_coils):
    """ Draws a shock symbol that looks a bit like resistor
    symbol in electric circuits """
    
    direction = [from_pos[X]-to_pos[X], from_pos[Y]-to_pos[Y]]
    straight_edge_end_up = [
            from_pos[X]+direction[X]*-1/6.0,
            from_pos[Y]+direction[Y]*-1/6.0,
    ]
    straight_edge_end_down = [
            from_pos[X]+direction[X]*-5/6.0,
            from_pos[Y]+direction[Y]*-5/6.0,
    ]
    pygame.draw.line(screen, BLACK, from_pos, straight_edge_end_up, 4)
    pygame.draw.line(screen, BLACK, to_pos, straight_edge_end_down, 4)

    nlen = sqrt(direction[X]**2+direction[Y]**2)
    normal = [direction[Y]/max(0.001, nlen), -direction[X]/max(0.001, nlen)] #flipped, normalized
    
    coil_prev = straight_edge_end_up
    for i in range(nbr_coils):
        multiplier = (-1+2*(i%2)) * SIZE[Y]/SPRING_WIDTH_MULTIPLIER
        base = [straight_edge_end_up[X] + direction[X] * -4/6.0 * (i+0.5)/nbr_coils,
                  straight_edge_end_up[Y] + direction[Y] * -4/6.0 * (i+0.5)/nbr_coils ]
        coil_next = [base[X]+normal[X]*multiplier, base[Y]+normal[Y]*multiplier]
        pygame.draw.line(screen, BLACK, coil_prev, coil_next, 4)
        coil_prev = coil_next
        
    pygame.draw.line(screen, BLACK, coil_prev, straight_edge_end_down, 4)
 
 
 
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('RC buggy shock geometry toy')

## Init some geomtery variables ##
downtravel_limit = 3*SIZE[Y]/4
uptravel_limit = SIZE[Y]/4
wheel_position = [3*SIZE[X]/4, SIZE[Y]/2]
upper_shock_position = [int(1.5*SIZE[X]/4), SIZE[Y]/6]
lower_shock_position = [0.0, 0.0] #updates on each cycle
lower_shock_ratio = 0.5
arm_length = d(wheel_position, HINGE_POSITION)

## State variables for the main loop ##
drag = None
clock = pygame.time.Clock()
done = False
geometry_changed = False

## The main loop ##
while done == False:
    ## event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if d(event.pos, upper_shock_position)<GRAB_DISC_RADIUS:
                drag = upper_shock_position
            elif d(event.pos, lower_shock_position)<GRAB_DISC_RADIUS:
                drag = lower_shock_position
            elif d(event.pos, wheel_position)<GRAB_DISC_RADIUS:
                drag = wheel_position
            #TODO: up / downtravel limiters
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            drag = None
        elif event.type == pygame.MOUSEMOTION and drag!=None:
            if drag==wheel_position:
                direction = get_unit_vector(HINGE_POSITION, event.pos)
                new_pos = [
                    HINGE_POSITION[X]+int(direction[X]*arm_length),
                    HINGE_POSITION[Y]+int(direction[Y]*arm_length)]
                if new_pos[Y]>uptravel_limit and \
                   new_pos[Y]<downtravel_limit and \
                   new_pos[X]>HINGE_POSITION[X]:
                    # keep the ref to the list (therefore drag=event.pos is not used)
                    drag[X] = new_pos[X]
                    drag[Y] = new_pos[Y]
            elif drag==lower_shock_position:
                lower_shock_ratio = max(0.01, min(1.0, d(HINGE_POSITION, event.pos)/arm_length))
            else:
                # keep the ref to the list (therefore drag=event.pos is not used)
                drag[X] = event.pos[X]
                drag[Y] = event.pos[Y]            
            # TODO: up / downtravel
            
            geometry_changed = True
                
    # keep the ref to the list (therefore lower_shock_position is not overwritten)
    lower_shock_position[0] = int(HINGE_POSITION[X]+
        (HINGE_POSITION[X]-wheel_position[X])*-lower_shock_ratio)
    lower_shock_position[1] = int(HINGE_POSITION[Y]+
        (HINGE_POSITION[Y]-wheel_position[Y])*-lower_shock_ratio)
    
    # Valid area 
    screen.fill(LIGHT_GREY) 
    pygame.draw.rect(screen, DARK_GREY, (0,0, SIZE[X], uptravel_limit))
    pygame.draw.rect(screen, DARK_GREY, (0,downtravel_limit, SIZE[X], SIZE[Y]))
    # TODO: dashed lines    
    
    # Draw the shock and the arm, with discs that can be dragged
    draw_shock(screen, lower_shock_position, upper_shock_position, SPRING_COILS)
    pygame.draw.line(screen, BLACK, HINGE_POSITION, wheel_position, 4)
    pygame.draw.circle(screen, BLACK, HINGE_POSITION, GRAB_DISC_RADIUS)
    pygame.draw.circle(screen, RED, upper_shock_position, GRAB_DISC_RADIUS)
    pygame.draw.circle(screen, BLACK, upper_shock_position, GRAB_DISC_RADIUS, 2)
    pygame.draw.circle(screen, RED, lower_shock_position, GRAB_DISC_RADIUS)
    pygame.draw.circle(screen, BLACK, lower_shock_position, GRAB_DISC_RADIUS, 2)
    pygame.draw.circle(screen, RED, wheel_position, GRAB_DISC_RADIUS)
    pygame.draw.circle(screen, BLACK, wheel_position, GRAB_DISC_RADIUS, 2)
    
    if geometry_changed:
        shock_tower_support = [HINGE_POSITION[X]-upper_shock_position[X],
             HINGE_POSITION[Y]-upper_shock_position[Y]]        
        lim_up = HINGE_POSITION[Y]-uptravel_limit
        lim_down = HINGE_POSITION[Y]-downtravel_limit
        spring_response, dampener_response = calculate_shock_response(
            abs(shock_tower_support[X]), abs(shock_tower_support[Y]), #shock upper mount position
            arm_length, lower_shock_ratio, # shock lower mount position
            lim_up, lim_down, steps = 20)
        
        
        #plot_response( [0,0,100,100], spring_response,  "Spring response" )            
        #plot_response( [0,110,100,100], dampener_response, "Spring response" )
        
        geometry_changed= False
    # display what’s drawn. this might change.
    pygame.display.update()
    # run at 20 fps
    clock.tick(20)
 
# close the window and quit
pygame.quit()
