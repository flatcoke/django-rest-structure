#!/usr/bin/env python
import sys

import dotenv
import os


def valid_env():
    env_list = []
    env_example_list = []

    f = open('.env', 'r')
    for i in f.readlines():
        env_list.append(i.rstrip().split('=')[0])

    f = open('.env_example', 'r')
    for i in f.readlines():
        value = i.rstrip()
        env_example_list.append(value)
        if os.environ.get(value) is None:
            raise EnvironmentError('must set env in list of env_example file')
    if not set(env_example_list) == set(env_list):
        raise EnvironmentError('env and env_example are not match')


if __name__ == "__main__":
    dotenv.read_dotenv()
    valid_env()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "flatcoke.settings.development")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
