# pyinput-cli
**The definitive input handler for your python cli programs.**

pyinput-cli is a package that provides functions to handle user input in a consistent way across any project.

- **get_str**: reads a string and can validate its length or its format as a name.
- **get_num**: reads an integer or float and validates minimum and maximum values.
- **yes_no**: asks a yes/no question and returns the boolean result.

## Example usage

```python
from pyinput import get_num, get_str, yes_no

name = get_str("Name: ", name=True, max_length=30)
age = get_num("Age: ", min_val=0, max_val=120)
continue_ = yes_no("Continue?")

print(name, age, continue_)
```

## Notes

- Empty strings are rejected by default for `get_str`.
- `get_num` rejects invalid input and values outside the configured bounds.
- The functions are designed for small interactive CLI flows and can be reused in larger projects.