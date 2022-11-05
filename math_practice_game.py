import sys
import pygame as py
import math_game_terminal as mgt
from SceneBase import Scene


def wrap_text(screen, font, text, pos, max_width):
    """
    renders lines of text to screen, going to a new line to
    prevent exceeding max width

    param screen: destentation to render text
    param font: pygame.font.Font object, used to create text surface
    param text: text to be rendered
    param pos: position to where text should be rendered (topleft)
    param max_width: defines max width of a single line of text, before newline
    """
    words = text.split()
    line = ''
    line_width = 0
    offset = 0

    while len(words):
        line += words.pop(0) + ' '
        line_surf = font.render(line, False, (0, 0, 0))
        line_width = line_surf.get_width()

        if line_width > max_width or len(words) == 0:
            screen.blit(line_surf, (pos[0], pos[1] + offset))
            offset += line_surf.get_size()[1] + 10
            line = ''
            line_width = 0


class MenuScene(Scene):
    """
    Creates a Scene for the menu, includes all variables for displayed text
    and options for player
    """

    def __init__(self):
        """
        Initialize all variables for displayed text, buttons and input boxes.
        """
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
        self.operations_text.rect.midleft = (50, 445)

        self.selected_ops_text = GameText(
            self.main_font, "Selected Operations: ", False, (0, 0, 0))

        self.dash_text = GameText(self.main_font, "-", False, (0, 0, 0))
        self.dash_text.rect.midleft = (425, 300)

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

        # input boxes for all game options
        self.num_terms_input = InputBox(
            py.Rect((350, 180), (40, 40)), (200, 200, 200), (100, 100, 100), self.main_font, 2)
        self.min_range_input = InputBox(
            py.Rect((350, 280), (40, 40)), (200, 200, 200), (100, 100, 100), self.main_font, 3)
        self.max_range_input = InputBox(
            py.Rect((450, 280), (40, 40)), (200, 200, 200), (100, 100, 100), self.main_font, 3)

    def ProcessInput(self, events):
        """
        Takes events from game loop and handles them as needed in the Menu.

        param events: pygame events passed in from game loop
        """

        # get all inputted options from player and save in separate variables
        # set to 0 if no input was given
        num_terms = int(
            self.num_terms_input.text) if self.num_terms_input.text else 0
        min_range = int(
            self.min_range_input.text) if self.min_range_input.text else 0
        max_range = int(
            self.max_range_input.text) if self.max_range_input.text else 0
        term_range = [min_range, max_range] if min_range < max_range else []

        # if all inputs were given this will be True
        input_given = num_terms and term_range

        for e in events:
            if e.type == py.MOUSEBUTTONDOWN:
                if self.apply_button.click_handler(e.pos) and input_given:
                    # switch to GameScene, passing in options, only if all options are given
                    self.SwitchToScene(
                        GameScene(self.operations, num_terms, term_range))
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
            # given event, process inputs for all input boxes
            self.num_terms_input.ProcessInput(e)
            self.min_range_input.ProcessInput(e)
            self.max_range_input.ProcessInput(e)

    def Update(self):
        pass

    def Render(self, screen):
        """
        Render all text, buttons and input boxes to given surface.

        param screen: a pygame display that is passed in from main.
        """

        screen.fill((255, 255, 255))

        # render all buttons
        self.plus_button.Render(screen)
        self.minus_button.Render(screen)
        self.multiply_button.Render(screen)
        self.divide_button.Render(screen)
        self.apply_button.Render(screen)

        # render all inputs boxes
        self.num_terms_input.Render(screen)
        self.min_range_input.Render(screen)
        self.max_range_input.Render(screen)

        # add selected operations to respective text object
        self.selected_ops_text.text = "Selected Operations: " + \
            mgt.display_expression(self.operations)
        self.selected_ops_text.render()
        self.selected_ops_text.rect.topleft = (50, 550)

        # display all text on screen
        screen.blit(self.title_text.surface, self.title_text.rect)
        screen.blit(self.n_terms_text.surface, self.n_terms_text.rect)
        screen.blit(self.range_text.surface, self.range_text.rect)
        screen.blit(self.operations_text.surface, self.operations_text.rect)
        screen.blit(self.selected_ops_text.surface,
                    self.selected_ops_text.rect)
        screen.blit(self.dash_text.surface, self.dash_text.rect)


class GameScene(Scene):
    """
    Creates a Scene for the main game, includes all variables for displayed text,
    including math expression and score, and ability for player to enter answer.
    """

    def __init__(self, operations, num_terms, term_range):
        """
        Initialize all variables for displayed text and game variables.
        """
        super(GameScene, self).__init__()
        self.ops = operations
        self.num_terms = num_terms
        self.term_range = term_range

        # font for all text
        self.base_font = py.font.Font(None, 100)
        self.answer_font = py.font.Font(None, 50)

        self.expression_list = mgt.generate_expression(
            self.num_terms, self.ops, self.term_range)
        # answer of the expression
        self.answer = round(evaluate_answer(self.expression_list)[0], 2)

        self.answer_text = GameText(
            self.answer_font, "ANSWER WAS", False, (0, 0, 0))
        self.answer_text.rect.center = (350, 110)

        # expression put into a string
        self.expression = mgt.display_expression(
            self.expression_list) + ' = ?'
        # text objects for expression
        self.expression_text = GameText(
            self.base_font, self.expression, False, (0, 0, 0))
        self.expression_text.rect.center = (350, 375)

        # correct text
        self.correct_text = GameText(
            self.base_font, 'CORRECT!', False, (0, 255, 0))
        self.correct_text.rect.center = (350, 50)

        # incorrect text
        self.incorrect_text = GameText(
            self.base_font, 'INCORRECT!', False, (255, 0, 0))
        self.incorrect_text.rect.center = (350, 50)

        # score text
        self.score = 0
        self.score_text = GameText(
            self.base_font, 'Score: ' + str(self.score), False, (0, 0, 0))
        self.score_text.rect.center = (350, 200)

        # user guess text
        self.user_guess = ''
        self.user_text = GameText(
            self.base_font, self.user_guess, False, (0, 0, 0))
        self.user_text.rect.center = (350, 690)

        self.guess_correct = None

    def ProcessInput(self, events):
        """
        Takes events from game loop and handles them as needed in the Game.

        param events: pygame events passed in from game loop
        """
        for e in events:
            if e.type == py.KEYDOWN:
                if e.key == py.K_ESCAPE:
                    # go back to Menu if escape it pressed
                    self.SwitchToScene(MenuScene())
                elif (len(self.user_guess) != 0 and self.user_guess != '-') and e.key == py.K_RETURN:
                    # checks users guess with answer
                    if float(self.user_guess) == self.answer:
                        self.guess_correct = True
                        # if correct update score
                        self.score += 1
                        self.score_text.text = 'Score: ' + str(self.score)
                    else:
                        self.guess_correct = False

                    self.answer_text.text = f'ANSWER WAS {self.answer}'
                    # regardless of correctness of guess, reset guess text
                    self.user_guess = ''

                    # generate new expression and answer
                    self.expression_list = mgt.generate_expression(
                        self.num_terms, self.ops, self.term_range)
                    self.answer = round(evaluate_answer(
                        self.expression_list)[0], 2)

                    self.expression = mgt.display_expression(
                        self.expression_list) + ' = ?'
                    self.expression_text.text = self.expression

                elif e.key == py.K_BACKSPACE:
                    # delete one character in user's guess
                    self.user_guess = self.user_guess[:-1]
                elif e.unicode.isnumeric():
                    # only add numeric input
                    self.user_guess += e.unicode
                elif e.unicode == '-':
                    # make the user guess negative
                    if len(self.user_guess) == 0:
                        self.user_guess = '-'
                    elif self.user_guess[0] == '-':
                        # if user_guess is already negative remove negative
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
        """
        Render all text to given surface.

        param screen: a pygame display that is passed in from main.
        """

        # render all GameText objects and change positioning of GameText rects
        self.answer_text.render()
        self.answer_text.rect.center = (350, 110)

        self.score_text.render()
        self.score_text.rect.center = (350, 200)

        self.expression_text.render()
        self.expression_text.rect.center = (350, 375)

        self.user_text.render()
        self.user_text.rect.center = (350, 690)

        # display corresponding text depending on correctness of guess
        if self.guess_correct is True:
            screen.blit(self.correct_text.surface, self.correct_text.rect)
        elif self.guess_correct is False:
            screen.blit(self.incorrect_text.surface, self.incorrect_text.rect)
        else:
            # if it's the first guess don't display correct or incorrect text
            screen.fill((255, 255, 255))

        # display all text on screen

        # use wrap_text for expression_text, to stop it from going off screen
        wrap_text(screen, self.base_font,
                  self.expression_text.text, (40, 250), 590)

        screen.blit(self.answer_text.surface, self.answer_text.rect)
        screen.blit(self.user_text.surface, self.user_text.rect)
        screen.blit(self.score_text.surface, self.score_text.rect)


class GameText():
    """
    Class that stores all necessary aspects to display pygame text.
    """

    def __init__(self, font, text, antialias, colour):
        """
        Creates GameText() object with necessary variables

        param font: font to render render text from
        param text: text to render
        param antialias: boolean, if True characters will have smooth edges
        param colour: the colour of the text when it is rendered
        """
        self.font = font
        self.text = text
        self.antialias = antialias
        self.colour = colour

        # get surface of text from font.render and rect from said surface
        self.surface = self.font.render(
            self.text, self.antialias, self.colour)
        self.rect = self.surface.get_rect()

    def render(self):
        """
        To be used after text is changed. Reset surface and rect to be based
        on newly given text.
        """
        self.surface = self.font.render(
            self.text, self.antialias, self.colour)
        self.rect = self.surface.get_rect()


class RectButton():
    """
    Class for a pygame rectangular button.
    """

    def __init__(self, font, pos, background, text_colour, text=""):
        """
        Creates a RectButton() object with necessary variables

        param font: font to render button text from
        param pos: position to draw button at (topleft coordinate)
        param background: colour of button rectangle
        param text: text inside button, default is empty string
        """
        self.font = font
        self.pos = pos
        self.background = background

        # make use of GameText object to store text for button
        self.text = GameText(self.font, text, False, text_colour)
        self.text.rect.topleft = self.pos

    def click_handler(self, mouse_pos):
        """
        Detects if the button is clicked on

        param mouse_pos: the position of the mouse during the click
        """
        if self.text.rect.collidepoint(mouse_pos):
            return True

        return False

    def Render(self, screen):
        """
        Render button text and draw rectangle to given surface.

        param screen: a pygame display.
        """
        py.draw.rect(screen, self.background, self.text.rect)
        screen.blit(self.text.surface, self.text.rect)


class InputBox():
    """
    Class for a pygame text input box.
    """

    def __init__(self, rect, active_colour, passive_colour, font, text_limit=None):
        """
        Creates a InputBox() object with necessary variables

        param rect: pygame.Rect that defines the size and position of the input box
        param active_colour: the colour of the InputBox when it's in use
        param passive_colour: the colour of the InputBox when it isn't in use
        param font: font to render inputted text from
        param text_limit: the max number of character allowed in the InputBox,
                            default to None
        """
        self.rect = rect
        self.active_colour = active_colour
        self.passive_colour = passive_colour

        self.colour = self.passive_colour
        self.active = False

        self.font = font
        self.text = ''
        self.text_limit = text_limit

    def ProcessInput(self, event):
        """
        Handles clicks on the InputBox and text input.

        param events: a pygame event
        """

        # checks if the InputBox has been clicked into
        if event.type == py.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == py.KEYDOWN and self.active:
            # remove a character on backspace
            if event.key == py.K_BACKSPACE:
                self.text = self.text[:-1]
            # only enter text if it's a digit and the if text_limit is not exceeded
            elif event.unicode.isdigit() and (self.text_limit is None or len(self.text) < self.text_limit):
                self.text += event.unicode

    def Render(self, screen):
        """
        Render InputBox text and draw rectangle to given surface.

        param screen: a pygame display.
        """
        # set colour of InputBox rect if it's active or not
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
        self.rect.w = max(self.rect.w, text_surface.get_width() + 10)


def evaluate_answer(exp):
    """
    Evaluate the answer of an expression

    param exp: a math expression created from mgt.generate_expression
    """
    answer = mgt.evaluate_products_quotients(exp)
    return mgt.evaluate_sum_differences(answer)


def main():
    """
    main function that handles creation of display and game loop.
    """
    screen = py.display.set_mode((700, 750))
    clock = py.time.Clock()

    # keeps track of which scene the game is in
    active_scene = MenuScene()

    while True:
        active_scene = active_scene.next

        # all events that should be passed into Scene.ProcessInput()
        filtered_events = []
        for e in py.event.get():
            if e.type == py.QUIT:
                # exit case for game
                py.quit()
                sys.exit()
            else:
                filtered_events.append(e)

        screen.fill((255, 255, 255))

        # call all Scene methods to handle events and render to screen
        active_scene.ProcessInput(filtered_events)
        active_scene.Update()
        active_scene.Render(screen)

        py.display.update()

        clock.tick(60)


if __name__ == '__main__':
    py.init()
    main()
