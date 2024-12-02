PORT = 'PORT'

ETHERNET_CONNECTION = 'ETHERNET_CONNECTION'
WIRELESS_CONNECTION = 'WIRELESS_CONNECTION'

DEVICE_MODE_FILE_PATH = 'DEVICE_MODE_FILE_PATH'

REBOOT_SYSTEM = "sudo reboot"
SHUTDOWN_SYSTEM = "sudo shutdown -h now"

NMCLI_GET_IP4_ADDRESS = "nmcli -f IP4.ADDRESS connection show {}"
NMCLI_GET_CONNECTION_SSID_AND_PASSWORD = "nmcli connection show {} --show-secrets"
NMCLI_CHANGE_AP_SSID = "nmcli connection modify {} 802-11-wireless.ssid {}"
NMCLI_CHANGE_AP_PASSWORD = "nmcli connection modify {} 802-11-wireless-security.psk {}"
NMCLI_BRING_CONNECTION_DOWN = "nmcli connection down {}"
NMCLI_BRING_CONNECTION_UP = "nmcli connection up {}"
NMCLI_GET_STATE_OF_CONNECTION = "nmcli -t -f GENERAL.STATE connection show {}"

NMCLI_SSID_KEY = "802-11-wireless.ssid"
NMCLI_PASSWORD_KEY = "802-11-wireless-security.psk"
NMCLI_STATE_ACTIVATED_VALUE = "activated"

NMAP_SCAN_NO_PORT = "sudo nmap -sn {}"

NMAP_IP_PATTERN = r"Nmap scan report for (\d{1,3}(?:\.\d{1,3}){3})"
NMAP_MAC_PATTERN = r"MAC Address: ([0-9A-F:]+)"

MAC_PREFIX_FOR_RASPBERRY = "B8:27:EB"

DAUGHTERBOX_WEBSERVER_PORT = ":81"
