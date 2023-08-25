"""
Unit tests for Guess the Number Game.

This module contains unit tests for the classes and methods in the Guess
the Number Game application.
It uses the `unittest` framework to define and run test cases
to ensure the correctness of the
application's logic and user interface components.

To run these tests, execute this script using a Python interpreter.

Note: The tests are written based on the assumptions and behavior of
the code in the 'main' module
      (not shown here).

Author: [S370170 - Nithya Romeshika Yamasinghe]
Date: [2023/08/20 S2 2023]
"""

# pylint: disable=arguments-differ
import unittest
from unittest.mock import patch, Mock
import tkinter as tk
from main import GuessNumberGameLogic, GuessNumberGameApp


class TestGuessNumberGameLogic(unittest.TestCase):
    """Test cases for GuessNumberGameLogic class."""

    @patch('main.random.randint')
    def setUp(self, mock_randint):
        mock_randint.return_value = 1234
        self.logic = GuessNumberGameLogic()

    # Test case: Testing all correct digits and positions
    def test_calculate_hints_all_correct(self):
        """Set up the test environment for GuessNumberGameLogic tests."""
        # Verify the hints calculation for a guess with all
        # correct digits and positions
        correct_digit, correct_digit_position = self.logic.calculate_hints(
            1234
        )
        self.assertEqual(correct_digit, 0)
        self.assertEqual(correct_digit_position, 4)

    # Test case: Testing some correct digits and positions
    def test_calculate_hints_some_correct(self):
        """Test calculation of hints for correct digits and positions."""
        # Verify the hints calculation for a guess with
        # some correct digits and positions
        correct_digit, correct_digit_position = self.logic.calculate_hints(
            1324
        )
        self.assertEqual(correct_digit, 2)
        self.assertEqual(correct_digit_position, 2)

    # Test case: Testing no correct digits
    def test_calculate_hints_no_correct(self):
        """Test calculation of hints for no correct digits."""
        # Verify the hints calculation for a guess with no correct digits
        correct_digit, correct_digit_position = self.logic.calculate_hints(
            5678
        )
        self.assertEqual(correct_digit, 0)
        self.assertEqual(correct_digit_position, 0)

    # Test case: Testing mixed correct digits and positions
    def test_calculate_hints_mixed_correct(self):
        """Test calculation of hints for mixed correct digits and positions."""
        # Verify the hints calculation for a guess
        # with mixed correct digits and positions
        correct_digit, correct_digit_position = self.logic.calculate_hints(
            1243
        )
        self.assertEqual(correct_digit, 2)
        self.assertEqual(correct_digit_position, 2)

    # Test case: Testing all correct positions, but not all correct digits
    def test_calculate_hints_all_correct_positions(self):
        """Test calculation of hints for all correct positions
        but different digits."""
        # Verify the hints calculation for a guess with
        # all correct positions but different digits
        correct_digit, correct_digit_position = self.logic.calculate_hints(
            4321
        )
        self.assertEqual(correct_digit, 4)
        self.assertEqual(correct_digit_position, 0)

    # Test case: Testing mixed correct positions and digits
    def test_calculate_hints_mixed_correct_positions(self):
        """Test calculation of hints for mixed correct positions and digits."""
        # Verify the hints calculation for a guess with
        # mixed correct positions and digits
        correct_digit, correct_digit_position = self.logic.calculate_hints(
            1435
        )
        self.assertEqual(correct_digit, 1)
        self.assertEqual(correct_digit_position, 2)

    # Test case: Testing when user input has duplicate digits
    def test_calculate_hints_duplicate_digits(self):
        """Test calculation of hints for input with duplicate digits."""
        # Verify the hints calculation for a guess with duplicate digits
        correct_digit, correct_digit_position = self.logic.calculate_hints(
            1122
        )
        self.assertEqual(correct_digit, 3)
        self.assertEqual(correct_digit_position, 1)

    # Test case: Testing when user input is the same as the random number
    def test_calculate_hints_same_number(self):
        """Test calculation of hints for input matching the random number."""
        # Verify the hints calculation for a
        # guess that matches the random number
        correct_digit, correct_digit_position = self.logic.calculate_hints(
            1234
        )
        self.assertEqual(correct_digit, 0)
        self.assertEqual(correct_digit_position, 4)


class TestGuessNumberGameApp(unittest.TestCase):
    """Test cases for GuessNumberGameApp class."""
    def setUp(self):
        """Set up the test environment for GuessNumberGameApp tests."""
        self.root = tk.Tk()  # Create the root window
        self.logic = GuessNumberGameLogic()
        self.app = GuessNumberGameApp(self.root, self.logic)

    # Test case: Validate valid input values
    def test_validate_input_valid(self):
        """Test validation of valid input values."""
        valid_inputs = ["1234", "5678", ""]
        for input_value in valid_inputs:
            result = self.app.validate_input(input_value)
            self.assertTrue(result)

    # Test case: Validate invalid input values
    def test_validate_input_invalid(self):
        """Test validation of invalid input values."""
        invalid_inputs = ["12a3", "12345", "00001"]
        for input_value in invalid_inputs:
            result = self.app.validate_input(input_value)
            self.assertFalse(result)

    # Test case: Verify hints calculation and UI updates
    def test_calculate_hints(self):
        """Test calculation of hints and UI updates."""
        self.logic.rand_num = 1234
        correct_digit, correct_digit_position = self.logic.calculate_hints(
            1243
        )
        self.assertEqual(correct_digit, 2)
        self.assertEqual(correct_digit_position, 2)

    # Test case: Handle wrong guess - verify UI updates
    def test_handle_wrong_guess(self):
        """Test handling of wrong guess and UI updates."""
        self.app.update_hints = Mock()
        self.app.show_result_message = Mock()
        self.app.handle_wrong_guess(1, 2)
        self.app.update_hints.assert_called_once_with(1, 2)
        self.app.show_result_message.assert_called_once()

    # Test case: Update hints UI elements
    def test_update_hints(self):
        """Test updating hints UI elements."""
        self.app.hint_label_circle.config = Mock()
        self.app.hint_label_cross.config = Mock()
        self.app.vars["message"].set = Mock()
        self.app.update_hints(2, 1)
        self.app.hint_label_circle.config.assert_called_once()
        self.app.hint_label_cross.config.assert_called_once()
        self.app.vars["message"].set.assert_called_once()

    # Test case: Close the application window
    def test_close_window(self):
        """Test closing the application window."""
        self.app.root.quit = Mock()
        self.app.root.after = Mock()
        self.app.close_window()
        self.app.root.after.assert_called_once()
        self.app.root.quit.assert_not_called()

    # Test case: Quit the game (exit the application)
    def test_quit_game(self):
        """Test quitting the game (exit the application)."""
        with self.assertRaises(SystemExit):
            self.app.quit_game()

    def tearDown(self):
        """Tear down the test environment for GuessNumberGameApp tests."""
        self.root.destroy()  # Close the root window


if __name__ == '__main__':
    unittest.main()
