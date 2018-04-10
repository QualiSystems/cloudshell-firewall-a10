from cloudshell.devices.runners.configuration_runner import ConfigurationRunner
from cloudshell.firewall.a10.flows.a10_save_flow import A10SaveFlow


class A10ConfigurationRunner(ConfigurationRunner):
    @property
    def restore_flow(self):
        return

    @property
    def save_flow(self):
        return A10SaveFlow(cli_handler=self.cli_handler, logger=self._logger)

    @property
    def file_system(self):
        return 'flash:'
