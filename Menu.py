import sys
import pygame_widgets

import cv2
import Settings
from Settings import *
from pygame_widgets.slider import Slider

from SonicBossFight import SonicBossFight
from button import Button
from SonicLevel import SonicLevel
from TailsLevel import TailsLevel


class Menu:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("[ezrf")
        self.BG1 = pygame.image.load("data/menu_objects/menu_background.png")
        self.BG2 = pygame.image.load("data/menu_objects/play_background.png")
        self.BG3 = pygame.image.load("data/menu_objects/settings_background.png")
        self.BG4 = pygame.image.load("data/menu_objects/developers_background.png")
        self.BG5 = pygame.image.load("data/menu_objects/knuckles_background.png")

        self.background_music = pygame.mixer.Sound('data/MUSIC/Bg_Music.mp3')

        self.playing = True

        self.start_video_loop()

        self.additional_sound = 0.05

    def get_font(self, size) -> pygame.font.Font:
        return pygame.font.Font("data/menu_objects/menu_font.ttf", size)

    def play_music(self) -> None:
        self.background_music.set_volume(Settings.sound)
        self.background_music.play(-1)

    def stop_music(self) -> None:
        self.background_music.stop()

    def play(self) -> None:

        running = True
        while running:
            PLAY_MOUSE_POS = pygame.mouse.get_pos()

            screen.blit(self.BG2, (0, 0))

            PLAY_SONIC = Button(image=pygame.image.load("data/menu_objects/character_rect.png"), pos=(600, 550),
                                text_input="Соник", font=self.get_font(50), base_color="White", hovering_color="Blue")

            PLAY_SONIC.changeColor(PLAY_MOUSE_POS)
            PLAY_SONIC.update(screen)

            PLAY_TAILS = Button(image=pygame.image.load("data/menu_objects/character_rect.png"), pos=(216, 550),
                                text_input="Тейлз", font=self.get_font(50), base_color="White", hovering_color="Orange")

            PLAY_TAILS.changeColor(PLAY_MOUSE_POS)
            PLAY_TAILS.update(screen)

            PLAY_KNUCKLES = Button(image=pygame.image.load("data/menu_objects/character_rect.png"), pos=(984, 550),
                                   text_input="Наклз", font=self.get_font(50), base_color="White", hovering_color="Red")

            PLAY_KNUCKLES.changeColor(PLAY_MOUSE_POS)
            PLAY_KNUCKLES.update(screen)

            PLAY_BACK = Button(image=pygame.image.load("data/menu_objects/back_rect.png"), pos=(600, 700),
                               text_input="Назад", font=self.get_font(40), base_color="White", hovering_color="Green")

            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        running = False
                        self.main_menu()
                    if PLAY_TAILS.checkForInput(PLAY_MOUSE_POS):
                        running = False
                        self.stop_music()
                        self.playing = False
                        TailsLevel()
                        self.main_menu()
                    if PLAY_SONIC.checkForInput(PLAY_MOUSE_POS):
                        running = False
                        self.stop_music()
                        self.playing = False
                        SonicLevel()
                        self.main_menu()
                    if PLAY_KNUCKLES.checkForInput(PLAY_MOUSE_POS):
                        running = False
                        self.knuckles_play()

            pygame.display.update()

    def knuckles_play(self) -> None:
        running = True
        while running:
            KNUCKLES_MOUSE_POS = pygame.mouse.get_pos()

            screen.blit(self.BG5, (0, 0))

            KNUCKLES_BACK = Button(image=pygame.image.load("data/menu_objects/back_rect.png"),
                                   pos=(600, 700),
                                   text_input="Назад", font=self.get_font(40), base_color="White",
                                   hovering_color="Green")

            KNUCKLES_BACK.changeColor(KNUCKLES_MOUSE_POS)
            KNUCKLES_BACK.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if KNUCKLES_BACK.checkForInput(KNUCKLES_MOUSE_POS):
                        running = False
                        self.play()

            pygame.display.update()

    def options(self) -> None:
        running = True
        self.slider = Slider(screen, SCREEN_WIDTH/4, 250 , SCREEN_WIDTH/2, 40, initial=Settings.sound, min=0, max=3, step=0.1, handleColour=(255, 255, 255), colour=(0, 0, 0))
        while running:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            screen.blit(self.BG3, (0, 0))
            SELECT_WASD = Button(image=pygame.image.load("data/menu_objects/select_rect.png"), pos=(420, 635),
                                 text_input="Выбрать", font=self.get_font(30), base_color="White", hovering_color="Red")

            SELECT_WASD.changeColor(OPTIONS_MOUSE_POS)
            SELECT_WASD.update(screen)

            SELECT_ARROW = Button(image=pygame.image.load("data/menu_objects/select_rect.png"), pos=(800, 635),
                                  text_input="Выбрать", font=self.get_font(30), base_color="White",
                                  hovering_color="Red")

            SELECT_ARROW.changeColor(OPTIONS_MOUSE_POS)
            SELECT_ARROW.update(screen)

            OPTIONS_BACK = Button(image=pygame.image.load("data/menu_objects/back_rect.png"), pos=(600, 730),
                                  text_input="Назад", font=self.get_font(40), base_color="White",
                                  hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        running = False
                        self.background_music.set_volume(Settings.sound)
                        self.main_menu()
                    if SELECT_ARROW.checkForInput(OPTIONS_MOUSE_POS):
                        Settings.dict_movement_pointer = 1
                    if SELECT_WASD.checkForInput(OPTIONS_MOUSE_POS):
                        Settings.dict_movement_pointer = 0
            Settings.sound = self.slider.getValue()

            pygame_widgets.update(pygame.event.get())
            pygame.display.update()

    def developers(self) -> None:
        running = True
        while running:
            DEVELOPERS_MOUSE_POS = pygame.mouse.get_pos()

            screen.blit(self.BG4, (0, 0))

            DEVELOPERS_BACK = Button(image=pygame.image.load("data/menu_objects/back_rect.png"), pos=(600, 700),
                                     text_input="Назад", font=self.get_font(40), base_color="White",
                                     hovering_color="Green")

            DEVELOPERS_BACK.changeColor(DEVELOPERS_MOUSE_POS)
            DEVELOPERS_BACK.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if DEVELOPERS_BACK.checkForInput(DEVELOPERS_MOUSE_POS):
                        running = False
                        self.main_menu()

            pygame.display.update()

    def main_menu(self) -> None:
        if not self.playing:
            self.play_music()
            self.playing = True

        running = True
        while running:

            screen.blit(self.BG1, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            PLAY_BUTTON = Button(image=pygame.image.load("data/menu_objects/play_rect.png"), pos=(990, 220),
                                 text_input="Играть", font=self.get_font(45), base_color="white",
                                 hovering_color="green")
            OPTIONS_BUTTON = Button(image=pygame.image.load("data/menu_objects/play_rect.png"), pos=(950, 380),
                                    text_input="Настройки", font=self.get_font(43), base_color="white",
                                    hovering_color="green")
            DEVELOPERS_BUTTON = Button(image=pygame.image.load("data/menu_objects/play_rect.png"), pos=(910, 540),
                                       text_input="Разрабы", font=self.get_font(45), base_color="white",
                                       hovering_color="green")
            QUIT_BUTTON = Button(image=pygame.image.load("data/menu_objects/play_rect.png"), pos=(870, 700),
                                 text_input="Выход", font=self.get_font(45), base_color="white", hovering_color="green")

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, DEVELOPERS_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        running = False
                        self.play()
                    if DEVELOPERS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        running = False
                        self.developers()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        running = False
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        quit()
            pygame.display.update()

    def start_video_loop(self) -> None:
        video = cv2.VideoCapture("data/VIDEO/INTRO.mp4")
        success, video_image = video.read()
        fps = video.get(cv2.CAP_PROP_FPS)

        window = pygame.display.set_mode(video_image.shape[1::-1])
        clock = pygame.time.Clock()
        pygame.mixer.init()
        pygame.mixer.music.load('data/MUSIC/INTRO_MUSIC.mp3')
        pygame.mixer.music.set_volume(Settings.sound)
        pygame.mixer.music.play(-1)

        run = success
        while run:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()


            success, video_image = video.read()
            if success:
                video_surf = pygame.image.frombuffer(
                    video_image.tobytes(),
                    video_image.shape[1::-1],
                    "BGR"
                )
            else:
                run = False
            window.blit(video_surf, (0, 0))
            pygame.display.flip()

        pygame.mixer.music.stop()
        self.play_music()
        self.main_menu()