#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Pizza.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Check if the command is to run the server
    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        # Bind to the port specified by the PORT environment variable
        port = os.getenv("PORT", "8000")  # Default to 8000 if PORT isn't set
        sys.argv[2:] = [f"0.0.0.0:{port}"]  # Set the host and port

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
