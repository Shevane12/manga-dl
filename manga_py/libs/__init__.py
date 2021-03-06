from os import name as os_name
from sys import stdout


def is_windows():
    if ~os_name.lower().find('nt'):
        return True
    return False


def print_lib(*args, sep=' ', end='\n', file=stdout):
    if is_windows():
        try:
            print(*args, sep=sep, end=end, file=file)
        except Exception:
            print(str(*args).encode().decode(stdout.encoding, 'ignore'), sep=sep, end=end, file=file)
    else:
        print(*args, sep=sep, end=end, file=file)
