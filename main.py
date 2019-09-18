import os
import ctypes

os.environ["PYSDL2_DLL_PATH"] = "lib/"

from lib import *


def main(screen):
	menu.MenuMain(screen)


def init():
	ctypes.windll.user32.SetProcessDPIAware()
	SDL_Init(SDL_INIT_VIDEO)
	TTF_Init()
	screen = display.Screen("Plateformer", (SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED), (1600, 900), SDL_WINDOW_SHOWN, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
	
	main(screen)
	
	TTF_Quit()
	SDL_Quit()


if __name__ == "__main__":
	init()