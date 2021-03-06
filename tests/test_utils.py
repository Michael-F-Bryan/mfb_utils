"""
The test suite for my utils package.

To Do
-----
- hidden_fields()
- get_logger()
"""

import sys
from unittest import mock
import pytest
from utils.misc import Hook, flatten, humansize, Timed, hidden_fields
import time
from io import StringIO


class TestHook:
    @pytest.fixture
    def hook_dummy(self, request):
        class HookDummy:
            def __init__(self):
                self.call_log = []

            @Hook('my_special_hook')
            def do(self):
                self.call_log.append('ran do')

            def my_special_hook(self):
                self.call_log.append('ran my_special_hook')

        return HookDummy()


    def test_hook_method_no_args(self, hook_dummy):
        hook_dummy.do() 

        expected_call_log = ['ran do', 'ran my_special_hook'] 
        assert expected_call_log == hook_dummy.call_log

    def test_hook_method_skip_hook_exception(self, hook_dummy):
        def my_special_hook(self):
            raise RuntimeError

        hook_dummy.my_special_hook = my_special_hook
        hook_dummy.do() 

        expected_call_log = ['ran do'] 
        assert expected_call_log == hook_dummy.call_log

    def test_hook_method_catch_exception(self):
        # Can't use the fixture because monkeypatching the do() method doesn't
        # work properly for some reason
        class HookDummy:
            def __init__(self):
                self.call_log = []

            @Hook('my_special_hook', skip_exceptions=False)
            def do(self):
                self.call_log.append('ran do')

            def my_special_hook(self):
                raise RuntimeError

        hook_dummy = HookDummy()

        with pytest.raises(RuntimeError):
            hook_dummy.do() 

    def test_hook_method_called_before(self):
        class HookDummy:
            def __init__(self):
                self.call_log = []

            @Hook('my_special_hook', call_after=False)
            def do(self):
                self.call_log.append('ran do')

            def my_special_hook(self):
                self.call_log.append('ran my_special_hook')

        hook_dummy = HookDummy()
        hook_dummy.do() 

        expected_call_log = ['ran my_special_hook', 'ran do']
        assert expected_call_log == hook_dummy.call_log

    def test_hook_no_hook_method(self):
        class HookDummy:
            def __init__(self):
                self.call_log = []

            @Hook('nonexistent_hook')
            def do(self):
                self.call_log.append('ran do')

        hook_dummy = HookDummy()
        hook_dummy.do() 

        expected_call_log = ['ran do']
        assert expected_call_log == hook_dummy.call_log

    def test_hook_method_with_args_and_kwargs(self):
        class HookDummy:
            def __init__(self):
                self.call_log = []

            @Hook('my_special_hook', arg_1='arg_1', arg_2=72, arg_3=1)
            def do(self):
                self.call_log.append('ran do')

            def my_special_hook(self, **kwargs):
                self.call_log.append('ran my_special_hook')
                self.call_log.append(kwargs)

        hook_dummy = HookDummy()
        hook_dummy.do()

        expected_call_log = [
                'ran do', 
                'ran my_special_hook',
                {'arg_1': 'arg_1', 'arg_2': 72, 'arg_3': 1},
                ]

        assert expected_call_log == hook_dummy.call_log

    def test_hook_error_when_called_on_function(self):
        @Hook('my_special_hook')
        def some_function():
            pass

        with pytest.raises(TypeError):
            some_function()

    def test_hook_access_return_when_called_after(self):
        class HookDummy:
            def __init__(self):
                self.call_log = []

            @Hook('on_do', skip_exceptions=False)
            def do(self):
                self.call_log.append('ran do')
                return 'something'

            def on_do(self, **kwargs):
                self.call_log.append('return value: "{}"'.format(self._hook_return_value))

        hook_dummy = HookDummy()
        hook_dummy.do() 

        expected_call_log = ['ran do', 'return value: "something"']
        assert expected_call_log == hook_dummy.call_log

    def test_hook_access_return_when_called_before(self):
        class HookDummy:
            def __init__(self):
                self.call_log = []

            @Hook('on_do', skip_exceptions=False, call_after=False)
            def do(self):
                self.call_log.append('ran do')
                return 'something'

            def on_do(self, **kwargs):
                self.call_log.append('return value: "{}"'.format(self._hook_return_value))

        hook_dummy = HookDummy()
        hook_dummy.do() 

        expected_call_log = [ 'return value: "None"', 'ran do']
        assert expected_call_log == hook_dummy.call_log

 
class TestFlatten:
    def test_flatten_list_of_lists(self):
        nested_structure = [[1, 2, 3], [3, 'hello']]

        output = flatten(nested_structure)
        temp = []
        for thing in output:
            temp.append(thing)

        expected = [1, 2, 3, 3, 'hello']

        assert temp == expected

    def test_flatten_only_string_provided(self):
        nested_structure = 'some string'

        output = flatten(nested_structure)
        temp = []
        for thing in output:
            temp.append(thing)

        expected = ['some string']
        assert temp == expected


class TestHumanSize:
    def test_humansize_12_kbytes(self):
        size = 12*1024
        string = humansize(size)
        assert string == '12 KB'

    def test_humansize_10_point_815_kbytes_2_decimals(self):
        size = 10.815*1024
        string = humansize(size, decimals=2)
        assert string == '10.81 KB'

    def test_humansize_10_point_81_kbytes(self):
        size = 10.81*1024
        string = humansize(size)
        assert string == '10.81 KB'

    def test_humansize_31_mbytes(self):
        size = 1024*1024*31
        string = humansize(size)
        assert string == '31 MB'

    def test_humansize_kbytes(self):
        size = 1024
        string = humansize(size)
        assert string == '1 KB'

    def test_humansize_kbytes(self):
        size = 1024*1024
        string = humansize(size)
        assert string == '1 MB'

    def test_humansize_mbytes(self):
        size = 1024*1024*1024
        string = humansize(size)
        assert string == '1 GB'


class TestTimed:
    def test_Timed_stderr_message_decimals_is_1(self):
        output_stream = StringIO()
        duration_should_be = 0.1
        decimals = 1
        @Timed(output_stream, decimals=decimals)
        def do_something():
            time.sleep(duration_should_be)

        do_something()

        duration = round(do_something.duration, decimals)
        should_be = 'do_something() took {} seconds'.format(duration)
        assert output_stream.getvalue() == should_be

    def test_Timed_stderr_message_decimals_is_negative(self):
        output_stream = StringIO()
        duration_should_be = 0.1
        decimals = -3
        @Timed(output_stream, decimals=decimals)
        def do_something():
            time.sleep(duration_should_be)

        do_something()

        duration = round(do_something.duration, decimals)
        should_be = 'do_something() took {} seconds'.format(duration)
        assert output_stream.getvalue() == should_be

    def test_Timed_stderr_message(self):
        output_stream = StringIO()
        duration_should_be = 0.1
        @Timed(output_stream)
        def do_something():
            time.sleep(duration_should_be)

        do_something()

        should_be = 'do_something() took {:.3} seconds'.format(do_something.duration)
        assert output_stream.getvalue() == should_be

    def test_Timed_stderr_message_invalid_decimals(self):
        output_stream = StringIO()
        duration_should_be = 0.1

        with pytest.raises(TypeError):
            @Timed(output_stream, decimals='hello')
            def do_something():
                time.sleep(duration_should_be)


    def test_Timed_stderr_message_invalid_stream(self):
        output_stream = 'boobies'
        duration_should_be = 0.1

        with pytest.raises(TypeError):
            @Timed(output_stream, decimals='hello')
            def do_something():
                time.sleep(duration_should_be)

    def test_Timed_stderr_message(self):
        output_stream = StringIO()
        duration_should_be = 0.1
        @Timed(output_stream)
        def do_something():
            time.sleep(duration_should_be)

        do_something()

        should_be = 'do_something() took {:.3} seconds'.format(do_something.duration)
        assert output_stream.getvalue() == should_be

    def test_Timed_no_stderr(self):
        duration_should_be = 0.1
        @Timed(None)
        def do_something():
            time.sleep(duration_should_be)

        do_something()

        assert do_something.duration - duration_should_be < 0.01 


class TestHiddenFields:
    def test_hidden_fields(self):
        stuff = """
        <!DOCTYPE html>
        <html>
        <body>
        <form action="demo_form.asp">
        First name: <input type="text" name="fname"><br>
        <input type="hidden" name="country" value="Norway">
        <input type="submit" value="Submit">
        </form>
        </body>
        </html>
        """
        hiddens = hidden_fields(stuff)
        should_be = {'country': 'Norway'}
        assert should_be == hiddens


    def test_hidden_fields_no_hiddens(self):
        stuff = """
        <!DOCTYPE html>
        <html>
        <body>
        <form action="demo_form.asp">
        First name: <input type="text" name="fname"><br>
        <input type="submit" value="Submit">
        </form>
        </body>
        </html>
        """
        hiddens = hidden_fields(stuff)
        should_be = {}
        assert should_be == hiddens


    def test_hidden_fields_invalid_html(self):
        stuff = 'stuff'
        hiddens = hidden_fields(stuff)
        should_be = {}
        assert should_be == hiddens


    def test_hidden_fields_invalid_input(self):
        stuff = 1234
        with pytest.raises(TypeError):
            hiddens = hidden_fields(stuff)


if __name__ == "__main__":
    # Including sys.argv means that you can pass in all the normal py.test 
    # commandline arguments
    pytest.main(sys.argv[1:])
