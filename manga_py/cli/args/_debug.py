from argparse import ArgumentParser

from manga_py.meta import __version__


def main(args_parser: ArgumentParser):
    args = args_parser.add_argument_group('Debug / Simulation options')

    args.add_argument('-h', '--help', action='help', help='show help and exit')
    args.add_argument('-v', '--version', action='version', version=__version__)
    args.add_argument('-J', '--print-json', action='store_const', const=True, default=False,
                      help='Print information about the results in the form of json (after completion)')

    args.add_argument('-S', '--simulate', action='store_const', const=True, default=False,
                      help='Do not download the files and do not write anything to disk')

    args.add_argument('-l', '--show-log', action='store_const', const=True, default=False,
                      help='Print log (Don\'t show progress bar)')

    args.add_argument('-L', '--file-log', type=str, default='', help='Print log to file')

    args.add_argument('--verbose-log', action='store_const', const=True, default=False,
                      help='Verbose log (See -l or -L)')

    args.add_argument('-P', '--no-progress', action='store_const',
                      const=True, help='Don\'t show progress bar', default=False)

    args.add_argument('--force-make-db', action='store_const',
                      const=True, help='Don\'t show progress bar', default=False)

    args.add_argument('-D', '--do-not-use-database', action='store_const',
                      help='Run manga-py without database', const=True, default=False)
