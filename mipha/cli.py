#!/usr/bin/env python

import django

from mipha.pre_settings import pre_setting


def main():
    pre_setting()
    from mipha.models import User
    print(User.all())


if __name__ == "__main__":
    main()
