#!/usr/bin/python
"""
This file is part of the 'Physics' Project
Physics is a 2D Physics Playground for Kids (supporting Box2D2)
Physics Copyright (C) 2008, Alex Levenson, Brian Jordan
Elements Copyright (C) 2008, The Elements Team, <elements@linuxuser.at>

Wiki:   http://wiki.laptop.org/wiki/Physics
IRC:    #olpc-physics on irc.freenode.org

Code:   http://dev.laptop.org/git?p=activities/physics
        git clone git://dev.laptop.org/activities/physics

License:  GPLv3 http://gplv3.fsf.org/
"""

import sys
import math
import pygame
from pygame.locals import *
from pygame.color import *
import elements
from elements import Elements
import tools
from helpers import *
import sys
sys.path.insert(0, "elements")
import box2d
from gi.repository import Gtk

class XOlympicsGame:
    def __init__(self):
        pass

    def run(self):
        self.rightscore = self.leftscore = 0
        self.forcespeed = 75
        self.jumpforce = 20
        self.leftDPress = False
        self.rightDPress = False
        self.leftLPress = False
        self.leftRPress = False
        self.leftJump = False
        self.rightLPress = False
        self.rightRPress = False
        self.rightJump = False
        self.updateList = []

        pygame.init()
        self.screen = pygame.display.get_surface()
        # get everything set up
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24) # font object
        self.joystickobject = None 
        self.debug = True
        # kids laptop
        # create the name --> instance map for components
        self.toolList = {}
        for c in tools.allTools:
            self.toolList[c.name] = c(self)
        #self.currentTool = self.toolList[tools.allTools[0].name]
       # no tools, eh? 
        # set up the world (instance of Elements)
        self.world = elements.Elements(self.screen.get_size())
        self.world.renderer.set_surface(self.screen)
        # set up static environment
        self.world.set_color((0, 255, 0))  
        self.world.add.ground()
        self.ball = self.world.add.ball((600, 0), 50)
        # ADD LEFT BORDER
        self.world.set_color((255, 0, 0))  
        self.world.add.rect((0,-20), 25, 900, dynamic=False, density=1.0, restitution=0.16, friction=0.5)   
        self.leftplayer = self.world.add.poly(( 264.0, 81.0 ),  ((-109.9405166666667, -64.244016666666653), (110.60718333333335, -63.089316666666605), (-0.66666666666668561, 127.33333333333337)) , dynamic=True, density=1.0, restitution=0.16, friction=0.5, screenCoord=False)
        # ADD RIGHT BORDER
        self.world.set_color((0, 0, 255))  
        self.world.add.rect((1180,-20), 25, 900, dynamic=False, density=1.0, restitution=0.16, friction=0.5)   
        self.rightplayer = self.world.add.poly(( 885.0, 78.0 ),  [(108.94051666666667, -65.976066666666611), (2.6666666666666288, 127.33333333333337), (-111.60718333333341, -61.357266666666646)] , dynamic=True, density=1.0, restitution=0.16, friction=0.5, screenCoord=False)
        # we're getting 2 grounds - grey and green. wtf.  
#	self.leftplayer = 
#        self.world.add.poly((900,800),((-300,300), (300, 300), (300, -300)), dynamic=True, density=1.0, restitution=0.16, friction=0.5)
        # self.leftplayer = self.world.add.rect((500,0), 25, 90, dynamic=True, density=1.0, restitution=0.16, friction=0.5)
        self.leftplayer.linearDamping = 0.07
        self.test = self.leftplayer.worldCenter 
#        self.rightplayer = self.world.add.rect((900,775), 25, 90, dynamic=True, density=1.0, restitution=0.16, friction=0.5)
        # hack fix: set_color early!

        self.running = True    
        while self.running:
            while Gtk.events_pending():
                Gtk.main_iteration()

            for event in pygame.event.get():
                if (event.type == KEYDOWN and (event.key == K_a or event.key == K_KP4)):
                    self.leftLPress = True
                if (event.type == KEYUP and (event.key == K_a or event.key == K_KP4)):
                    self.leftLPress = False
                if (event.type == KEYDOWN and (event.key == K_s or event.key == K_KP2)):
                    self.leftDPress = True
                if (event.type == KEYUP and (event.key == K_s or event.key == K_KP2)):
                    self.leftDPress = False
                if (event.type == KEYDOWN and (event.key == K_d or event.key == K_KP6)):
                    self.leftRPress = True
                if (event.type == KEYUP and (event.key == K_d or event.key == K_KP6)):
                    self.leftRPress = False
                if (event.type == KEYDOWN and (event.key == K_w or event.key == K_KP8)):
                    self.leftJump = True
                if (event.type == KEYUP and (event.key == K_w or event.key == K_KP8)):
                    self.leftJump = False
                if (event.type == KEYDOWN and (event.key == K_LEFT or event.key == K_KP7)):
                    self.rightLPress = True
                if (event.type == KEYUP and (event.key == K_LEFT or event.key == K_KP7)):
                    self.rightLPress = False
                if (event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_KP1)):
                    self.rightRPress = True
                if (event.type == KEYUP and (event.key == K_RIGHT or event.key == K_KP1)):
                    self.rightRPress = False
                if (event.type == KEYDOWN and (event.key == K_UP or event.key == K_KP9)):
                    self.rightJump = True
                if (event.type == KEYUP and (event.key == K_UP or event.key == K_KP9)):
                    self.rightJump = False            
                if (event.type == KEYDOWN and (event.key == K_DOWN or event.key == K_KP3)):
                    self.rightDPress = True
                if (event.type == KEYUP and (event.key == K_DOWN or event.key == K_KP3)):
                    self.rightDPress = False             
#            for event in pygame.event.get():
                #self.currentTool.handleEvents(event)
            if self.leftLPress:
                self.leftplayer.ApplyForce(box2d.b2Vec2(-self.forcespeed,0), self.leftplayer.worldCenter, True)
            if self.leftRPress:
                self.leftplayer.ApplyForce(box2d.b2Vec2(self.forcespeed,0), self.leftplayer.worldCenter, True)
            if self.leftJump:
                if self.leftplayer.worldCenter.y < 0.80:
                    self.leftplayer.ApplyLinearImpulse(box2d.b2Vec2(0,self.jumpforce), self.leftplayer.worldCenter, True)
            if self.rightLPress:
                self.rightplayer.ApplyForce(box2d.b2Vec2(-self.forcespeed,0), self.rightplayer.worldCenter, True)
            if self.rightRPress:
                self.rightplayer.ApplyForce(box2d.b2Vec2(self.forcespeed,0), self.rightplayer.worldCenter, True)
            if self.rightDPress:
	            self.rightplayer.ApplyLinearImpulse(box2d.b2Vec2(0,-self.jumpforce), self.rightplayer.worldCenter, True)
            if self.rightJump:
                if self.rightplayer.worldCenter.y < 0.80:
	                self.rightplayer.ApplyLinearImpulse(box2d.b2Vec2(0,self.jumpforce), self.rightplayer.worldCenter, True)
            if self.leftDPress:
	            self.leftplayer.ApplyLinearImpulse(box2d.b2Vec2(0,-self.jumpforce), self.leftplayer.worldCenter, True)
            #if self.leftleft == True
            #    self.leftplayer.ApplyForce((50,0), self.leftplayer.worldCenter)
            # Clear Display
            if self.ball.worldCenter.x < 1:
                print "Goal Blue!", self.rightscore
                self.leftscore += 1
                self.world.set_color((0, 0, 255))
                self.ball = self.world.add.ball((600, 0), 50)
            elif self.ball.worldCenter.x > 11:
                print "Goal Red!", self.rightscore
                self.rightscore += 1
                self.world.set_color((255, 0, 0))
                self.ball = self.world.add.ball((600, 0), 50)

            # For some reason this isn't being reached... thats
            # a problem. THe screen is gray.
            self.screen.fill((255,255,255)) 
            # Update & Draw World
            self.world.update()
            self.world.draw()
            
            # draw output from tools
            #self.currentTool.draw()
            
            #Print all the text on the screen
            
		    #text = self.font.render("Current Tool: "+self.currentTool.name, True, (255,255,255))
            #textpos = text.get_rect(left=700,top=7)
            # self.screen.blit(text,textpos)  
            # for displaying text ^
            # Flip Display
            pygame.display.flip()  
            
            # Try to stay at 30 FPS
            self.clock.tick(30) # originally 50    

def main():
    toolbarheight = 75
    tabheight = 45
    pygame.init()
    pygame.display.init()
    x,y  = pygame.display.list_modes()[0]
    screen = pygame.display.set_mode((x,y-toolbarheight))#-tabheight))
    # create an instance of the game
    game = XOlympicsGame(screen) 
    # start the main loop
    game.run()

# make sure that main get's called
if __name__ == '__main__':
    main()

