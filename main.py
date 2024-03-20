import sys

from cards import *

SCREEN_SIZE = (1410, 550)
CENTER_POS = tuple(map(lambda a: a / 2, SCREEN_SIZE))
FRAME_RATE = 24
BG_COLOR = "green4"
WINDOW_TITLE = "神経衰弱"
CARD_BACK_PATH = "assets/img/cardBack.png"
REPLAY_BTN_PATH = "assets/img/replay.png"
FLIP_SOUND_PATH = "assets/sound/flip.mp3"
CORRECT_SOUND_PATH = "assets/sound/correct.mp3"
CLEAR_SOUND_PATH = "assets/sound/clear.mp3"
MISS_SOUND_PATH = "assets/sound/miss.mp3"
BUTTON_SOUND_PATH = "assets/sound/button.mp3"


def game_shutdown():
    pg.quit()
    sys.exit()


def main():
    pg.init()
    card_lists = init_cards()
    card_len = sum(len(i) for i in card_lists)
    screen = pg.display.set_mode(size=SCREEN_SIZE)
    pg.display.set_caption(title=WINDOW_TITLE)
    card_back_surface = pg.image.load(CARD_BACK_PATH)
    pg.display.set_icon(card_back_surface)
    opened_cards = []
    font = pg.font.Font(None, 130)
    clear_text_surface = font.render("Cleared!", True, pg.Color("RED"))
    clear_text_rect = clear_text_surface.get_rect(center=CENTER_POS)
    replay_btn_surface = pg.image.load(REPLAY_BTN_PATH)
    replay_btn_rect = replay_btn_surface.get_rect(center=(CENTER_POS[0], CENTER_POS[1] + 200))
    cleared_card = 0
    clear_sound = pg.mixer.Sound(CLEAR_SOUND_PATH)
    miss_sound = pg.mixer.Sound(MISS_SOUND_PATH)
    correct_sound = pg.mixer.Sound(CORRECT_SOUND_PATH)
    flip_sound = pg.mixer.Sound(FLIP_SOUND_PATH)
    button_sound = pg.mixer.Sound(BUTTON_SOUND_PATH)
    is_cleared = False
    while True:
        try:
            screen.fill(pg.Color(BG_COLOR))
            m_down = pg.mouse.get_pressed()
            mouse_pos = pg.mouse.get_pos()
            if is_cleared:
                screen.blit(clear_text_surface, clear_text_rect)
                btn = screen.blit(replay_btn_surface, replay_btn_rect)
                if m_down[0]:
                    if btn.collidepoint(mouse_pos):
                        button_sound.play()
                        is_cleared = False
                        cleared_card = 0
                        card_lists = init_cards()
                pass
            else:
                for col in card_lists:
                    for card in col:
                        if card.is_cleared:
                            continue
                        target_rect = screen.blit(card.surface, card.rect)
                        if card in opened_cards:
                            continue
                        if m_down[0] and target_rect.collidepoint(mouse_pos):
                            card.open_card()
                            screen.blit(card.surface, card.rect)
                            flip_sound.play()
                            if len(opened_cards) < 2:
                                opened_cards.append(card)
            pg.display.update()
            pg.time.Clock().tick(FRAME_RATE)
            if len(opened_cards) == 2:
                pg.time.wait(500)
                if opened_cards[0].SCORE == opened_cards[1].SCORE:
                    for card in opened_cards:
                        card.clear_card()
                        cleared_card += 1
                    if cleared_card >= card_len:
                        is_cleared = True
                        clear_sound.play()
                    else:
                        correct_sound.play()
                else:
                    for card in opened_cards:
                        card.hide_card()
                    miss_sound.play()
                opened_cards.clear()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_shutdown()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        game_shutdown()
        except KeyboardInterrupt:
            print("shutdown by keyboard input")
            game_shutdown()
    pass


if __name__ == "__main__":
    main()
