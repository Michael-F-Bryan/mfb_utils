import pytest
from utils.scanner import StringScanner


@pytest.fixture
def scanner():
    src = 'Hello, world!'
    return StringScanner(src)


class TestScanner:
    def test_init(self):
        src = 'Hello, world!'
        scanner = StringScanner(src)
        assert scanner.text == src
        assert scanner.pos == 0
        assert scanner.match == None

    def test_repr(self, scanner):
        should_be = '<StringScanner: position=0 text="Hello, world!">'
        assert repr(scanner) == should_be

    def test_check_valid(self, scanner):
        stuff = scanner.check(r'\w+')
        assert stuff == 'Hello'
        assert scanner.match == stuff
        assert scanner.pos == 0

    def test_check_invalid(self, scanner):
        stuff = scanner.check(r'\s+')
        assert stuff == None
        assert scanner.match == stuff
        assert scanner.pos == 0

    def test_skip_valid(self, scanner):
        num_skipped = scanner.skip(r'\w+')
        assert num_skipped == 5
        assert scanner.pos == 5
        assert scanner.match == 'Hello'

    def test_skip_invalid(self, scanner):
        num_skipped = scanner.skip(r'\s+')
        assert num_skipped == 0
        assert scanner.pos == 0
        assert scanner.match ==None

    def test_unscan(self, scanner):
        scanner.scan(r'\w+')
        assert scanner.pos == 5
        assert scanner.match == 'Hello'
        scanner.unscan()
        assert scanner.pos == 0
        assert scanner.match == None

    def test_getch(self, scanner):
        first_char = scanner.getch()
        assert scanner.pos == 1
        assert first_char == 'H'
        assert scanner.match == 'H'
        second_char = scanner.getch()
        assert scanner.pos == 2
        assert second_char == 'e'
        assert scanner.match == 'e'

    def test_append(self, scanner):
        text = scanner.text
        old_pos = scanner.pos
        old_match = scanner.match
        scanner.append('blah')
        assert scanner.text == text + 'blah'
        assert scanner.pos == old_pos
        assert scanner.match == old_match

    def test_not_at_eos(self, scanner):
        assert scanner.pos == 0
        assert len(scanner.text) > 0
        assert not scanner.end_of_string

    def test_at_eos(self, scanner):
        scanner.scan('Hello, world!')
        assert scanner.pos == len(scanner.text)
        assert scanner.end_of_string

    def test_simple_getitem(self, scanner):
        assert scanner[2] == 'l'
        assert scanner[-1] == '!'

    def test_getitem_slice(self, scanner):
        assert scanner[:5] == 'Hello'
        assert scanner[1:5:2] == 'el'
        assert scanner[5:] == ', world!'

    def test_invalid_getitem(self, scanner):
        with pytest.raises(IndexError):
            scanner[123]
        with pytest.raises(TypeError):
            # Because we shouldn't be trying to access a string using a 
            # string index
            scanner['blah']

    def test_current_char(self, scanner):
        assert scanner.current_char == 'H'
        scanner.scan(r'\w+,')
        assert scanner.current_char == ' '

    def test_current_char_at_eos(self, scanner):
        scanner.scan('Hello, world!')
        assert scanner.end_of_string 
        assert scanner.current_char == None

    def test_peek(self, scanner):
        """
        Make sure that using peek() doesn't affect the state of the scanner
        """
        assert scanner.pos == 0
        assert scanner.current_char == 'H'
        assert scanner.match == None

        assert scanner.peek() == 'e'

        assert scanner.pos == 0
        assert scanner.current_char == 'H'
        assert scanner.match == None

    def test_peek_multiple_chars(self, scanner):
        assert scanner.peek(2) == 'el'
        assert scanner.peek(5) == 'ello,'
        
    def test_rest(self, scanner):
        scanner.scan(r'\w+')
        old_pos = scanner.pos
        assert scanner.rest == ', world!'
        assert scanner.pos == old_pos
