#!/usr/bin/env python
import os
import sys

from django.core.management.templates import TemplateCommand
from django.core.management.utils import get_random_secret_key


CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 4)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        "This version of Wagtail requires Python {}.{} or above - you are running {}.{}\n".format(*(REQUIRED_PYTHON + CURRENT_PYTHON))  # noqa
    )
    sys.exit(1)


class CreateProject(TemplateCommand):
    """
    Based on django.core.management.startproject
    """
    help = "Creates the directory structure for a new Wagtail CRX project."
    missing_args_message = "You must provide a project name."

    def add_arguments(self, parser):
        parser.add_argument(
            '--sitename',
            help='Human readable name of your website or brand, e.g. "Mega Corp Inc."'
        )
        parser.add_argument(
            '--domain',
            help='Domain that will be used for your website in production, e.g. "www.example.com"'
        )
        super().add_arguments(parser)

    def handle(self, **options):
        # pop standard args
        project_name = options.pop('name')
        target = options.pop('directory')

        # Make sure given name is not already in use by another python package/module.
        try:
            __import__(project_name)
        except ImportError:
            pass
        else:
            sys.exit("'%s' conflicts with the name of an existing "
                     "Python module and cannot be used as a project "
                     "name. Please try another name." % project_name)

        # Create a random SECRET_KEY to put it in the main settings.
        options['secret_key'] = get_random_secret_key()

        # Handle custom template logic
        import coderedcms
        codered_path = os.path.dirname(coderedcms.__file__)
        if not options['template']:
            options['template'] = 'basic'
        template_path = os.path.join(
            os.path.join(codered_path, 'project_template'),
            options['template']
        )

        # Check if provided template is built-in to coderedcms,
        # otherwise, do not change it.
        if os.path.isdir(template_path):
            options['template'] = template_path

        # Treat these files as Django templates to render the boilerplate.
        options['extensions'] = ['py', 'md', 'txt']
        options['files'] = ['Dockerfile']

        # Set options
        message = "Creating a Wagtail CRX project called %(project_name)s"

        if options.get('sitename'):
            message += " for %(sitename)s"
        else:
            options['sitename'] = project_name

        if options.get('domain'):
            message += " (%(domain)s)"
            # Stip protocol out of domain if it is present.
            options['domain'] = options['domain'].split('://')[-1]
            # Figure out www logic.
            if options['domain'].startswith('www.'):
                options['domain_nowww'] = options['domain'].split('www.')[-1]
            else:
                options['domain_nowww'] = options['domain']
        else:
            options['domain'] = 'localhost'
            options['domain_nowww'] = options['domain']

        # Add additional custom options to the context.
        options['coderedcms_release'] = coderedcms.release

        # Print a friendly message
        print(message % {
            'project_name': project_name,
            'sitename': options.get('sitename'),
            'domain': options.get('domain'),
        })

        # Run command
        super().handle('project', project_name, target, **options)

        # Be a friend once again.
        print("Success! %(project_name)s has been created" % {'project_name': project_name})

        nextsteps = """
Next steps:
    1. cd %(directory)s/
    2. python manage.py migrate
    3. python manage.py createsuperuser
    4. python manage.py runserver
    5. Go to http://localhost:8000/admin/ and start editing!
"""
        print(nextsteps % {'directory': target if target else project_name})


COMMANDS = {
    'start': CreateProject(),
}


def prog_name():
    return os.path.basename(sys.argv[0])


def help_index():
    print("Type '%s help <subcommand>' for help on a specific subcommand.\n" % prog_name())  # NOQA
    print("Available subcommands:\n")  # NOQA
    for name, cmd in sorted(COMMANDS.items()):
        print("    %s%s" % (name.ljust(20), cmd.help))  # NOQA


def unknown_command(command):
    print("Unknown command: '%s'" % command)  # NOQA
    print("Type '%s help' for usage." % prog_name())  # NOQA
    sys.exit(1)


def main():
    try:
        command_name = sys.argv[1]
    except IndexError:
        help_index()
        return

    if command_name == 'help':
        try:
            help_command_name = sys.argv[2]
        except IndexError:
            help_index()
            return

        try:
            command = COMMANDS[help_command_name]
        except KeyError:
            unknown_command(help_command_name)
            return

        command.print_help(prog_name(), help_command_name)
        return

    try:
        command = COMMANDS[command_name]
    except KeyError:
        unknown_command(command_name)
        return

    command.run_from_argv(sys.argv)


if __name__ == "__main__":
    main()
