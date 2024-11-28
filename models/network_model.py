import ipaddress
import re
import subprocess

from config.constants import WIRELESS_NETWORK_INTERFACE_KEY, IPV4_CIDR_PREFIX, IP_COMMAND_TEMPLATE, \
    NMAP_COMMAND_TEMPLATE, MAC_PREFIX, IP_PATTERN, MAC_PATTERN, PORT_SUFFIX
from config.config import get_env_variable


def get_ip_and_mask(interface: str) -> tuple:
    """
    Retrieves the IP address and subnet mask for the specified network interface.

    Args:
        interface (str): The name of the network interface (e.g., 'eno1').

    Returns:
        tuple: A tuple containing the IP address and subnet mask (e.g., ('192.168.1.10', '255.255.255.0')).

    Raises:
        RuntimeError: If the command to fetch network details fails.
        ValueError: If the IP address and mask cannot be found.
    """
    command = IP_COMMAND_TEMPLATE.format(interface)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to execute command '{command}'. Error: {result.stderr}")

    ip, mask = None, None

    for line in result.stdout.splitlines():
        if 'inet ' in line:
            parts = line.strip().split()
            ip_mask = parts[1]
            ip, mask = ip_mask.split('/')
            break

    if ip is None or mask is None:
        raise ValueError(f"Could not find the IP address and mask for the interface '{interface}'.")

    return ip, mask


def calculate_network(ip: str, mask: str) -> str:
    """
    Calculates the network address given an IP address and a subnet mask.

    Args:
        ip (str): The IP address in the format 'x.x.x.x'.
        mask (str): The subnet mask in the format 'x.x.x.x'.

    Returns:
        str: The network address in the format 'x.x.x.x/mask'.
    """
    try:
        # Create an IP network object using the IP address and mask
        network = ipaddress.IPv4Network(f'{ip}{IPV4_CIDR_PREFIX}{mask}', strict=False)
        return f"{network.network_address}{IPV4_CIDR_PREFIX}{mask}"
    except ValueError as e:
        # Return an empty string if there's an issue with the calculation
        print(f"Error in network calculation: {e}")
        return ""


def run_nmap_scan_ip_and_mac(network: str) -> list:
    """
    Runs nmap to discover devices in the given network and retrieves their IP and MAC addresses.

    Args:
        network (str): The network address in CIDR format (e.g., '192.168.1.0/24').

    Returns:
        list: A list of dictionaries with IP and MAC addresses of the discovered devices.
              Example: [{"ip": "192.168.1.1", "mac": "AA:BB:CC:DD:EE:FF"}, ...]
    """
    try:
        # Run nmap to discover devices
        result = subprocess.run(
            NMAP_COMMAND_TEMPLATE.format(network),
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        devices = []
        lines = result.stdout.splitlines()

        # Compile regex patterns
        ip_pattern = re.compile(IP_PATTERN)
        mac_pattern = re.compile(MAC_PATTERN)

        current_ip = None

        for line in lines:
            ip_match = ip_pattern.search(line)
            mac_match = mac_pattern.search(line)

            if ip_match:
                current_ip = ip_match.group(1)
            if mac_match and current_ip:
                mac = mac_match.group(1)
                # Filter devices by MAC address prefix
                if mac.startswith(MAC_PREFIX):
                    devices.append({"ip": current_ip, "mac": mac})
                current_ip = None  # Reset after capturing IP-MAC pair

        return devices

    except subprocess.CalledProcessError as e:
        print(f"Error running nmap: {e}")
        return []


def add_port_suffix_to_devices(devices: list) -> list:
    """
    Adds a port suffix to the IP address of each device in the list.

    Args:
        devices (list): A list of dictionaries with IP and MAC addresses of the discovered devices.
                        Example: [{"ip": "192.168.1.1", "mac": "AA:BB:CC:DD:EE:FF"}, ...]

    Returns:
        list: A list of dictionaries with IP, MAC addresses, and IP with port suffix.
              Example: [{"ip": "192.168.1.1", "mac": "AA:BB:CC:DD:EE:FF", "ip_with_port": "192.168.1.1:81"}, ...]
    """
    if not isinstance(devices, list):
        raise ValueError("The 'devices' parameter must be a list.")

    for device in devices:
        if not isinstance(device, dict):
            raise ValueError("Each device must be a dictionary.")
        if 'ip' not in device:
            raise KeyError("Each device dictionary must contain an 'ip' key.")
        device['ip_with_port'] = f"{device['ip']}{PORT_SUFFIX}"

    return devices

def get_connected_devices() -> list:
    """
    Retrieves the connected devices on the network.

    Returns:
        list: A list of dictionaries with IP, MAC addresses, and IP with port suffix of the connected devices,
              or an empty list if an error occurs.
              Example: [{"ip": "192.168.1.1", "mac": "AA:BB:CC:DD:EE:FF", "ip_with_port": "192.168.1.1:81"}, ...]
    """
    try:
        # Get the network interface name from the environment
        interface = get_env_variable(WIRELESS_NETWORK_INTERFACE_KEY)
        if not interface:
            print(f"Error: Environment variable '{WIRELESS_NETWORK_INTERFACE_KEY}' is missing.")
            return []

        # Get the IP and subnet mask of the interface
        ip, mask = get_ip_and_mask(interface)
        if not ip or not mask:
            print("Error: IP address or subnet mask could not be retrieved.")
            return []

        # Calculate the network address
        network = calculate_network(ip, mask)
        if not network:
            print("Error: Invalid network address.")
            return []

        # Run the nmap scan and get the devices
        mapped_devices = run_nmap_scan_ip_and_mac(network)
        if not mapped_devices:
            print("Error: No devices found on the network.")
            return []

        # Add port suffix to the devices
        devices = add_port_suffix_to_devices(mapped_devices)

        return devices

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
