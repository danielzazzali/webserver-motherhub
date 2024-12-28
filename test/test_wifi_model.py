import unittest
from unittest.mock import patch, MagicMock
from models.wifi_model import get_ap_ssid_and_password, change_ap_ssid, change_ap_password, bring_ap_connection_down, bring_ap_connection_up, is_ap_connection_active, get_ap_connected_devices

class TestWifiModel(unittest.TestCase):

    @patch('models.wifi_model.subprocess.run')
    def test_get_ap_ssid_and_password(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="802-11-wireless.ssid:TestSSID\n802-11-wireless-security.psk:TestPassword\n")
        result = get_ap_ssid_and_password()
        self.assertEqual(result, {"ssid": "TestSSID", "password": "TestPassword"})

    @patch('models.wifi_model.subprocess.run')
    def test_change_ap_ssid(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        with patch('models.wifi_model.is_ap_connection_active', return_value=True), \
             patch('models.wifi_model.bring_ap_connection_down', return_value=True), \
             patch('models.wifi_model.bring_ap_connection_up', return_value=True):
            result = change_ap_ssid("NewSSID")
            self.assertTrue(result)

    @patch('models.wifi_model.subprocess.run')
    def test_change_ap_password(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        with patch('models.wifi_model.is_ap_connection_active', return_value=True), \
             patch('models.wifi_model.bring_ap_connection_down', return_value=True), \
             patch('models.wifi_model.bring_ap_connection_up', return_value=True):
            result = change_ap_password("NewPassword")
            self.assertTrue(result)

    @patch('models.wifi_model.subprocess.run')
    def test_bring_ap_connection_down(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        result = bring_ap_connection_down()
        self.assertTrue(result)

    @patch('models.wifi_model.subprocess.run')
    def test_bring_ap_connection_up(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        result = bring_ap_connection_up()
        self.assertTrue(result)

    @patch('models.wifi_model.subprocess.run')
    def test_is_ap_connection_active(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout=":activated")
        result = is_ap_connection_active()
        self.assertTrue(result)

    @patch('models.wifi_model.get_ip_and_mask', return_value={'ip': '192.168.1.1', 'mask': '255.255.255.0'})
    @patch('models.wifi_model.calculate_network', return_value='192.168.1.0/24')
    @patch('models.wifi_model.run_nmap_scan_ip_and_mac', return_value=[{'ip': '192.168.1.2', 'mac': 'AA:BB:CC:DD:EE:FF'}])
    @patch('models.wifi_model.add_port_suffix_to_devices', return_value=[{'ip': '192.168.1.2', 'mac': 'AA:BB:CC:DD:EE:FF', 'ip_with_port': '192.168.1.2:81'}])
    def test_get_ap_connected_devices(self, mock_add_port_suffix_to_devices, mock_run_nmap_scan_ip_and_mac, mock_calculate_network, mock_get_ip_and_mask):
        result = get_ap_connected_devices()
        self.assertEqual(result, [{'ip': '192.168.1.2', 'mac': 'AA:BB:CC:DD:EE:FF', 'ip_with_port': '192.168.1.2:81'}])

if __name__ == '__main__':
    unittest.main()