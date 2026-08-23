import math
from dataclasses import dataclass
from typing import Any, Callable, Optional, Tuple


@dataclass
class Validator:
    parser: Callable[[str], Any]
    is_valid: Callable[[Any], Tuple[bool, Any]]
    error_message: str = "Invalid input"
    max_attempts: Optional[int] = None

    def prompt(self, prompt_text: str):
        attempts = 0

        while True:
            if self.max_attempts is not None and attempts >= self.max_attempts:
                raise ValueError("Maximum number of attempts reached.")

            try:
                raw = input(prompt_text)
            except (EOFError, KeyboardInterrupt):
                raise

            attempts += 1

            try:
                value = self.parser(raw)
            except (TypeError, ValueError, OverflowError):
                print(self.error_message)
                continue

            valid, result = self.is_valid(value)
            if valid:
                return result

            print(result if isinstance(result, str) else self.error_message)


# ==================== STRING ====================
def get_str(prompt="Text: ", *, max_length=50, name=False, allow_empty=False):
    """
    Asks the user for a string until a valid one is given.

    If name=True, the input is normalized as a title-cased name and restricted
    to letters and spaces. If allow_empty=True, blank values are accepted.
    """

    def parser(raw):
        return " ".join(raw.split())

    def is_valid(value):
        value = " ".join(value.split())

        if not value and not allow_empty:
            return False, "Input cannot be empty. Try Again."

        if len(value) > max_length:
            return False, f"You exceeded the maximum length ({max_length}). Try Again."

        if name:
            normalized = value.title()
            if _has_invalid_characters(normalized):
                return False, "Invalid characters detected, use only letters and whitespaces. Try Again."
            return True, normalized

        return True, value

    return Validator(parser=parser, is_valid=is_valid).prompt(prompt)


# helper function
def _has_invalid_characters(text):
    """Check if text contains non-alphabetic characters (except spaces)."""
    return any(char != " " and not char.isalpha() for char in text)


# ==================== NUMBER (int or float) ====================
def get_num(prompt, *, min_val=None, max_val=None, floating=False):
    """
    Asks the user for a number until a valid one is given.
    It validates in the range:
        (-Infinite - max_val) if min_val is None
        (min_val - Infinite) if max_val is None
        (min_val - max_val) if both are given
    If floating is True, it accepts floating point numbers, otherwise only integers.
    """

    def parser(raw):
        return float(raw) if floating else int(raw)

    def is_valid(value):
        if floating and not math.isfinite(value):
            return False, f"You didn't insert a valid {'float' if floating else 'integer'}. Try again."

        if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
            lower = min_val if min_val is not None else "-Infinite"
            upper = max_val if max_val is not None else "Infinite"
            return False, f"You inserted a number out of the valid range [{lower} - {upper}]"

        return True, value

    return Validator(
        parser=parser,
        is_valid=is_valid,
        error_message=f"You didn't insert a valid {'float' if floating else 'integer'}. Try again.",
    ).prompt(prompt)


# ==================== BOOLEAN LOGIC ====================
def yes_no(prompt):
    """Asks the user a yes/no question and returns True for yes and False for no."""

    def parser(raw):
        return raw.strip().lower()

    def is_valid(value):
        if value in ["y", "yes"]:
            return True, True
        if value in ["n", "no"]:
            return True, False
        return False, "Invalid input. Please enter 'y' or 'n'."

    return Validator(
        parser=parser, 
        is_valid=is_valid, 
        error_message="Invalid input. Please enter 'y' or 'n'."
        ).prompt(prompt + " (y/n): ")