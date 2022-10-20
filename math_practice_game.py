import sys
import pygame as py
import math_game_terminal as mgt
from SceneBase import Scene


class GameScene(Scene):
    def __init__(self):
        super.__init__(self)
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

        self.guess_correct = None

    def ProcessInput(self, events):
        raise NotImplementedError

    def Update(self):
        raise NotImplementedError

    def Render(self, screen):
        raise NotImplementedError


class GameText():
    def __init__(self, font, text, antialias, color, background=None):
        self.font = font
        self.text = text
        self.antialias = antialias
        self.color = color
        self.surface = self.font.render(
            self.text, self.antialias, self.color)
        self.rect = self.surface.get_rect()

    def render(self):
        self.surface = self.font.render(
            self.text, self.antialias, self.color)
        self.rect = self.surface.get_rect()


def evaluate_answer(e):
    answer = mgt.evaluate_products_quotients(e)
    return mgt.evaluate_sum_differences(answer)


def main():
    screen = py.display.set_mode((700, 750))
    clock = py.time.Clock()

    while True:
        for event in py.event.get():
            if event.type == py.QUIT or event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
                # exit case for game
                py.quit()
                sys.exit()
            if event.type == py.KEYDOWN:
                if (len(user_guess) != 0 and user_guess != '-') and event.key == py.K_RETURN:
                    # checks users guess with answer
                    if int(user_guess) == answer[0]:
                        guess_correct = True
                        score += 1
                        score_text.text = 'Score: ' + str(score)
                        score_text.render()
                        score_text.rect.center = (350, 200)
                    else:
                        guess_correct = False
                    user_guess = ''

                    # generate new expression and answer
                    expression_list = mgt.generate_expression(
                        3, ['+', '-'], [1, 10])
                    answer = evaluate_answer(expression_list)

                    expression = mgt.display_expression(
                        expression_list) + ' = ' + str(answer[0])
                    expression_text.text = expression
                    expression_text.render()
                    expression_text.rect.center = (350, 375)
                elif event.key == py.K_BACKSPACE:
                    user_guess = user_guess[:-1]
                elif event.unicode.isnumeric():
                    # only add numeric input
                    user_guess += event.unicode
                elif event.unicode == '-':
                    if len(user_guess) == 0:
                        user_guess = '-'
                    elif user_guess[0] == '-':
                        user_guess = user_guess[1:]
                    else:
                        user_guess = '-' + user_guess
                elif event.unicode == '.':
                    if '.' not in user_guess:
                        user_guess += '.'

        user_text = GameText(base_font, user_guess, False, (0, 0, 0))
        user_text.rect.center = (350, 450)

        screen.fill((255, 255, 255))

        if guess_correct is True:
            screen.blit(correct_text.surface, correct_text.rect)
        elif guess_correct is False:
            screen.blit(incorrect_text.surface, incorrect_text.rect)
        else:
            screen.fill((255, 255, 255))

        screen.blit(expression_text.surface, expression_text.rect)
        screen.blit(user_text.surface, user_text.rect)
        screen.blit(score_text.surface, score_text.rect)

        py.display.update()

        clock.tick(60)


if __name__ == '__main__':
    py.init()
    main()
    sys.exit()
