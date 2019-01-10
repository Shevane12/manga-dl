#!/usr/bin/python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

from sys import stderr
import argcomplete

from .cli import Cli
from .cli import args, db


def main():
    argcomplete.autocomplete(args.get_cli_arguments())
    _cli = Cli()
    _cli.fill_args()
    check = _cli.check_version()
    if check['need_update']:
        print('Please, update manga-py')
        print('See url: %s' % check['url'], file=stderr)
    _cli.run()


def db_main():
    argcomplete.autocomplete(db.args())
    _db = db.DataBase()
    _db.run(db.args())
