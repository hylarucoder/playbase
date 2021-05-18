#!/usr/bin/env python

import sys
import django

from mipha.pre_settings import pre_setting
from django.core.management import execute_from_command_line


def main():
    pre_setting()
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
