"""Subcommands for limejudge."""


class UnknownCommandError(ValueError):
    """Command name is unknown."""


def run_command_by_name(name, argv=None):
    if name == 'autocreate':
        from limejudge.commands.autocreate import main
    elif name == 'resourcetest':
        from limejudge.commands.resourcetest import main
    elif name == 'runjudge':
        from limejudge.commands.runjudge import main
    else:
        raise UnknownCommandError('Unknown command name: ' + repr(name))
    return main(argv)
