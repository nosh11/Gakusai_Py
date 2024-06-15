from os import walk
import pygame

def import_folder(path, scale: tuple):
	surface_list = []

	for _, __, img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(pygame.transform.scale(image_surf, scale))

	return surface_list