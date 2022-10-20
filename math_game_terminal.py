"""
a1.py
Author: Harman Suri - 501098498
Oct 18, 2021
Problem:        Math is somewhat of a tricky subject to get good at and you cannot begin to comprehend
                advanced topics without first learning the basics. In the case of this program the basics
                are inlcude adding, subtracting, multiplying and dividing, as well as using BEDMAS also
                known as the order of operations. This progam tailors more towards kids as it
                only has 4 basic operations, however, becoming proficient at these operations is what
                makes a good foundation for learning other concepts, not to mention it can help brush up
                skills that have been forgotten because of calculaters. In summary, this program solves
                the problem of learning the basics of math by creating randomly generated math expressions
                for the user to solve.
"""

from random import randint, choice


def generate_expression(n, operations, terms):
    """
    Returns a random mathamtical expression with n number of random terms seperated by an operation (+, -, *, /).
    Operations is a list of the operations that will be used in making the expression; for example
    to make the expression easier to evalute enter a list that doesn't have '*' (multiplication) or '/' (division).
    Terms is a list that denotes the range that will give the numbers between each operation; for example if terms is
    only [1, 10] then only 1, 2, ..., 10 will be used in the expression, making the math eaiser.
    """
    # empty list for the expression
    expression = []

    # only loop to 1 less than n, because if we loop to n there will be too many operators for the number of terms
    # example '1 + 2 -'
    for i in range(n - 1):
        # append a random number between the 0th and 1st elemnts of terms to the expression
        expression.append(randint(terms[0], terms[1]))
        # add a random element from the operations list to the expression
        expression += choice(operations)

    # append another random number at the end to have the correct n number of terms
    # if we don't do this there will be a lone operator and not enough numbers
    expression.append(randint(terms[0], terms[1]))

    return expression


def evaluate_products_quotients(expression):
    """
    Takes in an expression and evaluates the mulitplication and division portions of it (2 + 3 * 3 = 2 + 9, 2 + 3 / 3 = 2 + 1).
    After evaluating all products and quotients, a new expression is returned that wouldn't consist of any '*' or '/'.
    This function helps to faciliate the order of operations.
    """

    # keeps looping while there is still a division or multiplication symbol in the expression
    while '/' in expression or '*' in expression:
        # if there is both a division and multiplication, then i is equal to the index of the operation that comes first
        # this is because the order of operations state that you do multiplication and division from left to right
        if '/' in expression and '*' in expression:
            if expression.index('/') < expression.index('*'):
                i = expression.index('/')
            else:
                i = expression.index('*')
        # otherwise if there's only a division or multiplication, then i is the index of whichever one is present
        elif '/' in expression:
            i = expression.index('/')
        else:
            i = expression.index('*')

        if expression[i] == '/':
            # quotient is a list that contains the division of the number before the index of the symbol by the number after
            # it's put in a list to make concatenation possible
            quotient = [expression[i - 1] / expression[i + 1]]
            # expression is then equal to everything before the dividend plus the calculated qoutient, to everything after the divisor
            # this gets rid of the division sign and the numbers part of the calculation with the qoutient
            expression = expression[:i - 1] + quotient + expression[i + 2:]
        else:
            # product is a list that contains the product of the number before the index of the symbol times the number after
            # it's put in a list to make concatenation possible
            product = [expression[i - 1] * expression[i + 1]]
            # expression is then equal to everything before the multiplicand plus the calculated product, to everything after the multiplier
            # this gets rid of the multiplication sign and the numbers part of the calculation with the product
            expression = expression[:i - 1] + product + expression[i + 2:]

    return expression


def evaluate_sum_differences(expression):
    """
    Takes in an expression and evaluates the addition and subtraction portions of it (2 + 9 - 1 = 10). After evaluating
    all sums and differences, a new expression is returned that wouldn't consist of any '+' or '-'. However, as addition
    and subrataction are last in the order of operations, using this function should return the final answer of the original expression.
    """

    # keeps looping while there is still an addition or subtraction symbol in the expression
    while '+' in expression or '-' in expression:
        # if there is both an addition and subtraction, then i is equal to the index of the operation that comes first
        # this is because the order of operations state that you do subtraction and addition from left to right
        if '+' in expression and '-' in expression:
            if expression.index('+') < expression.index('-'):
                i = expression.index('+')
            else:
                i = expression.index('-')
        # otherwise if there's only an addition or subtraction, then i is the index of whichever one is present
        elif '+' in expression:
            i = expression.index('+')
        else:
            i = expression.index('-')

        if expression[i] == '+':
            # total is a list that contains the sum of the number before the index of the symbol with the number after
            # it's put in a list to make concatenation possible
            total = [expression[i - 1] + expression[i + 1]]
            # expression is then equal to everything before the first addend plus the calculated sum, to everything after the second addend
            # this gets rid of the addition sign and the numbers part of the calculation with the sum
            expression = expression[:i - 1] + total + expression[i + 2:]
        elif expression[i] == '-':
            # differnce is a list that contains the difference of the number before the index of the symbol minus the number after
            # it's put in a list to make concatenation possible
            differnce = [expression[i - 1] - expression[i + 1]]
            # expression is then equal to everything before the minuend plus the calculated difference, to everything after the subtrahend
            # this gets rid of the subtraction sign and the numbers part of the calculation with the difference
            expression = expression[:i - 1] + differnce + expression[i + 2:]

    return expression


def display_expression(expression):
    """
    Takes an expression and returns a string that is prettified (i.e instead the format of a list it's just one
    continuous string).
    """

    # display will hold the string form of the expression
    display = ''

    # iterates through all the parts of the expression
    for i in expression:
        # adds the corresponding operations to display, but surrounded with spaces to make it look nicer
        # specifically the division and multiplication symbols are replaced by their actual symbols '÷' and '×'
        if i == '/':
            display += ' ÷ '
        elif i == '*':
            display += ' × '
        elif i == '+' or i == '-':
            display += f' {i} '
        # if i isn't a symbol it must be a number, so the number cast to a string is added to display
        else:
            display += str(i)

    return display


if __name__ == '__main__':
    # 3 variables for the number of terms in the expression, the operations used in the expression
    # and the range of numbers each term is in
    num_terms = 0
    operations = []
    range_terms = [0, 0]
    # ask the user if they want easy, normal, or hard mode, or ask if they want to use advanced options
    user_input = input(
        'WELCOME TO MATH PRACTICE! EASY NORMAL HARD (1, 2 or 3)? ENTER ADV FOR MORE OPTIONS: ')

    # 1 is easy mode
    if user_input == '1':
        # set the number of terms, the kinds of of operations, and the range of the terms
        num_terms = 4
        operations = ['+', '-']
        range_terms = [1, 20]
        # print a message letting the user know what easy mode means
        print('YOU CHOSE EASY MODE! ONLY 4 TERMS RANGING FROM 1 TO 20 WITH ADDITION AND SUBTRACTION!')

    # 2 is normal mode
    elif user_input == '2':
        # set the number of terms, the kinds of of operations, and the range of the terms
        num_terms = 4
        operations = ['+', '-', '*']
        range_terms = [1, 9]
        # print a message letting the user know what normal mode means
        print('YOU CHOSE NORMAL MODE! ONLY 4 TERMS RANGING FROM 1 TO 9 WITH ADDITION, SUBTRACTION AND MULTIPLICATION!')

    # 3 is hard mode
    elif user_input == '3':
        # set the number of terms, the kinds of of operations, and the range of the terms
        num_terms = 4
        operations = ['+', '-', '*', '/']
        range_terms = [1, 9]
        # print a message letting the user know what hard mode means
        print('YOU CHOSE HARD MODE! ONLY 4 TERMS RANGING FROM 1 TO 9 WITH ADDITION, SUBTRACTION, MULTIPLICATION AND DIVISION!')

    # if they type 'adv' in any case it is put into lower so the conditional works no matter what
    # 'adv' is for advanced options where the user can decide how the expression looks themself
    elif user_input.lower() == 'adv':
        # the 4 math operations that work in this program
        default_operations = ['+', '-', '*', '/']

        # ask the user how many terms they want in the expression
        num_terms = int(
            input('HOW MANY TERMS WOULD YOU LIKE IN EACH EXPRESSION?: '))

        # ask the user which operations they want
        print('CHOOSE IF YOU WANT TO INCLUDE ADDITION, SUBTRACTION, MULTIPLICATION OR DIVISION')
        # loops through each default operation asking if they would like it in the expression
        for i in default_operations:
            ops = input(f'WOULD YOU LIKE {i} (Y/N)?: ')
            if ops.lower() == 'y':
                # if they do want the expression the operation is appended to the operations variable
                operations.append(i)

        # ask the user the min and max value for the range of the terms that will appear in their expression
        range_terms[0] = int(input(
            'WHAT IS THE MINIMUM OF THE RANGE OF NUMBERS YOU WOULD LIKE TO INCLUDE (INCLUSIVE)?: '))
        range_terms[1] = int(input(
            'WHAT IS THE MAX OF THE RANGE OF NUMBERS YOU WOULD LIKE TO INCLUDE (INCLUSIVE)?: '))

    else:
        # if a valid option isn't enterd the user is told so and the program ends
        print("Sorry that wasn't an option, enter a valid option next time.")
        exit()

    # varibales to keep track of the players score and if the player wants to continue playing the game
    score = 0
    keep_playing = True

    # continues to loop while the player still wants to play, this means we can continuosly ask the user questions
    while keep_playing:
        # an expression by calling the function and passing in all the defined arguments
        expression = generate_expression(num_terms, operations, range_terms)

        # first answer is equal to an expression that has all the multiplication and division done
        answer = evaluate_products_quotients(expression)

        # then answer is equal to an expression that has all the addition and subraction done
        # as addition and subtraction are the last step there is only a single term left in a list
        # so we index the list to take out the answer while also rounding it to 3 decimal spots
        answer = round(evaluate_sum_differences(answer)[0], 3)

        # tell the player if they what to stop playing type exit when prompted
        print('TO STOP PLAYING ENTER EXIT!')
        # ask the player for their answer to the expression, this is also where they can exit the game
        user_guess = input(
            f'WHAT DOES {display_expression(expression)} EVALUATE TO (ROUND FINAL ANSWER TO 3 DECIMAL PLACES)?: ')

        # if they enter exit then keep_playing is false the loop will stop
        if user_guess.lower() == 'exit':
            keep_playing = False
        elif float(user_guess) == answer:
            # otherwise if their answer was correct they're told so and 1 is added to their score
            score += 1
            print(f'{user_guess} WAS CORRECT!')
            print('SCORE:', score)
        else:
            # if their answer was wrong then they are told so
            print(f'{user_guess} WAS WRONG\nTHE ANSER WAS {answer}!')
            print('SCORE:', score)

    # when they exit the game loop they're given their final score
    print('YOUR FINAL SCORE WAS:', score, '\nTHANKS FOR PLAYING!')
