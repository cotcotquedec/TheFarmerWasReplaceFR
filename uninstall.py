import os
import shutil
from helpers import logger, config  # Import config from helpers

try:
    # Check if the 'language_folder' is present in the configuration
    if "language_folder" not in config:
        raise KeyError("The 'language_folder' key is missing from the configuration. Please define it in your config file.")

    # Retrieve the language folder from the configuration
    base_path = config["language_folder"]

    # Define base directories
    en_path = os.path.join(base_path, "EN")
    original_en_path = os.path.join(base_path, "original_EN")

    # Check if the original_EN folder exists for restoration
    if not os.path.exists(original_en_path):
        raise FileNotFoundError("The 'original_EN' backup folder does not exist. Cannot uninstall translation without the original English files.")

    # DELETE the current EN folder if it exists
    if os.path.exists(en_path):
        shutil.rmtree(en_path)
        logger.info(f"The folder {en_path} has been deleted.")

    # RESTORE the original English language by copying original_EN to EN
    shutil.copytree(original_en_path, en_path)
    logger.info(f"The folder {original_en_path} has been copied back to {en_path}. The original English version is now restored.")

except KeyError as key_error:
    logger.error(f"Configuration error: {key_error}")
    raise key_error  # Re-raise the exception to notify the user
except FileNotFoundError as fnf_error:
    logger.error(f"File not found error: {fnf_error}")
except Exception as e:
    logger.error(f"An unexpected error occurred: {e}")
    raise e  # Re-raise the exception to notify the user
