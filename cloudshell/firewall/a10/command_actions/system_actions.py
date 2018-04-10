from logging import Logger

from cloudshell.cli.cli_service import CliService
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.firewall.a10.command_templates import configuration


class SystemActions(object):
    def __init__(self, cli_service, logger):
        """System actions

        :param CliService cli_service: config mode cli_service
        :param Logger logger:
        """

        self._cli_service = cli_service
        self._logger = logger

    def copy(self, source, destination, timeout=180):
        """Copy file from device to tftp or vice versa, as well as copying inside devices filesystem

        :param str source: source file
        :param str destination: destination file
        :param int timeout: session timeout
        """

        CommandTemplateExecutor(
            self._cli_service,
            configuration.COPY,
            timeout=timeout,
        ).execute_command(src=source, dst=destination)
