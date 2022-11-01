import sys
import pygame as py
import math_game_terminal as mgt
from SceneBase import Scene


class MenuScene(Scene):
    def __init__(self):
        super(MenuScene, self).__init__()
        # fonts for menu
        self.title_font = py.font.Font(None, 100)
        self.main_font = py.font.Font(None, 50)

        # text objects for options
        self.title_text = GameText(
            self.title_font, "OPTIONS", False, (0, 0, 0))
        self.title_text.rect.center = (350, 100)

        self.n_terms_text = GameText(
            self.main_font, "Number of terms:", False, (0, 0, 0))
        self.n_terms_text.rect.midleft = (50, 200)

        self.range_text = GameText(
            self.main_font, "Range of terms:", False, (0, 0, 0))
        self.range_text.rect.midleft = (50, 300)

        self.operations_text = GameText(
            self.main_font, "Operations:", False, (0, 0, 0))
        self.operations_text.rect.midleft = (50, 400)

        self.selected_ops_text = GameText(
            self.main_font, "Selected Operations: ", False, (0, 0, 0))

        # buttons for operations
        self.plus_button = RectButton(
            self.title_font, (70, 450), (255, 255, 255), (0, 0, 0), "+")
        self.minus_button = RectButton(
            self.title_font, (180, 450), (255, 255, 255), (0, 0, 0), "-")
        self.multiply_button = RectButton(
            self.title_font, (290, 450), (255, 255, 255), (0, 0, 0), "×")
        self.divide_button = RectButton(
            self.title_font, (400, 450), (255, 255, 255), (0, 0, 0), "÷")

        self.apply_button = RectButton(
            self.title_font, (250, 650), (255, 255, 255), (0, 0, 0), "APPLY")

        self.operations = []

    def ProcessInput(self, events):
        for e in events:
            if e.type == py.MOUSEBUTTONDOWN:
                if self.apply_button.click_handler(e.pos):
                    self.SwitchToScene(GameScene())
                # depending on which button is clicked on
                # add or remove respective operation from list
                elif self.plus_button.click_handler(e.pos):
                    if '+' in self.operations:
                        self.operations.remove('+')
                    else:
                        self.operations.append('+')
                elif self.minus_button.click_handler(e.pos):
                    if '-' in self.operations:
                        self.operations.remove('-')
                    else:
                        self.operations.append('-')
                elif self.multiply_button.click_handler(e.pos):
                    if '*' in self.operations:
                        self.operations.remove('*')
                    else:
                        self.operations.append('*')
                elif self.divide_button.click_handler(e.pos):
                    if '/' in self.operations:
                        self.operations.remove('/')
                    else:
                        self.operations.append('/')

    def Update(self):
        pass

    def Render(self, screen):
        screen.fill((255, 255, 255))
        self.plus_button.Render(screen)
        self.minus_button.Render(screen)
        self.multiply_button.Render(screen)
        self.divide_button.Render(screen)
        self.apply_button.Render(screen)

        # add selected operations to resepective text object
        self.selected_ops_text.text = "Selected Operations: " + \
            mgt.display_expression(self.operations)
        self.selected_ops_text.render()
        self.selected_ops_text.rect.topleft = (50, 550)

        screen.blit(self.title_text.surface, self.title_text.rect)
        screen.blit(self.n_terms_text.surface, self.n_terms_text.rect)
        screen.blit(self.range_text.surface, self.range_text.rect)
        screen.blit(self.operations_text.surface, self.operations_text.rect)
        screen.blit(self.selected_ops_text.surface,
                    self.selected_ops_text.rect)


class GameScene(Scene):
    def __init__(self):
        super(GameScene, self).__init__()
        # basic font for all text
        self.base_font = py.font.Font(None, 100)
        self.expression_list = mgt.generate_expression(3, ['+', '-'], [1, 10])
        # answer of the expression
        self.answer = evaluate_answer(self.expression_list)

        # expression put into a string
        self.expression = mgt.display_expression(
            self.expression_list) + ' = ' + str(self.answer[0])
        # text objects for expression
        self.expression_text = GameText(
            self.base_font, self.expression, False, (0, 0, 0))
        self.expression_text.rect.center = (350, 375)

        # correct text
        self.correct_text = GameText(
            self.base_font, 'CORRECT!', False, (0, 255, 0))
        self.correct_text.rect.center = (350, 100)

        # incorrect text
        self.incorrect_text = GameText(
            self.base_font, 'INCORRECT!', False, (255, 0, 0))
        self.incorrect_text.rect.center = (350, 100)

        # score text
        self.score = 0
        self.score_text = GameText(
            self.base_font, 'Score: ' + str(self.score), False, (0, 0, 0))
        self.score_text.rect.center = (350, 200)

        self.user_guess = ''
        self.user_text = GameText(
            self.base_font, self.user_guess, False, (0, 0, 0))
        self.user_text.rect.center = (350, 450)

        self.guess_correct = None

    def ProcessInput(self, events):
        for e in events:
            if e.type == py.KEYDOWN:
                if e.key == py.K_ESCAPE:
                    self.SwitchToScene(MenuScene())
                elif (len(self.user_guess) != 0 and self.user_guess != '-') and e.key == py.K_RETURN:
                    # checks users guess with answer
                    if int(self.user_guess) == self.answer[0]:
                        self.guess_correct = True
                        self.score += 1
                        self.score_text.text = 'Score: ' + str(self.score)
                    else:
                        self.guess_correct = False

                    # regardless of correctness of guess, reset guess text
                    self.user_guess = ''

                    # generate new expression and answer
                    self.expression_list = mgt.generate_expression(
                        3, ['+', '-'], [1, 10])
                    self.answer = evaluate_answer(self.expression_list)

                    self.expression = mgt.display_expression(
                        self.expression_list) + ' = ' + str(self.answer[0])
                    self.expression_text.text = self.expression
                elif e.key == py.K_BACKSPACE:
                    self.user_guess = self.user_guess[:-1]
                elif e.unicode.isnumeric():
                    # only add numeric input
                    self.user_guess += e.unicode
                elif e.unicode == '-':
                    # make the user guess negative
                    if len(self.user_guess) == 0:
                        self.user_guess = '-'
                    elif self.user_guess[0] == '-':
                        self.user_guess = self.user_guess[1:]
                    else:
                        self.user_guess = '-' + self.user_guess
                elif e.unicode == '.':
                    # add a decimal to the guess
                    if '.' not in self.user_guess:
                        self.user_guess += '.'

        # update the text in user_text
        self.user_text = GameText(
            self.base_font, self.user_guess, False, (0, 0, 0))

    def Update(self):
        pass

    def Render(self, screen):
        # render all GameText objects and change positioning of GameText rects
        self.score_text.render()
        self.score_text.rect.center = (350, 200)

        self.expression_text.render()
        self.expression_text.rect.center = (350, 375)

        self.user_text.render()
        self.user_text.rect.center = (350, 450)

        # display corresponding text depending on correctness of guess
        if self.guess_correct is True:
            screen.blit(self.correct_text.surface, self.correct_text.rect)
        elif self.guess_correct is False:
            screen.blit(self.incorrect_text.surface, self.incorrect_text.rect)
        else:
            # if it's the first guess don't display correct or incorrect text
            screen.fill((255, 255, 255))

        # display all text on screen
        screen.blit(self.expression_text.surface, self.expression_text.rect)
        screen.blit(self.user_text.surface, self.user_text.rect)
        screen.blit(self.score_text.surface, self.score_text.rect)


class GameText():
    def __init__(self, font, text, antialias, colour):
        self.font = font
        self.text = text
        self.antialias = antialias
        self.colour = colour
        self.surface = self.font.render(
            self.text, self.antialias, self.colour)
        self.rect = self.surface.get_rect()

    def render(self):
        self.surface = self.font.render(
            self.text, self.antialias, self.colour)
        self.rect = self.surface.get_rect()


class RectButton():
    def __init__(self, font, pos, background, text_colour, text=""):
        self.font = font
        self.pos = pos
        self.background = background
        self.text = GameText(self.font, text, False, text_colour)
        self.text.rect.topleft = self.pos
        self.rect = py.Rect(self.pos, self.text.surface.get_size())

    def click_handler(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True

        return False

    def Render(self, screen):
        py.draw.rect(screen, self.background, self.rect)
        screen.blit(self.text.surface, self.text.rect)


class InputBox():
    def __init__(self, rect, active_colour, passive_colour, font, text_limit=None):
        self.rect = rect
        self.active_colour = active_colour
        self.passive_colour = passive_colour

        self.colour = self.passive_colour
        self.active = False

        self.font = font
        self.text = ''
        self.text_limit = text_limit

    def ProcessInput(self, events):
        for event in events:
            if event.type == py.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

            if event.type == py.KEYDOWN and self.active:
                if event.key == py.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode.isdigit() and (self.text_limit is None or len(self.text) < self.text_limit):
                    self.text += event.unicode

    def Render(self, screen):
        if self.active:
            self.colour = self.active_colour
        else:
            self.colour = self.passive_colour

        # draw rectangle and argument passed which should
        py.draw.rect(screen, self.colour, self.rect)

        text_surface = self.font.render(self.text, True, (255, 255, 255))

        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        self.rect.w = max(100, text_surface.get_width() + 10)


def evaluate_answer(e):
    answer = mgt.evaluate_products_quotients(e)
    return mgt.evaluate_sum_differences(answer)


def main():
    screen = py.display.set_mode((700, 750))
    clock = py.time.Clock()

    active_scene = GameScene()

    while True:
        active_scene = active_scene.next
        filtered_events = []
        for e in py.event.get():
            if e.type == py.QUIT:
                # exit case for game
                py.quit()
                sys.exit()
            else:
                filtered_events.append(e)

        screen.fill((255, 255, 255))

        active_scene.ProcessInput(filtered_events)
        active_scene.Update()
        active_scene.Render(screen)

        py.display.update()

        clock.tick(60)


if __name__ == '__main__':
    py.init()
    main()
    sys.exit()
