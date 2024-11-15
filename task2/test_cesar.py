from cesar import encrypt, decrypt, reverse, to_upper, to_lower


def test_encrypt():
    assert encrypt("abc", 1) == "bcd"
    assert encrypt("xyz", 2) == "zab"
    assert encrypt("Hello, World!", 3) == "Khoor, Zruog!"


def test_decrypt():
    assert decrypt("bcd", 1) == "abc"
    assert decrypt("zab", 2) == "xyz"
    assert decrypt("Khoor, Zruog!", 3) == "Hello, World!"


def test_reverse():
    assert reverse("hello") == "olleh"
    assert reverse("abc") == "cba"


def test_to_upper():
    assert to_upper("hello") == "HELLO"
    assert to_upper("world") == "WORLD"


def test_to_lower():
    assert to_lower("HELLO") == "hello"  # ожидается ошибка
