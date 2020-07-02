#!/usr/bin/env python
import os
import sys
from pathlib import Path
from stat import S_IEXEC, S_IRUSR, S_IWUSR


def prep_git_versioning():
    """Do some things to make this project fully ready for
    development"""
    # pre-commit to .git/hooks/, found by github, which then runs
    # .githooks/pre-commit
    # this is how pre-commit script is being kept in version control

    with open(".git/hooks/pre-commit", "w") as hookscript:
        hookscript.write("#!/bin/sh\n" "sh .githooks/pre-commit")

    # change permissions to execute by owner so github can use it, write
    # by owner in case the above is called on existing file,
    # and read in case we want to ever see it.
    # equivalent to chmod +x; apply to .git/hooks/pre-push
    ## adapted from https://stackoverflow.com/a/12792002/8011811
    os.chmod(".git/hooks/pre-commit", S_IWUSR | S_IEXEC | S_IRUSR)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    #prep_git_versioning()  # Set up githook when this file is run

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )

        raise

    # This allows easy placement of apps within the interior
    # tinydoor directory.
    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "tinydoor"))

    execute_from_command_line(sys.argv)
