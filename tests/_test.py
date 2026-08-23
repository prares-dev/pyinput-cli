from PyInput.input import get_num, get_str, yes_no

def test_get_str_strips_str(monkeypatch):
    input = "    an str with leading and trailing whitespaces   "
    monkeypatch.setattr("builtins.input", lambda _ : input)
    
    readed = get_str()
    
    assert readed == input.strip()

def test_get_str_with_max_length(monkeypatch, capsys):
    responses = iter([
        "a string with more than 10 characters", 
        "another that's also very long", 
        "few here",
        'a last one'
        ])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    
    readed = get_str(max_length=10)
    
    assert readed == "few here"
    assert capsys.readouterr().out == (
        "You exceeded the maximum length (10). Try Again.\n"
        "You exceeded the maximum length (10). Try Again.\n"
    )

def test_get_str_eliminates_repeated_whitespaces(monkeypatch):
    input = "a    lot of     repeated whitespaces here   "
    monkeypatch.setattr("builtins.input", lambda _ : input)
    
    readed = get_str()
    
    assert readed == " ".join(input.split())

def test_get_str_with_name_true(monkeypatch):
    input = " pedro Alberto    rosquete ares  "
    monkeypatch.setattr("builtins.input", lambda _ : input)
    
    readed = get_str(name=True)
    
    assert readed == " ".join(input.split()).title()

def test_get_str_with_name_true_and_max_length(monkeypatch, capsys):
    responses = iter([
        "Pedro Alberto",
        "Pedro"
        ])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    
    readed = get_str("First name: ", name=True, max_length=10)
    
    assert readed == "Pedro"
    assert capsys.readouterr().out == (
        "You exceeded the maximum length (10). Try Again.\n"
    )


def test_get_str_rejects_empty_input(monkeypatch, capsys):
    responses = iter(["", "Jane Doe"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    assert get_str("Name: ") == "Jane Doe"
    assert capsys.readouterr().out == "Input cannot be empty. Try Again.\n"


def test_get_str_with_name_detects_invalid_chars(monkeypatch, capsys):
    responses = iter([
        "Pedro 234Alberto",
        "Pedro Albe-rto*",
        "Pedro Alberto",
        "asdasd"
        ])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    
    readed = get_str("Name: ", name=True)
    
    assert readed == "Pedro Alberto"
    assert capsys.readouterr().out == (
        "Invalid characters detected, use only letters and whitespaces. Try Again.\n"
        "Invalid characters detected, use only letters and whitespaces. Try Again.\n"
    )


def test_package_exports_public_api():
    import PyInput

    assert PyInput.get_str is not None
    assert PyInput.get_num is not None
    assert PyInput.yes_no is not None


def test_get_num_retries_until_integer_is_in_range(monkeypatch, capsys):
    responses = iter(["not a number", "-1", "42"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    read = get_num("Age: ", min_val=0, max_val=120)

    assert read == 42
    assert capsys.readouterr().out == (
        "You didn't insert a valid integer. Try again.\n"
        "You inserted a number out of the valid range [0 - 120]\n"
    )


def test_get_num_reads_float(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "12.5")

    read = get_num("Price: ", floating=True)

    assert read == 12.5
    assert capsys.readouterr().out == ""


def test_get_num_rejects_non_finite_float(monkeypatch, capsys):
    responses = iter(["nan", "inf", "42.5"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    assert get_num("Price: ", floating=True) == 42.5
    assert capsys.readouterr().out == (
        "You didn't insert a valid float. Try again.\n"
        "You didn't insert a valid float. Try again.\n"
    )


def test_get_num_accepts_inclusive_bounds(monkeypatch):
    responses = iter(["0", "120"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    assert get_num("Age: ", min_val=0, max_val=120) == 0
    assert get_num("Age: ", min_val=0, max_val=120) == 120


def test_get_num_supports_one_sided_bounds(monkeypatch):
    responses = iter(["-5", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    assert get_num("Number: ", max_val=0) == -5
    assert get_num("Number: ", min_val=0) == 5


def test_get_num_accepts_equal_min_and_max(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "-3")

    assert get_num("Number: ", min_val=-3, max_val=-3) == -3


def test_get_num_rejects_float_when_integer_expected(monkeypatch, capsys):
    responses = iter(["2.5", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    assert get_num("Count: ") == 2
    assert capsys.readouterr().out == (
        "You didn't insert a valid integer. Try again.\n"
    )


def test_yes_no_retries_after_invalid_response(monkeypatch, capsys):
    responses = iter(["maybe", " YES "])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    read = yes_no("Continue?")

    assert read is True
    assert capsys.readouterr().out == "Invalid input. Please enter 'y' or 'n'.\n"


def test_yes_no_returns_false_for_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: " No ")

    assert yes_no("Continue?") is False
