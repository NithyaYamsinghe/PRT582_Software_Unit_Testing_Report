"""
Guess the Number Game: A simple number guessing game using Python's tkinter.

This module implements a GUI-based number guessing game.
The user enters a number, and the program provides hints
based on the correct digits and positions of the guessed number.

Author: [S370170 - Nithya Romeshika Yamasinghe]
Date: [2023/08/20 S2 2023]
"""
import sys
import random
import tkinter as tk
from tkinter import IntVar, StringVar
from PIL import Image, ImageTk


class GuessNumberGameLogic:
    """
    A class representing the logic behind the Guess the Number game.
    """

    def __init__(self):
        """
            Initializes the GuessNumberGameLogic instance.
        """
        self.attempt = 0
        self.rand_num = random.randint(1000, 9999)

    def guess_number(self, user_input):
        """
        Validates the user's guess and provides feedback.

        Args:
            user_input (int): The user's guessed number.

        Returns:
            Tuple[int, int, bool]: A tuple containing:
                - The number of correct digits
                - The number of correct digits in correct positions
                - A boolean indicating if the guess is correct.
        """
        correct_digit, correct_digit_position = self.calculate_hints(
            user_input
        )
        self.attempt += 1
        is_correct = self.rand_num == user_input
        return correct_digit, correct_digit_position, is_correct

    def calculate_hints(self, user_input):
        """
        Calculates the number of correct digits and
        positions in the user's guess.

        Args:
            user_input (int): The user's guessed number.

        Returns:
            Tuple[int, int]: A tuple containing:
                - The number of correct digits
                - The number of correct digits in correct positions
        """
        correct_digit = 0
        correct_digit_position = 0

        num = str(self.rand_num)
        guess = str(user_input)

        for i, digit in enumerate(guess):
            if digit == num[i]:
                correct_digit_position += 1
            elif digit in num:
                correct_digit += 1

        return correct_digit, correct_digit_position


class GuessNumberGameApp:
    """
    A class representing the graphical user interface
    for the Guess the Number game.
    """
    def __init__(self, root_window, new_logic):
        """
        Initializes the GuessNumberGameApp instance.

        Args:
            root_window: The root window of the Tkinter application.
            new_logic (GuessNumberGameLogic):
            An instance of GuessNumberGameLogic.
        """
        self.root = root_window
        self.logic = new_logic

        self.root.iconbitmap(r'Guess_the_Number_Game\myicon.ico')
        self.root.title('Guess the Number Game')
        self.root.geometry('700x700')
        self.root.config(bg='#FCF3CF')

        self.vars = {
            "user_input": IntVar(),
            "result": StringVar(),
            "message": StringVar()
        }

        # self.var = IntVar()
        # self.result = StringVar()
        # self.message = StringVar()
        self.hint_images = {}

        self.initialize_images()
        self.create_widgets()

    def initialize_images(self):
        """
        Loads and initializes images for hints.
        """
        self.hint_images['circle'] = self.load_resized_image(
            r'Guess_the_Number_Game\circle.png', (140, 80)
        )
        self.hint_images['cross'] = self.load_resized_image(
            r'Guess_the_Number_Game\cross.png', (80, 80)
        )
        self.hint_images['winner'] = self.load_resized_image(
            r'Guess_the_Number_Game\winner.jpg', (200, 160)
        )
        self.hint_images['wronganswer'] = self.load_resized_image(
            r'Guess_the_Number_Game\wronganswer.jpg', (200, 160)
        )

    def validate_input(self, new_value):
        """
        Validates the input to allow only four-digit numbers.

        Args:
            new_value (str): The new value of the input.

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        if new_value == "":
            return True  # Allow deletion

        return new_value.isdigit() and len(new_value) <= 4

    def load_resized_image(self, path, size):
        """
        Loads and resizes an image from the given path.

        Args:
            path (str): The path to the image file.
            size (tuple): The desired dimensions (width, height)
            for the resized image.

        Returns:
            ImageTk.PhotoImage: The resized image as a PhotoImage object.
        """
        open_image = Image.open(path)
        resized_image = open_image.resize(size)
        return ImageTk.PhotoImage(resized_image)

    def create_widgets(self):
        """
        Creates and configures the widgets for
        the application's graphical interface.
        """
        validation = self.root.register(self.validate_input)

        tk.Label(
            self.root,
            text='Guess the Four Digit Number Game',
            font=('Verdana', 22),
            relief=tk.SOLID,
            padx=10,
            pady=10,
            bg='#C39BD3'
        ).pack(pady=(50, 10))

        tk.Entry(
            self.root,
            textvariable=self.vars["user_input"],
            font=('Verdana', 16),
            validate="key",
            validatecommand=(validation, '%P')
        ).pack(pady=(30, 10))

        tk.Button(
            self.root,
            text='Submit',
            background='#ABEBC6',
            font=('Verdana', 18),
            command=self.guess_number
        ).pack(pady=(0, 10))

        tk.Button(
            self.root,
            text='Quit',
            background='#F5B7B1',
            font=('Verdana', 18),
            command=self.quit_game
        ).pack()

        tk.Label(
            self.root,
            textvariable=self.vars["result"],
            font=('Verdana', 14)
        ).pack(pady=(20, 0))

        tk.Label(
            self.root,
            textvariable=self.vars["message"],
            font=('Verdana', 14)
        ).pack(pady=(20, 0))

        self.hint_label_circle = tk.Label(self.root)
        self.hint_label_circle.pack(pady=(20, 0))

        self.hint_label_cross = tk.Label(self.root)
        self.hint_label_cross.pack(pady=(20, 0))

        self.root.protocol('WM_DELETE_WINDOW', self.close_window)

    def guess_number(self):
        """
        Handles user's guess submission.
        """
        user_input = self.vars["user_input"].get()
        correct_digit, correct_digit_position, is_correct = \
            self.logic.guess_number(user_input)

        if is_correct:
            self.handle_correct_guess()
        else:
            self.handle_wrong_guess(correct_digit, correct_digit_position)

    def handle_correct_guess(self):
        """
        Handles the scenario when the user's guess is correct.
        """
        self.hint_label_circle.config(image=self.hint_images['winner'])
        self.hint_label_cross.config(image=empty_image_tk)
        self.show_result_message(
            f'Congratulations! {self.logic.rand_num} is the correct answer.'
        )
        self.vars["message"].set(
            f'You have taken {self.logic.attempt} attempts.'
        )
        self.close_window()

    def handle_wrong_guess(self, correct_digit, correct_digit_position):
        """
        Handles the scenario when the user's guess is incorrect.

        Args:
            correct_digit (int): The number of correct digits
            in the user's guess.
            correct_digit_position (int): The number of correct digits
            in correct positions.
        """
        self.update_hints(correct_digit, correct_digit_position)
        self.show_result_message(
            'Your guess is wrong. You have taken '
            f'{self.logic.attempt} attempts.'
        )

    def update_hints(self, correct_digit, correct_digit_position):
        """
        Updates the hints and feedback based
        on the correctness of the user's guess.

        Args:
        correct_digit (int): The number of correct digits
        in the user's guess.
        correct_digit_position (int): The number of correct digits
        in correct positions.
        """
        hint_message = ''
        if correct_digit_position > 0:
            hint_message += f'{correct_digit_position} x circle'
            self.hint_label_circle.config(image=self.hint_images['circle'])
        else:
            self.hint_label_circle.config(image=empty_image_tk)

        if correct_digit > 0:
            if hint_message:
                hint_message += ' & '
            hint_message += f'{correct_digit} x cross'
            self.hint_label_cross.config(image=self.hint_images['cross'])
        else:
            self.hint_label_cross.config(image=empty_image_tk)

        if not hint_message:
            hint_message = 'You do not have any hints.'
            self.hint_label_circle.config(
                image=self.hint_images['wronganswer']
            )
        self.vars["message"].set(f'Your hint is: {hint_message}')

    def show_result_message(self, msg):
        """
        Displays a message in the result label.

        Args:
            msg (str): The message to be displayed.
        """
        self.vars["result"].set(msg)

    def close_window(self):
        """
        Closes the application window after a delay.
        """
        self.root.after(3000, self.root.quit)

    def quit_game(self):
        """
        Quits the game and exits the application.
        """
        sys.exit(0)


if __name__ == '__main__':
    root = tk.Tk()
    logic = GuessNumberGameLogic()
    app = GuessNumberGameApp(root, logic)
    empty_image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    empty_image_tk = ImageTk.PhotoImage(empty_image)
    root.mainloop()
