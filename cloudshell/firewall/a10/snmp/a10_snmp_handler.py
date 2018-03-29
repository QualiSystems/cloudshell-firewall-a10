from cloudshell.devices.snmp_handler import SnmpHandler


class A10SnmpHandler(SnmpHandler):
    def __init__(self, resource_config, logger, api, cli_handler):
        super(A10SnmpHandler, self).__init__(resource_config, logger, api)
        self.cli_handler = cli_handler

    def _create_enable_flow(self):
        pass

    def _create_disable_flow(self):
        pass
