"""
A Python module containing various utility functions, classes, decorators or
whatever.
"""

from collections import namedtuple, Iterable
import sys
import functools
import inspect
from bs4 import BeautifulSoup
import logging
import time
import random
import os
import errno


# Constants
# =========

USER_AGENTS = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36 OPR/34.0.2036.25',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.6.01001)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1',
    'Opera/9.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.01',
]
"""
A bunch of random User-Agent strings.
"""


# Decorators
# ==========

class Hook:
    """
    A special Hook decorator that will call something after a method has 
    completed.

    When decorating your method, make sure to only use keyword arguments in
    the hook.

    The idea is for a developer to implement a specific class which has various
    methods, and on some methods he will add a Hook decorator. Then the user 
    can create a subclass of this class and implement the hooks themselves.

    The user is given access to the return value of the decorated function 
    through the `self._hook_return_value` variable. The return value is None
    if the hook is called before the decorated function.

    Example
    -------
    Developer::

        class MyClass:
            @Hook('on_do_stuff', arg1='something', arg2=7)
            def do_stuff(self):
                pass

    User::
    
        class MyNewClass(MyClass):
            def on_do_stuff(self, **kwargs):
                # Do something useful
                pass

    Parameters
    ----------
    hook_name: str
        The name of the hook function to be called.
    call_after: bool
        Whether to call the hook after or before the decorated function runs. 
        (default: True)
    
    Raises
    ------
    ValueError
        When a normal function is decorated instead of a method.
    """
    def __init__(self, hook_name, call_after=True, 
            skip_exceptions=True, **hook_kwargs):
        self.hook_name = hook_name
        self.hook_kwargs = hook_kwargs
        self.call_after = call_after
        self.skip_exceptions = skip_exceptions

    def __call__(self, func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            if self.call_after:
                ret = func(*args, **kwargs)
                self.call_hook(func, args, return_value=ret)
            else:
                self.call_hook(func, args)
                ret = func(*args, **kwargs)

            return ret

        return decorated

    def call_hook(self, func, args, return_value=None):
        """
        Get the "self" argument (i.e. the instance of a class that is implicitly
        passed to a method when you call something like "some_class.method()")
        then call our hook.

        Uses inspect to check that a function has this "self" variable passed
        in first. This is a sanity check to ensure that the hook decorator is
        only used on methods.

        By default any exceptions encountered while running the hook will be
        silently ignored.
        """
        func_args = inspect.getargspec(func).args
        if len(func_args) < 1 or 'self' not in func_args:
            raise TypeError('Only methods can be decorated with "Hook"')

        instance = args[0]
        hook = getattr(instance, self.hook_name, None)

        if hook:
            instance._hook_return_value = return_value
            try:
                hook(**self.hook_kwargs)
            except Exception:
                if not self.skip_exceptions:
                    raise 
    

class Timed:
    """
    Time a function call and save it's duration (in seconds) to 
    `function.duration`.

    Parameters
    ----------
    output_stream: Stream-like object
        A stream to write the timing message to, set to None to disable it
        (default: stderr)
    decimals: int
        The number of decimal places to print the duration to in the output
        stream
    """
    def __init__(self, output_stream=sys.stderr, decimals=3):
        if output_stream is None or hasattr(output_stream, 'write'):
            self.output_stream = output_stream
        else:
            raise TypeError('output_stream should be a Stream (i.e. has a '
                            '"write()" method)')

        if not isinstance(decimals, int):
            raise TypeError('decimals must be an integer')
        else:
            self.decimals = decimals
    
    def __call__(self, func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            start = time.time()
            ret = func(*args, **kwargs)
            decorated.duration = time.time() - start

            if self.output_stream:
                func_args = []
                func_args.extend(args)
                func_args.extend('{}={}'.format(key, value) for key, value in kwargs.items())
                func_arguments = ', '.join(func_args)
                function_call = '{}({})'.format(func.__name__, func_arguments)

                duration = round(decorated.duration, self.decimals)
                self.output_stream.write(
                        '{} took {} seconds'.format(function_call, duration))

            return ret
        return decorated


# Functions
# =========

def get_logger(name, log_file, log_level=None):
    """
    Get a logger object which is set up properly with the correct formatting,
    logfile, etc.

    Parameters
    ----------
    name: str
        The __name__ of the module calling this function.
    log_file: str
        The filename of the file to log to.

    Returns
    -------
    logging.Logger
        A logging.Logger object that can be used to log to a common file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level or logging.INFO)

    if log_file == 'stdout':
        handler = logging.StreamHandler(sys.stdout)
    elif log_file == 'stderr':
        handler = logging.StreamHandler(sys.stderr)
    else:
        handler = logging.FileHandler(log_file)

    if not len(logger.handlers):
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s: %(message)s',
            datefmt='%Y/%m/%d %I:%M:%S %p'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def flatten(items, ignore_types=(str, bytes)):
    """
    Turn a nested structure (usually a list of lists... of lists of lists of 
    lists) into one flat list.

    Parameters
    ----------
    items: list(list(...))
        A nested list structure.
    ignore_types: list(types)
        A list of types (usually iterables) that shouldn't be expanded. (e.g. 
        don't flatten a string into a list of characters, etc)

    Returns
    -------
    generator
        Yields each element of the nested structure in turn.
    """
    # If a string, bytes etc is passed in as the "items" nested function then
    # just yield it back out
    if isinstance(items, ignore_types):
        yield items
    else:
        for x in items:
            if isinstance(x, Iterable) and not isinstance(x, ignore_types):
                yield from flatten(x)
            else:
                yield x


def hidden_fields(soup):
    """
    Retrieve all the hidden fields from a html form.

    Parameters
    ----------
    soup: BeautifulSoup or str
        The form to search. If it is not a BeautifulSoup object then assume it
        is the html source and convert it into BeautifulSoup.

    Returns
    -------
    dict
        A dictionary of the hidden fields and their values.
    """
    if not isinstance(soup, BeautifulSoup):
        soup = BeautifulSoup(soup, 'html.parser')

    hidden = {}

    hidden_fields = soup.find_all('input', type='hidden')
    for field in hidden_fields:
        hidden[field['name']] = field['value']

    return hidden


_suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes, decimals=2):
    """
    Convert a number of bytes into it's human readable string using SI 
    suffixes.

    Note
    ----
    1 KB = 1024 bytes

    Parameters
    ----------
    nbytes: int
        The total number of bytes
    decimals: int
        The number of decimal places to round to

    Returns
    -------
    string
        The human readable size.

    """
    if nbytes == 0: return '0 B'
    i = 0
    while nbytes >= 1024 and i < len(_suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('{}'.format(round(nbytes, decimals)))
    f = f.rstrip('0').rstrip('.')
    return '%s %s' % (f, _suffixes[i])


def random_user_agent():
    return random.choice(USER_AGENTS)
    
def mkdir(path):
    try:
        os.makedirs(path)
        logger.debug('Made directory: {}'.format(path))
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
