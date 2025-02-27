import argparse
import logging
import os

from dotenv import load_dotenv


def load_environment():
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="Load environment configuration")
    parser.add_argument("--env", type=str, help="Current environment", default="local")
    args, _ = parser.parse_known_args()

    env_name=os.getenv("env", args.env)
    env_path: str = f"src/environments/.env.{env_name}"

    # Load environment variables from the specified file
    if os.path.exists(env_path):
        logging.debug(f"Loading environment from file {env_path}")
        correctly_loaded: bool = load_dotenv(env_path)

        if correctly_loaded:
            logging.debug("Environment loaded successfully!")
        else:
            raise EnvironmentError(f"Error loading environment file {env_path}!")
    else:
        raise FileNotFoundError(f"Environment file '{env_path}' not found!")