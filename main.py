import pygame
from utils.draw_graphics import game_loop
pygame.init()
pygame.display.set_caption("Professor Snake: AI Powered Snake Game")

Clock = pygame.time.Clock()

def main():
    game_loop(Clock)

main()