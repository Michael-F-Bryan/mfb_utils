import pytest
from invoke import ctask as task, Collection


@task(aliases=['tests'], help={
    'quiet': 'Use quiet output',
    'opts': 'Additional options',
    })
def test(c, quiet=False, opts=None):
    """Run all tests using py.test"""
    opts = opts or []

    if quiet:
        opts.append('-q')

    arguments = ' '.join(opts)
    pytest.main(arguments)


@task(default=True, aliases=['cov'])
def coverage(c, html=True):
    """Calculate code coverage"""
    c.run('coverage run -m pytest')
    
    if html:
        c.run('coverage html')

ns = Collection(test, coverage)
