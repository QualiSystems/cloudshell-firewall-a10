from cloudshell.cli.command_mode import CommandMode


class DefaultCommandMode(CommandMode):
    PROMPT = r'(\n|\r|^)[^>#]+?>\s*$'
    ENTER_COMMAND = ''
    EXIT_COMMAND = ''

    def __init__(self, resource_config, api):
        """Initialize Default command mode - default command mode for A10 Shells"""

        self.resource_config = resource_config
        self._api = api
        CommandMode.__init__(self, self.PROMPT, self.ENTER_COMMAND, self.EXIT_COMMAND)


class EnableCommandMode(CommandMode):
    PROMPT = r'(\n|\r|^)((?!\(config).)+?#\s*$'
    ENTER_COMMAND = 'enable'
    EXIT_COMMAND = 'exit'

    def __init__(self, resource_config, api):
        """Initialize Enable command mode"""

        self.resource_config = resource_config
        self._api = api
        self._enable_password = None

        CommandMode.__init__(
            self,
            self.PROMPT,
            self.ENTER_COMMAND,
            self.EXIT_COMMAND,
            enter_action_map={
                "[Pp]assword":
                    lambda session, logger: session.send_line(self.enable_password, logger)
            }
        )

    @property
    def enable_password(self):
        if not self._enable_password:
            password = self.resource_config.enable_password
            self._enable_password = self._api.DecryptPassword(password).Value
        return self._enable_password


class ConfigCommandMode(CommandMode):
    PROMPT = r'(\n|\r|^)[^>#]+?\(config[^>#]+?#\s*$'
    ENTER_COMMAND = 'configure'
    EXIT_COMMAND = 'exit'

    def __init__(self, resource_config, api):
        """Initialize Config command mode"""

        self.resource_config = resource_config
        self._api = api
        CommandMode.__init__(self, self.PROMPT, self.ENTER_COMMAND, self.EXIT_COMMAND)


CommandMode.RELATIONS_DICT = {
    DefaultCommandMode: {
        EnableCommandMode: {
            ConfigCommandMode: {},
        }
    }
}
