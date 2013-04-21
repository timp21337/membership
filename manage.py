#!/usr/bin/env python
import os
import sys
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "membership.settings")


# hack to prevent admin prompt
if 'syncdb' in sys.argv:
    sys.argv.append('--noinput')

execute_from_command_line(sys.argv)
