import os

def get_mode() -> str:
    """
    Retrieves the mode from the file specified by the MODE_FILE_PATH environment variable.
    The mode can only be 'AP' or 'STA'.

    Returns:
        str: The mode ('AP' or 'STA').

    Raises:
        ValueError: If the mode is not 'AP' or 'STA'.
        FileNotFoundError: If the mode file does not exist.
    """
    mode_file_path = os.getenv('MODE_FILE_PATH')
    if not mode_file_path:
        raise EnvironmentError("MODE_FILE_PATH environment variable is not set")

    if not os.path.exists(mode_file_path):
        raise FileNotFoundError(f"Mode file not found at path: {mode_file_path}")

    with open(mode_file_path, 'r') as file:
        mode = file.read().strip()

    if mode not in ['AP', 'STA']:
        raise ValueError("Mode must be either 'AP' or 'STA'")

    return mode


def set_mode(new_mode: str):
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

    mode_file_path = os.getenv('MODE_FILE_PATH')
    if not mode_file_path:
        raise EnvironmentError("MODE_FILE_PATH environment variable is not set")

    if not os.path.exists(mode_file_path):
        raise FileNotFoundError(f"Mode file not found at path: {mode_file_path}")

    with open(mode_file_path, 'w') as file:
        file.write(new_mode)

    reboot_system()


def reboot_system():
    """
    Reboots the system.
    """
    os.system('sudo reboot')