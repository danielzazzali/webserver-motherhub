import unittest
from unittest.mock import patch, MagicMock
from models.network_model import get_ip_and_mask, calculate_network, run_nmap_scan_ip_and_mac, add_port_suffix_to_devices

class TestNetworkModel(unittest.TestCase):

    @patch('models.network_model.subprocess.run')
    def test_get_ip_and_mask(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="IP4.ADDRESS[1]: 192.168.1.1/24\n")
        result = get_ip_and_mask('WLAN')
        self.assertEqual(result, {'ip': '192.168.1.1', 'mask': '24'})

    def test_calculate_network(self):
        result = calculate_network('192.168.1.1', '24')
        self.assertEqual(result, '192.168.1.0/24')

    @patch('models.network_model.subprocess.run')
    def test_run_nmap_scan_ip_and_mac(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="Nmap scan report for 192.168.1.2\nMAC Address: B8:27:EB:AA:BB:CC\n")
        result = run_nmap_scan_ip_and_mac('192.168.1.0/24')
        self.assertEqual(result, [{'ip': '192.168.1.2', 'mac': 'B8:27:EB:AA:BB:CC'}])

    def test_add_port_suffix_to_devices(self):
        devices = [{'ip': '192.168.1.2', 'mac': 'AA:BB:CC:DD:EE:FF'}]
        result = add_port_suffix_to_devices(devices)
        self.assertEqual(result, [{'ip': '192.168.1.2', 'mac': 'AA:BB:CC:DD:EE:FF', 'ip_with_port': '192.168.1.2:81'}])

if __name__ == '__main__':
    unittest.main()