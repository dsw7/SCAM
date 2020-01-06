import sys
import pygame
from threading import Thread
from queue import Queue, Empty


pygame.init()
screen = pygame.display.set_mode((300, 300))

coordinates = Queue(2)
coordinates.put([0.5, 0.5])

class Input(Thread):
    def run(self):
        while True:
            x = float(input('x: '))
            y = float(input('y: '))
            end_position = ([x, y])
            coordinates.put(end_position)
            

io_thread = Input()
io_thread.start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
           
    # do something with coordinates instance 
    # coordinates.get() ...

    
io_thread.join()