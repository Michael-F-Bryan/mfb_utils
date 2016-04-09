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
from utils import Hook, flatten


def test_hook_method_no_args():
    # Create our hook dummy
    class HookDummy:
        def __init__(self):
            self.call_log = []

        @Hook('my_special_hook')
        def do(self):
            self.call_log.append('ran do')

        def my_special_hook(self):
            self.call_log.append('ran my_special_hook')

    # Instantiate HookDummy and start the test
    hook_dummy = HookDummy()
    hook_dummy.do() 
    
    expected_call_log = ['ran do', 'ran my_special_hook'] 
    assert expected_call_log == hook_dummy.call_log


def test_hook_method_called_before():
    # Create our hook dummy
    class HookDummy:
        def __init__(self):
            self.call_log = []

        @Hook('my_special_hook', call_after=False)
        def do(self):
            self.call_log.append('ran do')

        def my_special_hook(self):
            self.call_log.append('ran my_special_hook')

    # Instantiate HookDummy and start the test
    hook_dummy = HookDummy()
    hook_dummy.do() 
    
    expected_call_log = ['ran my_special_hook', 'ran do']
    assert expected_call_log == hook_dummy.call_log


def test_hook_no_hook_method():
    # Create our hook dummy
    class HookDummy:
        def __init__(self):
            self.call_log = []

        @Hook('nonexistent_hook')
        def do(self):
            self.call_log.append('ran do')

    # Instantiate HookDummy and start the test
    hook_dummy = HookDummy()
    hook_dummy.do() 
    
    expected_call_log = ['ran do']
    assert expected_call_log == hook_dummy.call_log


def test_hook_method_with_args_and_kwargs():
    # Create our hook dummy
    class HookDummy:
        def __init__(self):
            self.call_log = []

        @Hook('my_special_hook', arg_1='arg_1', arg_2=72, arg_3=1)
        def do(self):
            self.call_log.append('ran do')

        def my_special_hook(self, **kwargs):
            self.call_log.append('ran my_special_hook')
            self.call_log.append(kwargs)

    # Instantiate HookDummy and start the test
    hook_dummy = HookDummy()
    hook_dummy.do()

    expected_call_log = [
            'ran do', 
            'ran my_special_hook',
            {'arg_1': 'arg_1', 'arg_2': 72, 'arg_3': 1},
            ]

    assert expected_call_log == hook_dummy.call_log


def test_hook_error_when_called_on_function():
    @Hook('my_special_hook')
    def some_function():
        pass

    with pytest.raises(TypeError):
        some_function()


def test_flatten_list_of_lists():
    nested_structure = [[1, 2, 3], [3, 'hello']]

    output = flatten(nested_structure)
    temp = []
    for thing in output:
        temp.append(thing)

    expected = [1, 2, 3, 3, 'hello']
    
    assert temp == expected


def test_flatten_only_string_provided():
    nested_structure = 'some string'

    output = flatten(nested_structure)
    temp = []
    for thing in output:
        temp.append(thing)

    expected = ['some string']
    assert temp == expected
    

if __name__ == "__main__":
    # Including sys.argv means that you can pass in all the normal py.test 
    # commandline arguments
    pytest.main(sys.argv[1:])
