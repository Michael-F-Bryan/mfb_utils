import os

def _get_version():
    this_file = os.path.abspath(__file__)
    base_dir = os.path.dirname(os.path.dirname(this_file))
    version_path = os.path.join(base_dir, 'VERSION')
    with open(version_path) as f:
        return f.read().strip()

__version__ = _get_version()




