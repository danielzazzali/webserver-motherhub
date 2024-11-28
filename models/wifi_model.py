import subprocess

from config.config import get_env_variable
from config.constants import NMCLI_COMMAND_TEMPLATE, SSID_KEY, PASSWORD_KEY, WIRELESS_CONNECTION_NAME_KEY, \
    NMCLI_COMMAND_CHANGE_SSID_TEMPLATE, NMCLI_COMMAND_UP_TEMPLATE, NMCLI_COMMAND_DOWN_TEMPLATE, \
    NMCLI_COMMAND_CHANGE_PASSWORD_TEMPLATE


def get_ap_info() -> dict:
    """
    Retrieves the SSID and password of the Access Point (AP) using nmcli.

    Returns:
        dict: A dictionary containing the SSID and password of the AP.
    """
    try:
        # Get the wireless connection name from the environment
        connection_name = get_env_variable(WIRELESS_CONNECTION_NAME_KEY)

        # Run the nmcli command to get the AP information
        command = NMCLI_COMMAND_TEMPLATE.format(connection_name)
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
                if key == SSID_KEY:
                    ap_info["ssid"] = value
                elif key == PASSWORD_KEY:
                    ap_info["password"] = value

        return ap_info

    except subprocess.CalledProcessError as e:
        print(f"Error running nmcli: {e}")
        return {}

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}



def change_ssid(new_ssid: str) -> bool:
    """
    Changes the SSID of the specified connection using nmcli.

    Args:
        new_ssid (str): The new SSID to set.

    Returns:
        bool: True if the SSID was changed successfully, False otherwise.
    """
    try:
        # Check if the connection is active before bringing it down
        if is_connection_active() and not bring_connection_down():
            return False

        # Get the wireless connection name from the environment
        connection_name = get_env_variable(WIRELESS_CONNECTION_NAME_KEY)

        # Command to change the SSID
        command = NMCLI_COMMAND_CHANGE_SSID_TEMPLATE.format(connection_name, new_ssid)
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        if result.returncode != 0:
            print(f"Failed to execute command '{command}'. Error: {result.stderr}")
            return False

        # Bring the connection back up after changing the SSID
        if not bring_connection_up():
            return False

        return True

    except subprocess.CalledProcessError as e:
        print(f"Error running nmcli: {e}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def change_password(new_password: str) -> bool:
    """
    Changes the password of the specified connection using nmcli.

    Args:
        new_password (str): The new password to set.

    Returns:
        bool: True if the password was changed successfully, False otherwise.
    """
    try:
        # Check if the connection is active before bringing it down
        if is_connection_active() and not bring_connection_down():
            return False

        # Get the wireless connection name from the environment
        connection_name = get_env_variable(WIRELESS_CONNECTION_NAME_KEY)

        # Command to change the password
        command = NMCLI_COMMAND_CHANGE_PASSWORD_TEMPLATE.format(connection_name, new_password)
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        if result.returncode != 0:
            print(f"Failed to execute command '{command}'. Error: {result.stderr}")
            return False

        # Bring the connection back up after changing the password
        if not bring_connection_up():
            return False

        return True

    except subprocess.CalledProcessError as e:
        print(f"Error running nmcli: {e}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def bring_connection_down() -> bool:
    """
    Brings the specified connection down using nmcli.

    Returns:
        bool: True if the connection was brought down successfully, False otherwise.
    """
    try:
        connection_name = get_env_variable(WIRELESS_CONNECTION_NAME_KEY)
        command = NMCLI_COMMAND_DOWN_TEMPLATE.format(connection_name)
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


def bring_connection_up() -> bool:
    """
    Brings the specified connection up using nmcli.

    Returns:
        bool: True if the connection was brought up successfully, False otherwise.
    """
    try:
        connection_name = get_env_variable(WIRELESS_CONNECTION_NAME_KEY)
        command = NMCLI_COMMAND_UP_TEMPLATE.format(connection_name)
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


def is_connection_active() -> bool:
    """
    Checks if the specified connection is active using nmcli.

    Returns:
        bool: True if the connection is active, False otherwise.
    """
    try:
        connection_name = get_env_variable(WIRELESS_CONNECTION_NAME_KEY)
        command = f"nmcli -t -f NAME,STATE connection show --active"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        if result.returncode != 0:
            print(f"Failed to execute command '{command}'. Error: {result.stderr}")
            return False

        active_connections = result.stdout.splitlines()
        for line in active_connections:
            name, state = line.split(':')
            if name == connection_name and state == 'activated':
                return True

        return False

    except subprocess.CalledProcessError as e:
        print(f"Error running nmcli: {e}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False