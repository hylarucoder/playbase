#!/usr/bin/env python
import os
import sys

from django.core.management import execute_from_command_line


def main():
    execute_from_command_line(sys.argv)
    # if not settings.configured:
    #     # settings.INSTALLED_APPS  # noqa
    #     django.setup()
    # from mipha.models import User
    # print(User.all())


if __name__ == "__main__":
    main()
