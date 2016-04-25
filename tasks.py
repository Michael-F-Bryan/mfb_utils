import os
import configparser
import pytest
from invoke import ctask as task, Collection


@task(aliases=['tests'], help={
    'quiet': 'Use quiet output',
    'args': 'Additional options',
    })
def test(c, quiet=False, args=None):
    """Run all tests using py.test"""
    args = args.split() if args else []

    if quiet:
        args.append('-q')

    arguments = ' '.join(args)
    pytest.main(arguments)


@task(default=True, aliases=['cov'], help={
    'html': 'Create a html report showing your code coverage',
    'browse': 'Open the html report up in Firefox',
    })
def coverage(c, html=True, browse=False):
    """Calculate code coverage"""
    c.run('coverage run -m pytest')
    
    if html:
        c.run('coverage html')

        if browse:
            directory = os.path.abspath(find_coverage_html())
            index = os.path.join(directory, 'index.html')
            c.run('firefox {}'.format(index))


@task
def lint(c, args=None):
    c.run('pylint utils')


def find_coverage_html():
    if not os.path.exists('.coveragerc'):
        return 'htmlcov'
    
    parser = configparser.ConfigParser()
    parser.read('.coveragerc')
    try:
        return parser['html']['directory']
    except KeyError:
        return 'htmlcov'


namespace = Collection(test, coverage, lint)
namespace.configure({'run.echo': True})
