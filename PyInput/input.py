# ==================== STRING ====================
def get_str(prompt="Text: ", *, max_length=50, name=False):
    """ 
    Asks the user for a string until a valid one is given. 
    if name = True
        the name can't contain any character other than a letter
        strips the string and also eliminates consecutive spaces
    Anyway the max_length is validated
    """
    while True:
        text = input(prompt)
        text = " ".join(text.split())
        
        if len(text) > max_length:
            print(f"You exceeded the maximum length ({max_length}). Try Again.")
            continue
        
        if name:
            text = " ".join(text.split()).title()
            if _has_invalid_characters(text):
                print("Invalid characters detected, use only letters and whitespaces. Try Again.")
                continue
            
        return text
    
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
    while True:
        text = input(prompt)
        try:
            num = int(text) if not floating else float(text)
        except ValueError:
            print(f"You didn't insert a valid {"float" if floating else "integer"}. Try again.")
            continue
        
        if (min_val is not None and num < min_val) or (max_val is not None and num > max_val):
            min = min_val if min_val is not None else "-Infinite"
            max = max_val if max_val is not None else "Infinite"
            print(f"You inserted a number out of the valid range [{min} - {max}]")
            continue
        
        return num

# ==================== BOOLEAN LOGIC ====================
def yes_no(prompt):
    """Asks the user a yes/no question and returns True for yes and False for no."""
    while True:
        response = input(prompt + " (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")