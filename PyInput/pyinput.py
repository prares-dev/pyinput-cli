import math
from dataclasses import dataclass
from typing import Any, Callable, Optional, NamedTuple, Literal

class ValidationResult(NamedTuple):
    valid: bool
    result: Any | str

@dataclass
class Validator:
    """ Generic object for reusable validation flow and harden input handling. """
    parser: Callable[[str], Any]
    is_valid: Callable[[Any], ValidationResult]
    error_message: str = "Invalid input"
    max_attempts: Optional[int] = None

    def prompt(self, prompt_text: str) -> Any:
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


# ==================== GENERIC STRING ====================
def get_str(prompt: str = "Text: ", *, 
            max_length: int = 50, 
            name: bool = False, 
            allow_empty: bool = False):
    """
    Asks the user for a string until a valid one is given.

    If name=True, the input is normalized as a title-cased name and restricted
    to letters and spaces. If allow_empty=True, blank values are accepted.
    """

    def is_valid(value: str):
        value = " ".join(value.split())

        if not value and not allow_empty:
            return ValidationResult(False, "Input cannot be empty. Try Again.")

        if len(value) > max_length:
            return ValidationResult(False, f"You exceeded the maximum length ({max_length}). Try Again.")

        if name:
            normalized = value.title()
            if _has_invalid_characters(normalized):
                return ValidationResult(False, "Invalid characters detected, use only letters and whitespaces. Try Again.")
            return ValidationResult(True, normalized)

        return ValidationResult(True, value)

    return Validator(
        parser = lambda raw: " ".join(raw.split()), 
        is_valid = is_valid
        ).prompt(prompt)


# helper function
def _has_invalid_characters(text):
    """Check if text contains non-alphabetic characters (except spaces)."""
    return any(char != " " and not char.isalpha() for char in text)

# ==================== EMAIL ====================


# ==================== NUMBER (int or float) ====================
def get_num(prompt: str = "Number: ", *, 
            min_val: Optional[int | float] = None, 
            max_val: Optional[int | float] = None, 
            floating: bool = False):
    """
    Asks the user for a number until a valid one is given.
    It validates in the range:
        (-Infinite - max_val) if min_val is None
        (min_val - Infinite) if max_val is None
        (min_val - max_val) if both are given
    If floating is True, it accepts floating point numbers, otherwise only integers.
    """

<<<<<<< HEAD
    def is_valid(value: int | float):
=======
    def is_valid(value):
>>>>>>> 8e2a191a2b360ecc79a7e5d236c6b559015133e7
        if floating and not math.isfinite(value):
            return ValidationResult(False, f"You didn't insert a valid {'float' if floating else 'integer'}. Try again.")

        if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
            lower = min_val if min_val is not None else "-Infinite"
            upper = max_val if max_val is not None else "Infinite"
            return ValidationResult(False, f"You inserted a number out of the valid range [{lower} - {upper}]")

        return ValidationResult(True, value)

    return Validator(
        parser= lambda raw: float(raw) if floating else int(raw),
        is_valid=is_valid,
        error_message=f"You didn't insert a valid {'float' if floating else 'integer'}. Try again.",
        ).prompt(prompt)


# ==================== BOOLEAN LOGIC ====================
<<<<<<< HEAD
def yes_no(prompt:str = "Answer"):
=======
def yes_no(prompt:str ="Answer"):
>>>>>>> 8e2a191a2b360ecc79a7e5d236c6b559015133e7
    """Asks the user a yes/no question and returns True for yes and False for no."""

    def is_valid(value):
        if value in ["y", "yes"]:
            return ValidationResult(True, True)
        if value in ["n", "no"]:
            return ValidationResult(True, False)
        return ValidationResult(False, "Invalid input. Please enter 'y' or 'n'.")

    return Validator(
        parser= lambda raw: raw.strip().lower(), 
        is_valid=is_valid, 
        error_message="Invalid input. Please enter 'y' or 'n'."
        ).prompt(prompt + " (y/n): ")