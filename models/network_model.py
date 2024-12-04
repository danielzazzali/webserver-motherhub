import ipaddress
import re
import subprocess


from config.constants import NMCLI_GET_IP4_ADDRESS, NMAP_SCAN_NO_PORT, NMAP_IP_PATTERN, NMAP_MAC_PATTERN, \
    MAC_PREFIX_FOR_RASPBERRY, DAUGHTERBOX_WEBSERVER_PORT


def get_ip_and_mask(connection) -> dict:
    """
    Retrieves the IP address and subnet mask for the specified network interface.

    Args:
        connection (str): The name of the network connection (e.g., 'WLAN', 'ETH').

    Returns:
        dict: A dictionary containing the IP address and subnet mask with the key 'ip'.

    Raises:
        RuntimeError: If the command to fetch network details fails.
        ValueError: If the IP address and mask cannot be found.
    """

    command = NMCLI_GET_IP4_ADDRESS.format(connection)

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to execute command '{command}'. Error: {result.stderr}")

    ip, mask = None, None

    for line in result.stdout.splitlines():
        if 'IP4.ADDRESS' in line:
            parts = line.split(':')
            ip_mask = parts[1].strip()
            ip, mask = ip_mask.split('/')
            break

    if ip is None or mask is None:
        raise ValueError("Could not find the IP address and mask for the connection 'AP'.")

    return {'ip': ip, 'mask': mask}


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
        network = ipaddress.IPv4Network(f'{ip}/{mask}', strict=False)
        return f"{network.network_address}/{mask}"
    except ValueError as e:
        # Return an empty string if there's an issue with the calculation
        print(f"Error in network calculation: {e}")
        return ""


def run_nmap_scan_ip_and_mac(network: str) -> list:
    """
    Runs nmap to discover devices on the specified network and retrieves their IP and MAC addresses,
    filtering only those whose MAC addresses start with the specified Raspberry Pi prefix.

    Args:
        network (str): The network address in CIDR format (e.g., '192.168.1.0/24').

    Returns:
        list: A list of dictionaries with the IP and MAC addresses of the discovered devices
              that match the Raspberry Pi MAC prefix.
              Example: [{"ip": "192.168.1.1", "mac": "B8:27:EB:AA:BB:CC"}, ...]
    """
    try:
        # Run the nmap command to perform a ping scan on the specified network
        result = subprocess.run(
            NMAP_SCAN_NO_PORT.format(network),
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )

        devices = []  # List to store discovered devices matching the MAC prefix
        lines = result.stdout.splitlines()  # Split output into lines for processing

        # Compile regular expressions to match IP and MAC address patterns
        ip_pattern = re.compile(NMAP_IP_PATTERN)
        mac_pattern = re.compile(NMAP_MAC_PATTERN)

        current_ip = None  # Variable to hold the current IP address being processed

        for line in lines:
            # Look for IP address lines without parentheses (to exclude the scanning device's IP)
            if "(" not in line:
                ip_match = ip_pattern.search(line)
                if ip_match:
                    current_ip = ip_match.group(1)  # Extract the IP address

            # Look for MAC address lines following an IP address
            mac_match = mac_pattern.search(line)
            if mac_match and current_ip:
                mac = mac_match.group(1)  # Extract the MAC address
                # Check if the MAC address starts with the Raspberry Pi prefix
                if mac.startswith(MAC_PREFIX_FOR_RASPBERRY):
                    devices.append({"ip": current_ip, "mac": mac})  # Store the IP-MAC pair
                current_ip = None  # Reset the current IP after storing or discarding

        return devices

    except subprocess.CalledProcessError as e:
        # Handle errors that occur during the execution of the nmap command
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
        device['ip_with_port'] = f"{device['ip']}{':'}{DAUGHTERBOX_WEBSERVER_PORT}"

    return devices

