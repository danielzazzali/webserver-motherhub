import os
import threading

from config.constants import DEVICE_MODE_FILE_PATH, REBOOT_SYSTEM, SHUTDOWN_SYSTEM


def get_device_mode() -> str:
    """
    Retrieves the mode from the file specified by the MODE_FILE_PATH environment variable.
    The mode can only be 'AP' or 'STA'.

    Returns:
        str: The mode ('AP' or 'STA').

    Raises:
        ValueError: If the mode is not 'AP' or 'STA'.
        FileNotFoundError: If the mode file does not exist.
    """
    mode_file_path = DEVICE_MODE_FILE_PATH
    if not mode_file_path:
        raise EnvironmentError(f"{DEVICE_MODE_FILE_PATH} environment variable is not set")

    if not os.path.exists(mode_file_path):
        raise FileNotFoundError(f"Mode file not found at path: {mode_file_path}")

    with open(mode_file_path, 'r') as file:
        mode = file.read().strip()

    if mode not in ['AP', 'STA']:
        raise ValueError("Mode must be either 'AP' or 'STA'")

    return mode


def set_device_mode(new_mode: str):
    """
    Sets the mode in the file specified by the MODE_FILE_PATH environment variable.
    The mode can only be 'AP' or 'STA'.

    Args:
        new_mode (str): The new mode to set ('AP' or 'STA').

    Raises:
        ValueError: If the new mode is not 'AP' or 'STA'.
        EnvironmentError: If the MODE_FILE_PATH environment variable is not set.
        FileNotFoundError: If the mode file does not exist.
    """
    if new_mode not in ['AP', 'STA']:
        raise ValueError("Mode must be either 'AP' or 'STA'")

    mode_file_path = DEVICE_MODE_FILE_PATH
    if not mode_file_path:
        raise EnvironmentError(f"{DEVICE_MODE_FILE_PATH} environment variable is not set")

    if not os.path.exists(mode_file_path):
        raise FileNotFoundError(f"Mode file not found at path: {mode_file_path}")

    with open(mode_file_path, 'w') as file:
        file.write(new_mode)

    reboot_system()


def reboot_system():
    """
    Reboots the system.
    """
    turn_off_i2c_display()
    os.system(REBOOT_SYSTEM)


def shutdown_system():
    """
    Shuts down the system.
    """
    turn_off_i2c_display()
    os.system(SHUTDOWN_SYSTEM)


def delayed_reboot():
    threading.Timer(3, reboot_system).start()

def delayed_shutdown():
    threading.Timer(3, shutdown_system).start()


def turn_off_i2c_display(bus: int = 1, address: str = "0x3C"):
    """
    Turns off an I2C display using the `i2cset` command available on Linux systems.

    Args:
        bus (int): I2C bus number.
        address (str): I2C address of the display in hexadecimal format (e.g., "0x3C").
    """
    try:
        os.system(f"i2cset -y {bus} {address} 0x00 0xAE")
    except Exception as e:
        print(f"Error turning off the I2C display: {e}")