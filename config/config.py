import os


def load_env(file_path: str = '.env'):
    """
    Loads environment variables from a .env file into the OS environment variables.

    Args:
        file_path (str): The path to the .env file (default is '.env').

    Raises:
        FileNotFoundError: If the .env file is not found.
    """
    if os.path.exists(file_path):
        with open(file_path) as f:
            for line in f:
                # Skip empty lines or comments
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    else:
        raise FileNotFoundError(f"{file_path} not found!")


def get_env_variable(key: str, default=None) -> str:
    """
    Retrieves an environment variable by key.

    Args:
        key (str): The key of the environment variable.
        default: The default value to return if the variable is not set.

    Returns:
        str: The value of the environment variable.
    """
    return os.getenv(key, default)
