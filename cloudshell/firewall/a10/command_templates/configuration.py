from cloudshell.cli.command_template.command_template import CommandTemplate


COPY = CommandTemplate(
    'copy {src} {dst}',
    action_map={
        r'[Uu]ser': lambda session, logger: session.send_line('', logger),
        r'[Pp]assword': lambda session, logger: session.send_line('', logger),
        r'for later use\?\[yes/no\]': lambda session, logger: session.send_line('no', logger),
        r'overwrite .* \([Nn]/[Yy]\)': lambda session, logger: session.send_line('y', logger),
    },
    error_map={
        r'^((?!File copied successfully).)*$': 'Fail to copy a file',
    }
)
