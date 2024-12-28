import unittest
from unittest.mock import patch, mock_open, MagicMock
from models.device_mode_model import get_device_mode, set_device_mode, reboot_system, shutdown_system, delayed_reboot, delayed_shutdown, turn_off_i2c_display


class TestDeviceModeModel(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='AP')
    @patch('os.path.exists', return_value=True)
    @patch('config.constants.DEVICE_MODE_FILE_PATH', '/fake/path/mode.txt')
    def test_get_device_mode_success(self, mock_exists, mock_open):
        self.assertEqual(get_device_mode(), 'AP')

    @patch('os.path.exists', return_value=False)
    @patch('config.constants.DEVICE_MODE_FILE_PATH', '/fake/path/mode.txt')
    def test_get_device_mode_file_not_found(self, mock_exists):
        with self.assertRaises(FileNotFoundError):
            get_device_mode()

    @patch('builtins.open', new_callable=mock_open, read_data='INVALID')
    @patch('os.path.exists', return_value=True)
    @patch('config.constants.DEVICE_MODE_FILE_PATH', '/fake/path/mode.txt')
    def test_get_device_mode_invalid_mode(self, mock_exists, mock_open):
        with self.assertRaises(ValueError):
            get_device_mode()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('config.constants.DEVICE_MODE_FILE_PATH', '/fake/path/mode.txt')
    @patch('models.device_mode_model.reboot_system')
    def test_set_device_mode_success(self, mock_reboot, mock_exists, mock_open):
        set_device_mode('STA')
        mock_open().write.assert_called_once_with('STA')
        mock_reboot.assert_called_once()

    @patch('os.path.exists', return_value=False)
    @patch('config.constants.DEVICE_MODE_FILE_PATH', '/fake/path/mode.txt')
    def test_set_device_mode_file_not_found(self, mock_exists):
        with self.assertRaises(FileNotFoundError):
            set_device_mode('STA')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('config.constants.DEVICE_MODE_FILE_PATH', '/fake/path/mode.txt')
    def test_set_device_mode_invalid_mode(self, mock_exists, mock_open):
        with self.assertRaises(ValueError):
            set_device_mode('INVALID')

    @patch('os.system')
    @patch('models.device_mode_model.turn_off_i2c_display')
    def test_reboot_system(self, mock_turn_off, mock_system):
        reboot_system()
        mock_turn_off.assert_called_once()
        mock_system.assert_called_once_with('sudo reboot')

    @patch('os.system')
    @patch('models.device_mode_model.turn_off_i2c_display')
    def test_shutdown_system(self, mock_turn_off, mock_system):
        shutdown_system()
        mock_turn_off.assert_called_once()
        mock_system.assert_called_once_with('sudo shutdown -h now')

    @patch('threading.Timer')
    def test_delayed_reboot(self, mock_timer):
        delayed_reboot()
        mock_timer.assert_called_once_with(3, reboot_system)
        mock_timer().start.assert_called_once()

    @patch('threading.Timer')
    def test_delayed_shutdown(self, mock_timer):
        delayed_shutdown()
        mock_timer.assert_called_once_with(3, shutdown_system)
        mock_timer().start.assert_called_once()

    @patch('os.system')
    def test_turn_off_i2c_display(self, mock_system):
        turn_off_i2c_display()
        mock_system.assert_called_once_with('i2cset -y 1 0x3C 0x00 0xAE')


if __name__ == '__main__':
    unittest.main()