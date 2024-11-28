# Network interface variable key in the environment
WIRELESS_NETWORK_INTERFACE_KEY = 'WIRELESS_NETWORK_INTERFACE'
WIRELESS_CONNECTION_NAME_KEY = 'WIRELESS_CONNECTION_NAME'
MODE_FILE_PATH = 'MODE_FILE_PATH'

# Subnet mask prefix length (CIDR) for IPv4 addresses
IPV4_CIDR_PREFIX = '/'

# Command to get IP and mask
IP_COMMAND_TEMPLATE = "ip addr show dev {}"

# Nmap command template
NMAP_COMMAND_TEMPLATE = "sudo nmap -sP {}"

# Define regex patterns for extracting IP and MAC addresses from nmap output
IP_PATTERN = r"Nmap scan report for (\S+)"
MAC_PATTERN = r"MAC Address: ([0-9A-F:]+)"

# Define the MAC prefix
MAC_PREFIX = "B8:27:EB"

# Port to access Daughter box webserver
PORT_SUFFIX = ":81"

NMCLI_COMMAND_TEMPLATE = "nmcli connection show {} --show-secrets"

SSID_KEY = "802-11-wireless.ssid"
PASSWORD_KEY = "802-11-wireless-security.psk"

NMCLI_COMMAND_CHANGE_SSID_TEMPLATE = "nmcli connection modify {} 802-11-wireless.ssid {}"
NMCLI_COMMAND_CHANGE_PASSWORD_TEMPLATE = "nmcli connection modify {} 802-11-wireless-security.psk {}"

NMCLI_COMMAND_DOWN_TEMPLATE = "nmcli connection down {}"
NMCLI_COMMAND_UP_TEMPLATE = "nmcli connection up {}"