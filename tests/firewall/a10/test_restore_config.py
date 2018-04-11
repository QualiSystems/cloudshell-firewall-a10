from mock import patch, MagicMock

from cloudshell.firewall.a10.helpers.exceptions import A10Exception
from cloudshell.firewall.a10.runners.a10_configuration_runner import A10ConfigurationRunner
from tests.firewall.a10.base_test import BaseA10TestCase, CliEmulator, Command, CONFIG_PROMPT


@patch('cloudshell.cli.session.ssh_session.paramiko', MagicMock())
@patch('cloudshell.cli.session.ssh_session.SSHSession._clear_buffer', MagicMock(return_value=''))
class TestRestoreConfig(BaseA10TestCase):

    def _setUp(self, attrs=None):
        super(TestRestoreConfig, self)._setUp(attrs)
        self.runner = A10ConfigurationRunner(
            self.logger, self.resource_config, self.api, self.cli_handler)

    def setUp(self):
        self._setUp()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_restore_anonymous(self, send_mock, recv_mock):
        remote_path = 'ftp://192.168.122.10/Test-running-100418-163658'
        configuration_type = 'running'

        emu = CliEmulator([
            Command('configure', CONFIG_PROMPT),
            Command(
                'copy {} {}-config'.format(remote_path, configuration_type),
                'User name []?',
            ),
            Command('', 'Password []?'),
            Command(
                '',
                'Do you want to save the remote host information to a profile for later use?'
                '[yes/no]',
            ),
            Command(
                'no',
                '.\nFile copied successfully.\n{}'.format(CONFIG_PROMPT),
            ),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.restore(remote_path, configuration_type)

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_restore(self, send_mock, recv_mock):
        remote_path = 'ftp://user:password@192.168.122.10/Test-running-100418-163658'
        configuration_type = 'startup'

        emu = CliEmulator([
            Command('configure', CONFIG_PROMPT),
            Command(
                'copy {} {}-config'.format(remote_path, configuration_type),
                'Do you want to save the remote host information to a profile for later use?'
                '[yes/no]',
            ),
            Command(
                'no',
                '.\nFile copied successfully.\n{}'.format(CONFIG_PROMPT),
            ),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.restore(remote_path, configuration_type)

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_fail_to_restore(self, send_mock, recv_mock):
        remote_path = 'ftp://user:password@192.168.122.10/Test-running-100418-163658'
        configuration_type = 'running'

        emu = CliEmulator([
            Command('configure', CONFIG_PROMPT),
            Command(
                'copy {} {}-config'.format(remote_path, configuration_type),
                'Do you want to save the remote host information to a profile for later use?'
                '[yes/no]',
            ),
            Command(
                'no',
                '.\nFailed to get file from ftp server. Check log for reason of failure.'
                '\n{}'.format(CONFIG_PROMPT),
            ),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.assertRaisesRegexp(
            Exception,
            'Session returned \'Fail to copy a file\'',
            self.runner.restore,
            remote_path,
            configuration_type,
        )

        emu.check_calls()

    def test_append_method(self):
        remote_path = 'ftp://user:password@192.168.122.10/Test-running-100418-163658'
        configuration_type = 'running'
        restore_method = 'append'

        self.assertRaisesRegexp(
            A10Exception,
            'Device doesn\'t support append restore method',
            self.runner.restore,
            remote_path,
            configuration_type,
            restore_method,
        )
