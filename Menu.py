import sys

import cv2


from Settings import *
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
        self.start_video_loop()
    def get_font(self, size):
        return pygame.font.Font("data/menu_objects/menu_font.ttf", size)

    def play(self):
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
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        running = False
                        self.main_menu()
                    if PLAY_TAILS.checkForInput(PLAY_MOUSE_POS):
                        running = False
                        TailsLevel()
                        self.main_menu()
                    if PLAY_SONIC.checkForInput(PLAY_MOUSE_POS):
                        running = False
                        SonicLevel()
                        self.main_menu()

            pygame.display.update()

    def options(self):
        running = True
        while running:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            screen.blit(self.BG3, (0, 0))

            PLUS_VOLUME = Button(image=pygame.image.load("data/menu_objects/plus_rect.png"), pos=(680, 270),
                                 text_input="+", font=self.get_font(50), base_color="Black", hovering_color="White")

            PLUS_VOLUME.changeColor(OPTIONS_MOUSE_POS)
            PLUS_VOLUME.update(screen)

            MINUS_VOLUME = Button(image=pygame.image.load("data/menu_objects/minus_rect.png"), pos=(520, 270),
                                  text_input="-", font=self.get_font(50), base_color="Black", hovering_color="White")

            MINUS_VOLUME.changeColor(OPTIONS_MOUSE_POS)
            MINUS_VOLUME.update(screen)

            SELECT_WASD = Button(image=pygame.image.load("data/menu_objects/select_rect.png"), pos=(420, 635),
                                 text_input="Выбрать", font=self.get_font(30), base_color="White", hovering_color="Red")

            SELECT_WASD.changeColor(OPTIONS_MOUSE_POS)
            SELECT_WASD.update(screen)

            SELECT_ARROW = Button(image=pygame.image.load("data/menu_objects/select_rect.png"), pos=(800, 635),
                                  text_input="Выбрать", font=self.get_font(30), base_color="White", hovering_color="Red")

            SELECT_ARROW.changeColor(OPTIONS_MOUSE_POS)
            SELECT_ARROW.update(screen)

            OPTIONS_BACK = Button(image=pygame.image.load("data/menu_objects/back_rect.png"), pos=(600, 730),
                                  text_input="Назад", font=self.get_font(40), base_color="White", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        running = False
                        self.main_menu()

            pygame.display.update()

    def developers(self):
        running = True
        while running:
            DEVELOPERS_MOUSE_POS = pygame.mouse.get_pos()

            screen.blit(self.BG4, (0, 0))

            DEVELOPERS_BACK = Button(image=pygame.image.load("data/menu_objects/back_rect.png"), pos=(600, 700),
                                     text_input="Назад", font=self.get_font(40), base_color="White", hovering_color="Green")

            DEVELOPERS_BACK.changeColor(DEVELOPERS_MOUSE_POS)
            DEVELOPERS_BACK.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if DEVELOPERS_BACK.checkForInput(DEVELOPERS_MOUSE_POS):
                        running = False
                        self.main_menu()

            pygame.display.update()

    def main_menu(self):
        running = True
        while running:
            screen.blit(self.BG1, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            PLAY_BUTTON = Button(image=pygame.image.load("data/menu_objects/play_rect.png"), pos=(990, 220),
                                 text_input="Играть", font=self.get_font(45), base_color="white", hovering_color="green")
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
                    self.quit()
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
                        self.quit()

            pygame.display.update()

    def start_video_loop(self) -> None:
        # video = cv2.VideoCapture("data/VIDEO/INTRO.mp4")
        # success, video_image = video.read()
        # fps = video.get(cv2.CAP_PROP_FPS)
        #
        # window = pygame.display.set_mode(video_image.shape[1::-1])
        # clock = pygame.time.Clock()
        # pygame.mixer.init()
        # pygame.mixer.music.load('data/MUSIC/INTRO_MUSIC.mp3')
        # pygame.mixer.music.play(-1)
        #
        # run = success
        # while run:
        #     clock.tick(fps)
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             self.quit()
        #
        #
        #     success, video_image = video.read()
        #     if success:
        #         video_surf = pygame.image.frombuffer(
        #             video_image.tobytes(),
        #             video_image.shape[1::-1],
        #             "BGR"
        #         )
        #     else:
        #         run = False
        #     window.blit(video_surf, (0, 0))
        #     pygame.display.flip()

        pygame.mixer.music.stop()
        self.main_menu()

    def quit(self):
        pygame.quit()
        sys.exit()