import pygame
import sys
from .constants import BACKGROUND, FPS, WHITE, FONTS_PATH, VERSION
from .buttons import Button
from .players import Player
from .assets import Asset
from .stats import get_solo_numbers


class ScreenManager:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self._resizing_display = False
        self._start_menu = False
        self._game_run = False
        self._end_screen = False
        self._about_screen = False
        self._reveal_cards = False
        self._stats_screen = False
        self._rulebook = False
        self._interrupt = False
        self._confirmed = False
        self._current_page = 0

    '''
    Structure of a Screen:
    1) pre-loop definitions
    2) while loop
    2.1) set clock.tick and set local relative HINT and DISP_W and DISP_H
    2.2) (re)create buttons only at start and when resizing display
    2.3) set fonts
    2.4) blit things independent of player input 
    2.5) call the button.type methods (independent of event)
    2.6) update display
    2.7) events loop
    2.7.1) call button.get_event methods for all buttons
    2.7.2) call any other input dependent function
    2.7.3) transition to other screens conditional
    2.7.4) resize screen conditional
    2.7.5) quit conditional
    '''

    def start_menu(self, game, display):
        self._start_menu = True
        self._resizing_display = True

        while self._start_menu:
            self.clock.tick(FPS)
            HINT = (
                display.HINT * 1.5
            )  # Magic number adjusts sizes without messing positions.
            DISP_W = display.DISP_W
            DISP_H = display.DISP_H

            # BUTTONS
            if self._resizing_display:
                self._resizing_display = False
                solo = Button(
                    DISP_W * 0.5 - HINT * 0.75,
                    HINT * 0.7,
                    HINT * 0.4,
                    HINT * 0.4,
                    "players_one.png",
                    "players_one_hover.png",
                    game.choose_players,
                    (1,),
                )
                two = Button(
                    DISP_W * 0.5 - HINT * 0.25,
                    HINT * 0.7,
                    HINT * 0.4,
                    HINT * 0.4,
                    "players_two.png",
                    "players_two_hover.png",
                    game.choose_players,
                    (2,),
                )
                three = Button(
                    DISP_W * 0.5 + HINT * 0.25,
                    HINT * 0.7,
                    HINT * 0.4,
                    HINT * 0.4,
                    "players_three.png",
                    "players_three_hover.png",
                    game.choose_players,
                    (3,),
                )
                four = Button(
                    DISP_W * 0.5 + HINT * 0.75,
                    HINT * 0.7,
                    HINT * 0.4,
                    HINT * 0.4,
                    "players_four.png",
                    "players_four_hover.png",
                    game.choose_players,
                    (4,),
                )
                grid = Button(
                    DISP_W * 0.5,
                    HINT * 1.5,
                    HINT * 0.6,
                    HINT * 0.2,
                    "toggle_left.png",
                    "toggle_right.png",
                    game.choose_grid,
                )
                setup = Button(
                    DISP_W * 0.5,
                    HINT * 2.2,
                    HINT * 0.6,
                    HINT * 0.2,
                    "toggle_left.png",
                    "toggle_right.png",
                    game.choose_setup,
                )
                logo = Button(
                    DISP_W * 0.5,
                    HINT * 3.2,
                    HINT * 1.5,
                    HINT * 1.5,
                    "mk_logo.png",
                    "mk_logo_hover.png",
                    self._start_game,
                )
                about = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "about.png",
                    "about_hover.png",
                    self._call_about,
                )

            DIMBO_L = pygame.font.Font(
                FONTS_PATH + "dimbo_regular.otf", int(HINT * 0.20)
            )
            DIMBO_R = pygame.font.Font(
                FONTS_PATH + "dimbo_regular.otf", int(HINT * 0.18)
            )
            UBUNTU_R = pygame.font.Font(
                FONTS_PATH + "ubuntu_regular.otf", int(HINT * 0.10)
            )
            UBUNTU_S = pygame.font.Font(
                FONTS_PATH + "ubuntu_regular.otf", int(HINT * 0.05)
            )
            display.WINDOW.fill((BACKGROUND))
            blit_text(
                display.WINDOW, DIMBO_L, "Number of Players", DISP_W * 0.5, HINT * 0.3
            )
            blit_text(display.WINDOW, DIMBO_L, "Grid Size", DISP_W * 0.5, HINT * 1.2)
            blit_text(
                display.WINDOW, DIMBO_R, "5x5", DISP_W * 0.5 - HINT * 0.5, HINT * 1.5
            )
            blit_text(
                display.WINDOW, DIMBO_R, "6x6", DISP_W * 0.5 + HINT * 0.5, HINT * 1.5
            )
            blit_text(
                display.WINDOW, DIMBO_L, "Setup Variant", DISP_W * 0.5, HINT * 1.9
            )
            blit_text(
                display.WINDOW,
                DIMBO_R,
                "Standard",
                DISP_W * 0.5 - HINT * 0.7,
                HINT * 2.2,
            )
            blit_text(
                display.WINDOW,
                DIMBO_R,
                "Alternate",
                DISP_W * 0.5 + HINT * 0.7,
                HINT * 2.2,
            )

            solo.switch(display.WINDOW, (game._num_of_players == 2))
            two.switch(display.WINDOW, (game._num_of_players == 3))
            three.switch(display.WINDOW, (game._num_of_players == 4))
            four.switch(display.WINDOW, (game._num_of_players == 5))
            grid.toggle(display.WINDOW, (game._grid_size == (6, 6)), False)
            setup.toggle(display.WINDOW, (game._setup_variant == "alternate"), False)
            logo.button(display.WINDOW, False)
            about.toggle(display.WINDOW, (self._about_screen == True))

            pygame.display.update()

            for event in pygame.event.get():
                display.knmcd.code(display, event)
                solo.get_event(display.WINDOW, event)
                two.get_event(display.WINDOW, event)
                three.get_event(display.WINDOW, event)
                four.get_event(display.WINDOW, event)
                grid.get_event(display.WINDOW, event)
                setup.get_event(display.WINDOW, event)
                logo.get_event(display.WINDOW, event)
                about.get_event(display.WINDOW, event)

                if self._about_screen:
                    self.about_screen(game, display)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    display._resize(game.board, size)
                    self._resizing_display = True

    def game_screen(self, game, display):
        self._game_run = True
        self._resizing_display = True

        while self._game_run:
            self.clock.tick(FPS)
            HINT = (
                display.HINT * 1.5
            )  # Magic number adjusts sizes without messing positions.
            DISP_W = display.DISP_W
            DISP_H = display.DISP_H

            if self._resizing_display:
                self._resizing_display = False
                replay = Button(
                    HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "replay.png",
                    "replay_hover.png",
                    self.interrupt_game,
                    (game, display),
                )
                about = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "about.png",
                    "about_hover.png",
                    self._call_about,
                )


            display.WINDOW.fill((BACKGROUND))
            replay.button(display.WINDOW)
            about.toggle(display.WINDOW, (self._about_screen == True))
            display.print_all(game.board, game.current, update=False)
            if not game._all_pawns_set and (len(game.counter.pawn) != 0 or Player.total != 2):
                display.print_invalid_placement(game)
            pygame.display.update()

            for event in pygame.event.get():
                display.knmcd.code(display, event)
                if event.type == pygame.QUIT:
                    game._abandoned = True
                    self._game_run = False

                about.get_event(display.WINDOW, event)
                if self._about_screen:
                    self.about_screen(game, display)

                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    display._resize(game.board, size)
                    self._resizing_display = True

                replay.get_event(display.WINDOW, event)
                if self._interrupt:
                    game._abandoned = True
                    self._game_run = False
                elif game.is_end_game():
                    self._game_run = False
                    display.WINDOW.fill((BACKGROUND))
                    replay.button(display.WINDOW)
                    about.toggle(display.WINDOW, (self._about_screen == True))
                    display.print_all(game.board, game.current)
                    pygame.time.wait(600)
                else:
                    if game._all_pawns_set is not True:
                        game.place_pawns(display, event)
                    if game._all_pawns_set is True:
                        game.round(display, event)
                    if game.end_turn is True:
                        game._turns += 1
                        game.change_turn()

    def end_screen(self, game, display):
        self._end_screen = True
        self._resizing_display = True

        while self._end_screen:
            self.clock.tick(FPS)
            HINT = (
                display.HINT * 1.5
            )  # Magic number adjusts sizes without messing positions.
            DISP_W = display.DISP_W
            DISP_H = display.DISP_H

            # BUTTON
            if self._resizing_display:
                self._resizing_display = False
                replay = Button(
                    HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "replay.png",
                    "replay_hover.png",
                    game._reset,
                )

                reveal = Button(
                    HINT * 0.5,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "reveal.png",
                    "reveal_hover.png",
                    self._call_reveal,
                )

                about = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "about.png",
                    "about_hover.png",
                    self._call_about,
                )

            if game._winner is None:
                return
            else:
                display.WINDOW.fill((BACKGROUND))

                DIMBO_L = pygame.font.Font(
                    FONTS_PATH + "dimbo_regular.otf", int(HINT * 0.5)
                )
                DIMBO_R = pygame.font.Font(
                    FONTS_PATH + "dimbo_regular.otf", int(HINT * 0.2)
                )
                if Player.total == 2:
                    if game._winner == game.counter:
                        blit_text(
                            display.WINDOW,
                            DIMBO_L,
                            "You Lost!",
                            DISP_W * 0.5,
                            DISP_H * 0.5 - HINT * 0.5,
                        )
                        if game._winner.score >= 6:
                            blit_text(
                                display.WINDOW,
                                DIMBO_R,
                                f"The Counter King recruited {game._winner.score} {'Pairs' if game._winner.score != 1 else 'Pair.'}",
                                DISP_W * 0.5,
                                DISP_H * 0.5 + HINT * 0.1,
                            )
                        else:
                            blit_text(
                                display.WINDOW,
                                DIMBO_R,
                                f"The Counter King reached the last card of the grid.",
                                DISP_W * 0.5,
                                DISP_H * 0.5 + HINT * 0.1,
                            )
                    else:
                        blit_text(
                            display.WINDOW,
                            DIMBO_L,
                            "You Won!",
                            DISP_W * 0.5,
                            DISP_H * 0.5 - HINT * 0.5,
                        )
                        blit_text(
                            display.WINDOW,
                            DIMBO_R,
                            f"You recruited {game._winner.score} {'Pairs' if game._winner.score != 1 else 'Pair'}.",
                            DISP_W * 0.5,
                            DISP_H * 0.5 + HINT * 0.1,
                        )
                else:
                    blit_text(
                        display.WINDOW,
                        DIMBO_L,
                        f"Player {game._winner.color} Won!",
                        DISP_W * 0.5,
                        DISP_H * 0.5 - HINT * 0.5,
                    )
                    blit_text(
                        display.WINDOW,
                        DIMBO_R,
                        f"{game._winner.score} {'Pairs' if game._winner.score != 1 else 'Pair'} Recruited.",
                        DISP_W * 0.5,
                        DISP_H * 0.5 + HINT * 0.1,
                    )

                replay.button(display.WINDOW)
                reveal.toggle(display.WINDOW, (self._reveal_cards == True))
                about.toggle(display.WINDOW, (self._about_screen == True))

                pygame.display.update()

                for event in pygame.event.get():
                    display.knmcd.code(display, event)
                    replay.get_event(display.WINDOW, event)
                    reveal.get_event(display.WINDOW, event)
                    about.get_event(display.WINDOW, event)

                    if event.type == pygame.QUIT:
                        self._end_screen = False

                    if event.type == pygame.VIDEORESIZE:
                        size = pygame.display.get_window_size()
                        display._resize(game.board, size)
                        self._resizing_display = True

                    if self._about_screen:
                        self.about_screen(game, display)

                    if self._reveal_cards:
                        self.reveal_cards(game, display)

    def reveal_cards(self, game, display):
        self._resizing_display = True

        while self._reveal_cards:
            self.clock.tick(FPS)
            HINT = (
                display.HINT * 1.5
            )  # Magic number adjusts sizes without messing positions.
            DISP_W = display.DISP_W
            DISP_H = display.DISP_H

            if self._resizing_display:
                self._resizing_display = False
                replay = Button(
                    HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "replay.png",
                    "replay_hover.png",
                    game._reset,
                )

                reveal = Button(
                    HINT * 0.5,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "reveal.png",
                    "reveal_hover.png",
                    self._call_reveal,
                )

                about = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "about.png",
                    "about_hover.png",
                    self._call_about,
                )

            display.WINDOW.fill((BACKGROUND))
            about.toggle(display.WINDOW, (self._about_screen == True))
            replay.button(display.WINDOW)
            reveal.toggle(display.WINDOW, (self._reveal_cards == True))
            display.print_all(
                game.board,
                current_player=None,
                invalid_moves=False,
                grid_revealed=True,
                update=False,
            )
            pygame.display.update()

            for event in pygame.event.get():

                about.get_event(display.WINDOW, event)
                reveal.get_event(display.WINDOW, event)
                replay.get_event(display.WINDOW, event)

                if self._about_screen:
                    self.about_screen(game, display)

                if game._reset_game:
                    self._reveal_cards = False

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    display._resize(game.board, size)
                    self._resizing_display = True

    def about_screen(self, game, display):
        self._resizing_display = True
        while self._about_screen:
            self.clock.tick(FPS)
            HINT = (
                display.HINT * 1.5
            )  # Magic number adjusts sizes without messing positions.
            DISP_W = display.DISP_W
            DISP_H = display.DISP_H

            if self._resizing_display:
                self._reisizing_display = False
                pdf_logo = Button(
                    DISP_W * 0.5 - HINT,
                    HINT * 1.5,
                    HINT * 0.4,
                    HINT * 0.4,
                    "pdf_logo.png",
                    action_func=self._open_link,
                    action_arg=("https://drive.google.com/file/d/1be3mYSzGpOooiSTmYnRBguKZ-2J40ip9/view?usp=sharing",),
                )

                youtube_logo = Button(
                    DISP_W * 0.5 + HINT,
                    HINT * 1.5,
                    HINT * 0.4,
                    HINT * 0.4,
                    "youtube_logo.png",
                    action_func=self._open_link,
                    action_arg=("https://youtu.be/snqjQtYmv_Q",),
                )

                bgg_logo = Button(
                    DISP_W * 0.5,
                    HINT * 2.8,
                    HINT * 0.4,
                    HINT * 0.4,
                    "bgg_logo.png",
                    action_func=self._open_link,
                    action_arg=("https://boardgamegeek.com/boardgame/319384/memory-kings",),
                )
                tgc_logo = Button(
                    DISP_W * 0.5 - HINT * 0.8,
                    HINT * 2.6,
                    HINT * 0.4,
                    HINT * 0.4,
                    "tgc_logo.png",
                    action_func=self._open_link,
                    action_arg=("https://www.thegamecrafter.com/games/memory-kings",),
                )
                facebook_logo = Button(
                    DISP_W * 0.5 + HINT * 0.8,
                    HINT * 2.6,
                    HINT * 0.4,
                    HINT * 0.4,
                    "facebook_logo.png",
                    action_func=self._open_link,
                    action_arg=("https://www.facebook.com/memorykingsthegame",),
                )
                sneaky_pirates_logo = Button(
                    DISP_W * 0.5,
                    DISP_H - HINT * 0.6,
                    HINT * 0.6,
                    HINT * 0.6,
                    "sneaky_pirates_logo.png",
                )
                stats = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.79,
                    HINT * 0.2,
                    HINT * 0.2,
                    "stats.png",
                    "stats_hover.png",
                    self._call_stats,
                )
                mute = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.49,
                    HINT * 0.2,
                    HINT * 0.2,
                    "sound_on.png",
                    "sound_off.png",
                    self._mute,
                )
                rules = Button(
                    DISP_W - HINT * 0.5,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "help.png",
                    "help_hover.png",
                    self._call_rulebook,
                )
                about = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "about.png",
                    "about_hover.png",
                    self._call_about,
                )

            display.WINDOW.fill((BACKGROUND))
            DIMBO_L = pygame.font.Font(
                FONTS_PATH + "dimbo_regular.otf", int(HINT * 0.20)
            )
            DIMBO_R = pygame.font.Font(
                FONTS_PATH + "dimbo_regular.otf", int(HINT * 0.12)
            )
            UBUNTU_R = pygame.font.Font(
                FONTS_PATH + "ubuntu_regular.otf", int(HINT * 0.10)
            )
            UBUNTU_S = pygame.font.Font(
                FONTS_PATH + "ubuntu_regular.otf", int(HINT * 0.05)
            )
            blit_text(display.WINDOW, DIMBO_L, "About", DISP_W * 0.5, HINT * 0.3)
            blit_long_text(
                display,
                "In Memory Kings, players challenge their memory in a mix of the classic games of Chess and Pairs (a.k.a. Match Up). They move their pawns strategically across a grid of hidden cards, revealing them, and finding indentical pairs. The player that finds the most pairs wins!",
                (HINT * 0.5, HINT * 0.5),
                UBUNTU_R,
                HINT * 0.5,
            )
            blit_text(display.WINDOW, DIMBO_L, "How to Play", DISP_W * 0.5, HINT * 1.6)
            blit_text(
                display.WINDOW,
                DIMBO_R,
                "Download Rulebook",
                DISP_W * 0.5 - HINT,
                HINT * 1.89,
            )
            blit_text(
                display.WINDOW,
                DIMBO_R,
                "Video Tutorial",
                DISP_W * 0.5 + HINT,
                HINT * 1.81,
            )
            blit_text(
                display.WINDOW,
                DIMBO_R,
                " (2-4 Players)",
                DISP_W * 0.5 + HINT,
                HINT * 1.97,
            )
            blit_text(display.WINDOW, DIMBO_L, "Links", DISP_W * 0.5, HINT * 2.4)
            blit_text(
                display.WINDOW,
                DIMBO_R,
                "Digital Version by G. Scary T.",
                DISP_W * 0.5,
                DISP_H - HINT * 0.2,
            )
            blit_text(
                display.WINDOW,
                UBUNTU_S,
                f"Memory Kings v{VERSION} in Python3.85/Pygame2.0",
                DISP_W * 0.01,
                DISP_H * 0.99,
                "bottomleft",
            )
            blit_image(display.WINDOW, Asset.image["rules_notice.png"],(DISP_W*0.80,DISP_H*0.87),HINT*0.6,HINT*0.6)

            stats.switch(display.WINDOW, (self._stats_screen == True))
            mute.switch(display.WINDOW, (Asset._mute_sounds == True))
            about.switch(display.WINDOW, (self._about_screen == True))
            rules.switch(display.WINDOW, (bool(self._rulebook) is True))
            pdf_logo.button(display.WINDOW)
            youtube_logo.button(display.WINDOW)
            bgg_logo.button(display.WINDOW)
            tgc_logo.button(display.WINDOW)
            facebook_logo.button(display.WINDOW)
            sneaky_pirates_logo.button(display.WINDOW, False)

            pygame.display.update()

            for event in pygame.event.get():
                display.knmcd.code(display, event)
                stats.get_event(display.WINDOW, event)
                mute.get_event(display.WINDOW, event)
                about.get_event(display.WINDOW, event)
                rules.get_event(display.WINDOW, event)
                pdf_logo.get_event(display.WINDOW, event)
                youtube_logo.get_event(display.WINDOW, event)
                bgg_logo.get_event(display.WINDOW, event)
                tgc_logo.get_event(display.WINDOW, event)
                facebook_logo.get_event(display.WINDOW, event)
                sneaky_pirates_logo.get_event(display.WINDOW, event)

                if event.type == pygame.QUIT:
                    if self._game_run == True:
                        game._abandoned = True
                        self._game_run = False
                        self._about_screen = False
                    else:
                        pygame.quit()
                        sys.exit()

                if bool(self._rulebook):
                    self.rulebook_screen(game,display)

                if self._stats_screen:
                    self.stats_screen(game, display)

                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    display._resize(game.board, size)
                    self._resizing_display = True

    def stats_screen(self, game, display):
        self._stats_screen = True

        while self._stats_screen:
            self.clock.tick(FPS)
            self._resizing_display = True
            HINT = (
                display.HINT * 1.5
            )  # Magic number adjusts sizes without messing positions.
            DISP_W = display.DISP_W
            DISP_H = display.DISP_H

            if self._resizing_display:
                self._reisizing_display = False
                stats = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.79,
                    HINT * 0.2,
                    HINT * 0.2,
                    "stats.png",
                    "stats_hover.png",
                    self._call_stats,
                )
                mute = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.49,
                    HINT * 0.2,
                    HINT * 0.2,
                    "sound_on.png",
                    "sound_off.png",
                    self._mute,
                )
                about = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "about.png",
                    "about_hover.png",
                    self._call_about,
                )

            display.WINDOW.fill((BACKGROUND))
            DIMBO_L = pygame.font.Font(
                FONTS_PATH + "dimbo_regular.otf", int(HINT * 0.20)
            )
            UBUNTU_R = pygame.font.Font(
                FONTS_PATH + "ubuntu_regular.otf", int(HINT * 0.10)
            )
            DF = get_solo_numbers()
            blit_text(display.WINDOW, DIMBO_L, "Solo Games:", DISP_W * 0.5, HINT * 0.3)
            if DF:
                blit_text(display.WINDOW, UBUNTU_R, f"Completed Games:    {DF['Games']}", DISP_W*0.5, HINT * 0.6)
                blit_text(display.WINDOW, UBUNTU_R, f"Victories:    {DF['Wins']}", DISP_W*0.5, HINT * 0.75)
                blit_text(display.WINDOW, UBUNTU_R, f"Defeats:    {DF['Defeats']}", DISP_W*0.5, HINT * 0.90)
                blit_text(display.WINDOW, UBUNTU_R, f"Average Number of Turns:    {round(DF['Turns'], 2)}", DISP_W*0.5, HINT * 1.05)
                blit_text(display.WINDOW, UBUNTU_R, f"Average Counter Score:    {round(DF['Counter'], 2)}", DISP_W*0.5, HINT * 1.20)
                blit_text(display.WINDOW, UBUNTU_R, f"Average Player Score:    {round(DF['Player'], 2)}", DISP_W*0.5, HINT * 1.35)
                blit_text(display.WINDOW, UBUNTU_R, f"Average Queen Uses:    {round(DF['Queen'], 2)}", DISP_W*0.5, HINT * 1.50)
                blit_text(display.WINDOW, UBUNTU_R, f"Abandoned Games:    {DF['Abandoned']}", DISP_W*0.5, HINT * 1.65)
            else:
                blit_text(display.WINDOW, UBUNTU_R, f"There is no data for Solo Games yet.", DISP_W*0.5, HINT * 1.0)

            blit_text(display.WINDOW, DIMBO_L, "Multiplayer Games:", DISP_W * 0.5, DISP_H * 0.5)
            blit_text(display.WINDOW, UBUNTU_R, f"Sorry!", DISP_W*0.5, DISP_H * 0.5 + HINT * 0.7)
            blit_text(display.WINDOW, UBUNTU_R, f"Stats for Multiplayer Games are not available in this version.", DISP_W*0.5, DISP_H * 0.5 + HINT * 0.85)

            stats.toggle(display.WINDOW, (self._stats_screen == True))
            mute.toggle(display.WINDOW, (Asset._mute_sounds == True))
            about.toggle(display.WINDOW, (self._about_screen == True))

            pygame.display.update()

            for event in pygame.event.get():
                display.knmcd.code(display, event)
                stats.get_event(display.WINDOW, event)
                mute.get_event(display.WINDOW, event)
                about.get_event(display.WINDOW, event)

                if event.type == pygame.QUIT:
                    if self._game_run == True:
                        game._abandoned = True
                        self._game_run = False
                        self._about_screen = False
                    else:
                        pygame.quit()
                        sys.exit()

                if self._about_screen is False:
                    self._stats_screen = False

                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    display._resize(game.board, size)
                    self._resizing_display = True

    def rulebook_screen(self, game, display):
        while bool(self._rulebook):
            self.clock.tick(FPS)
            self._resizing_display = True
            HINT = (
                display.HINT * 1.5
            )  # Magic number adjusts sizes without messing positions.
            DISP_W = display.DISP_W
            DISP_H = display.DISP_H

            if self._resizing_display:
                self._reisizing_display = False
                back = Button(
                    HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "back.png",
                    "back_hover.png",
                    self._flip_back,
                )
                forward = Button(
                    HINT * 0.5,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "forward.png",
                    "forward_hover.png",
                    self._flip_forward,
                )
                rules = Button(
                    DISP_W - HINT * 0.5,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "help.png",
                    "help_hover.png",
                    self._call_rulebook,
                )
                about = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "about.png",
                    "about_hover.png",
                    self._call_about,
                )

            display.WINDOW.fill((BACKGROUND))
            blit_image(display.WINDOW,self._rulebook[self._current_page], (DISP_W*0.5,DISP_H*0.5), HINT*3, HINT*4.2)
            forward.button(display.WINDOW)
            back.button(display.WINDOW)
            rules.toggle(display.WINDOW, (bool(self._rulebook) is True))
            about.toggle(display.WINDOW, (self._about_screen is True))

            pygame.display.update()

            for event in pygame.event.get():
                display.knmcd.code(display, event)
                forward.get_event(display.WINDOW, event)
                back.get_event(display.WINDOW, event)
                rules.get_event(display.WINDOW, event)
                about.get_event(display.WINDOW, event)

                if event.type == pygame.QUIT:
                    if self._game_run == True:
                        game._abandoned = True
                        self._game_run = False
                        self._about_screen = False
                    else:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and self._current_page < 7:
                        self._current_page += 1
                    elif event.key == pygame.K_LEFT and self._current_page > 0:
                        self._current_page -= 1

                if self._about_screen is False:
                    self._rulebook = False

                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    display._resize(game.board, size)
                    self._resizing_display = True

    def interrupt_game(self, game, display):
        while True:
            self.clock.tick(FPS)
            self._resizing_display = True
            HINT = (
                display.HINT * 1.5
            )  # Magic number adjusts sizes without messing positions.
            DISP_W = display.DISP_W
            DISP_H = display.DISP_H
            if self._resizing_display:
                self._reisizing_display = False
                locked1 = Button(
                    HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "button_locked.png",
                )
                locked2 = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "button_locked.png",
                )
                yes = Button(
                    DISP_W * 0.5 - HINT * 0.3,
                    DISP_H * 0.5 + HINT * 0.2,
                    HINT * 0.3,
                    HINT * 0.3,
                    "yes.png",
                    "yes_hover.png",
                    self._yes_no,
                    (True,),
                )
                no = Button(
                    DISP_W * 0.5 + HINT * 0.3,
                    DISP_H * 0.5 + HINT * 0.2,
                    HINT * 0.3,
                    HINT * 0.3,
                    "no.png",
                    "no_hover.png",
                    self._yes_no,
                    (False,),
                )
            display.WINDOW.fill((BACKGROUND))
            display.print_all(game.board, game.current, update="off", invalid_moves="off")

            border = pygame.rect.Rect(0,0,HINT*3.05, HINT*1.25)
            border.center = (DISP_W*0.5, DISP_H*0.5)
            pygame.draw.rect(display.WINDOW, (WHITE), border)
            rect = pygame.rect.Rect(0,0,HINT*3, HINT*1.2)
            rect.center = (DISP_W*0.5, DISP_H*0.5)
            pygame.draw.rect(display.WINDOW, (BACKGROUND), rect)

            locked1.button(display.WINDOW, False)
            locked2.button(display.WINDOW, False)
            yes.button(display.WINDOW)
            no.button(display.WINDOW)

            DIMBO_L = pygame.font.Font(
                FONTS_PATH + "dimbo_regular.otf", int(HINT * 0.20)
            )
            blit_text(display.WINDOW, DIMBO_L, "Do you really wish to abandon the game?", DISP_W * 0.5, DISP_H * 0.5 - HINT*0.25)
            pygame.display.update()
            for event in pygame.event.get():
                display.knmcd.code(display, event)
                yes.get_event(display.WINDOW, event)
                no.get_event(display.WINDOW, event)
                if self._confirmed == "no":
                    self._confirmed = False
                    event = pygame.event.clear()
                    return
                elif self._confirmed == "yes":
                    self._interrupt = True
                    return
                if event.type == pygame.QUIT:
                    if self._game_run == True:
                        game._abandoned = True
                        self._game_run = False
                        return
                    else:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    display._resize(game.board, size)
                    self._resizing_display = True

    # TRANSITION METHODS (Called by Buttons to switch screens)

    def _start_game(self):
        self._start_menu = False

    def _call_about(self):
        if self._about_screen is False:
            self._about_screen = True
        else:
            self._about_screen = False

    def _call_stats(self):
        if self._stats_screen is False:
            self._stats_screen = True
        else:
            self._stats_screen = False

    def _call_reveal(self):
        if self._reveal_cards is False:
            self._reveal_cards = True
        else:
            self._reveal_cards = False

    def _call_rulebook(self):
        if bool(self._rulebook) is False:
            self._rulebook = {
                0:Asset.image["rule0.png"],
                1:Asset.image["rule1.png"],
                2:Asset.image["rule2.png"],
                3:Asset.image["rule3.png"],
                4:Asset.image["rule4.png"],
                5:Asset.image["rule5.png"],
                6:Asset.image["rule6.png"],
                7:Asset.image["rule7.png"],
            }
        else:
            self._rulebook = False

    def _flip_forward(self):
        if self._current_page < 7:
            self._current_page += 1

    def _flip_back(self):
        if self._current_page > 0:
            self._current_page -= 1

    # STATES AND UTILITY

    def _open_link(self, link):
        import webbrowser

        webbrowser.open_new_tab(link)

    def _mute(self):
        if Asset._mute_sounds is False:
            Asset._mute_sounds = True
        else:
            Asset._mute_sounds = False

    def _yes_no(self, answer):
        if answer is True:
            self._confirmed = "yes"
        else:
            self._confirmed = "no"


# UTILITARY FUNCTIONS

def blit_text(surface, font, text_input, x, y, relative_to="center", color=WHITE):
    text = font.render(text_input, True, color)
    text_rect = text.get_rect()
    if relative_to == "center":
        text_rect.center = (int(x), int(y))
    elif relative_to == "topright":
        text_rect.topright = (int(x), int(y))
    elif relative_to == "topleft":
        text_rect.topleft = (int(x), int(y))
    elif relative_to == "bottomright":
        text_rect.bottomright = (int(x), int(y))
    elif relative_to == "bottomleft":
        text_rect.bottomleft = (int(x), int(y))
    else:
        text_rect.center = (int(x), int(y))
    surface.blit(text, text_rect)


def blit_image(surface, image, pos, width, height):
    scaled = pygame.transform.smoothscale(image, (int(width), int(height)))
    rect = scaled.get_rect()
    rect.center = pos
    surface.blit(scaled, rect)


def blit_long_text(display, text, pos, font, x_padding=0, color=WHITE):
    """
    Adapted from Ted Klein Bergman on StackOverflow.
    """
    words = [
        word.split(" ") for word in text.splitlines()
    ]  # 2D array where each row is a list of words.
    space = font.size(" ")[0]  # The width of a space.
    max_width, max_height = display.DISP_W, display.DISP_H
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width - x_padding:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            display.WINDOW.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height


def blit_FPS(clock, display):
    HINT = display.HINT * 1.5  # Magic number adjusts sizes without messing positions.
    DISP_W = display.DISP_W
    DISP_H = display.DISP_H
    UBUNTU_S = pygame.font.Font(FONTS_PATH + "ubuntu_regular.otf", int(HINT * 0.05))
    blit_text(
        display.WINDOW,
        UBUNTU_S,
        str(clock.get_fps()),
        DISP_W * 0.01,
        DISP_H * 0.99,
        relative_to="bottomleft",
    )
    pygame.display.update()
