#!/usr/bin/python

import os,sys
import pygame
import time
import random

import kvvliveapi
 
class pyscope :
    screen = None;
    
    def __init__(self):
        self.running = False
        self.backgroundColor = (0,0,0)
        self.textColor = (255,255,255)
        self.framerate = 40
        self.lastupdate = None
        self.interval = 5000
        self.departures = []

        self.trainImg = pygame.image.load('train.jpg')

        self.initFramebuffer()

        self.font = pygame.font.Font("DroidSansMono.ttf", 32)#pygame.font.SysFont("Courier", 32)
        self.bigFont = pygame.font.SysFont("FreeMono, Monospace", 72)

        pygame.mouse.set_visible(False)


    def initFramebuffer(self):
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
            pygame.display.init()
	    self.screenSize = (800,600)
            self.screen = pygame.display.set_mode(self.screenSize)
        
        else:
	    print "loading framebuffer"

            drivers = ['fbcon', 'directfb', 'svgalib', 'fbdev', 'inteldrmfb', 'dga', 'ggi', 'vgl', 'svgalib', 'aalib']
            found = False
            for driver in drivers:
		print "trying " + driver
                if not os.getenv('SDL_VIDEODRIVER'):
                    os.putenv('SDL_VIDEODRIVER', driver)
                try:
                    pygame.display.init()
                except pygame.error:
                    print 'Driver: {0} failed.'.format(driver)
                    continue
                found = True
                break
        
            if not found:
                raise Exception('No suitable video driver found!')
            
            self.screenSize = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            print "Framebuffer size: %d x %d" % (self.screenSize[0], self.screenSize[1])
            self.screen = pygame.display.set_mode(self.screenSize, pygame.FULLSCREEN)
        self.screen.fill((0, 0, 0))        
        pygame.font.init()
        pygame.display.update()
 
    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."
 
    def update(self):
	time = pygame.time.get_ticks()
	print "time:" + str(time) + ' ' + str(self.lastupdate) + ' ' + str(self.interval)
        if self.lastupdate == None or (time - self.lastupdate) > self.interval:
            self.departures = kvvliveapi.get_departures('de:8212:7')
	    self.lastupdate = time
	    sys.stdout.flush()

    def draw(self):
        self.screen.blit(self.trainImg, (300, 250))
        
        textSurface = self.bigFont.render("FELIX", True, self.textColor)
        self.screen.blit(textSurface, (0, 0))

	clockData = time.strftime("%H:%M:%S", time.gmtime())
	print clockData
	clockSurface = self.bigFont.render(clockData, True, self.textColor)
	self.screen.blit(clockSurface, (self.screenSize[0] - clockSurface.get_width(), self.screenSize[1] - clockSurface.get_height()))

        x = 50
        y = 50
	i = 0
        for departure in self.departures:
	    i += 1
            text = departure.route.ljust(5, ' ') + ' ' + departure.destination.ljust(20, ' ') + ' ' + departure.timestr.ljust(10, ' ')
            textSurface = self.font.render(text, True, self.textColor)
            y += 30
	    if i > 10: break


            self.screen.blit(textSurface, (x, y))
    
    def run(self):
        self.running = True
	print "Starting Screen"

        clock = pygame.time.Clock()
        while self.running:
            clock.tick(self.framerate)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
            self.screen.fill(self.backgroundColor)
            self.update()
            self.draw()
            pygame.display.update()

	print "Screen is now not running anymore"
 
scope = pyscope()
scope.run()
time.sleep(10)
