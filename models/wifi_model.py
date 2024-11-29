import subprocess

from config.config import get_env_variable
from config.constants import WIRELESS_CONNECTION, NMCLI_GET_CONNECTION_SSID_AND_PASSWORD, NMCLI_SSID_KEY, \
    NMCLI_PASSWORD_KEY, NMCLI_CHANGE_AP_SSID, NMCLI_CHANGE_AP_PASSWORD, NMCLI_BRING_CONNECTION_DOWN, \
    NMCLI_BRING_CONNECTION_UP, NMCLI_STATE_ACTIVATED_VALUE, NMCLI_GET_STATE_OF_CONNECTION
from models.network_model import get_ip_and_mask, calculate_network, run_nmap_scan_ip_and_mac, \
    add_port_suffix_to_devices


def get_ap_ssid_and_password() -> dict:
    """
    Retrieves the SSID and password of the Access Point (AP) using nmcli.

    Returns:
        dict: A dictionary containing the SSID and password of the AP.
    """
    try:
        # Get the wireless connection name from the environment
        connection_name = get_env_variable(WIRELESS_CONNECTION)

        # Run the nmcli command to get the AP information
        command = NMCLI_GET_CONNECTION_SSID_AND_PASSWORD.format(connection_name)
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        if result.returncode != 0:
            raise RuntimeError(f"Failed to execute command '{command}'. Error: {result.stderr}")

        # Parse the output to get SSID and password
        ap_info = {}
        for line in result.stdout.splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if key == NMCLI_SSID_KEY:
                    ap_info["ssid"] = value
                elif key == NMCLI_PASSWORD_KEY:
                    ap_info["password"] = value

        return ap_info

    except subprocess.CalledProcessError as e:
        print(f"Error running nmcli: {e}")
        return {}

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}


def change_ap_ssid(new_ssid: str) -> bool:
    """
    Changes the SSID of the specified connection using nmcli.

    Args:
        new_ssid (str): The new SSID to set.

    Returns:
        bool: True if the SSID was changed successfully, False otherwise.
    """
    try:
        # Check if the connection is active before bringing it down
        if is_ap_connection_active() and not bring_ap_connection_down():
            return False

        # Get the wireless connection name from the environment
        connection_name = get_env_variable(WIRELESS_CONNECTION)

        # Command to change the SSID
        command = NMCLI_CHANGE_AP_SSID.format(connection_name, new_ssid)
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        if result.returncode != 0:
            print(f"Failed to execute command '{command}'. Error: {result.stderr}")
            return False

        # Bring the connection back up after changing the SSID
        if not bring_ap_connection_up():
            return False

        return True

    except subprocess.CalledProcessError as e:
        print(f"Error running nmcli: {e}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def change_ap_password(new_password: str) -> bool:
    """
    Changes the password of the specified connection using nmcli.

    Args:
        new_password (str): The new password to set.

    Returns:
        bool: True if the password was changed successfully, False otherwise.
    """
    try:
        # Check if the connection is active before bringing it down
        if is_ap_connection_active() and not bring_ap_connection_down():
            return False

        # Get the wireless connection name from the environment
        connection_name = get_env_variable(WIRELESS_CONNECTION)

        # Command to change the password
        command = NMCLI_CHANGE_AP_PASSWORD.format(connection_name, new_password)
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        if result.returncode != 0:
            print(f"Failed to execute command '{command}'. Error: {result.stderr}")
            return False

        # Bring the connection back up after changing the password
        if not bring_ap_connection_up():
            return False

        return True

    except subprocess.CalledProcessError as e:
        print(f"Error running nmcli: {e}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def bring_ap_connection_down() -> bool:
    """
    Brings the specified connection down using nmcli.

    Returns:
        bool: True if the connection was brought down successfully, False otherwise.
    """
    try:
        connection_name = get_env_variable(WIRELESS_CONNECTION)
        command = NMCLI_BRING_CONNECTION_DOWN.format(connection_name)
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        if result.returncode != 0:
            print(f"Failed to execute command '{command}'. Error: {result.stderr}")
            return False

        return True

    except subprocess.CalledProcessError as e:
        print(f"Error running nmcli: {e}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def bring_ap_connection_up() -> bool:
    """
    Brings the specified connection up using nmcli.

    Returns:
        bool: True if the connection was brought up successfully, False otherwise.
    """
    try:
        connection_name = get_env_variable(WIRELESS_CONNECTION)
        command = NMCLI_BRING_CONNECTION_UP.format(connection_name)
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        if result.returncode != 0:
            print(f"Failed to execute command '{command}'. Error: {result.stderr}")
            return False

        return True

    except subprocess.CalledProcessError as e:
        print(f"Error running nmcli: {e}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def is_ap_connection_active() -> bool:
    """
    Checks if the specified connection is active using nmcli.

    Returns:
        bool: True if the connection is active, False otherwise.
    """
    try:
        connection_name = get_env_variable(WIRELESS_CONNECTION)
        command = NMCLI_GET_STATE_OF_CONNECTION.format(connection_name)
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        if result.returncode != 0:
            print(f"Failed to execute command '{command}'. Error: {result.stderr}")
            return False

        state = result.stdout.strip().split(':')[-1]
        return state == NMCLI_STATE_ACTIVATED_VALUE

    except subprocess.CalledProcessError as e:
        print(f"Error running nmcli: {e}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def get_ap_connected_devices() -> list:
    """
    Retrieves the connected devices on the wireless connection network.

    Returns:
        list: A list of dictionaries with IP, MAC addresses, and IP with port suffix of the connected devices,
              or an empty list if an error occurs.
              Example: [{"ip": "192.168.1.1", "mac": "AA:BB:CC:DD:EE:FF", "ip_with_port": "192.168.1.1:81"}, ...]
    """
    try:
        # Get the network interface name from the environment
        connection = get_env_variable(WIRELESS_CONNECTION)

        # Get the IP and subnet mask of the interface
        ip, mask = get_ip_and_mask(connection)
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