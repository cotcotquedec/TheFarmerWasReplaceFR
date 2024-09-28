import os
import shutil
from helpers import logger, config  # Import config for language directories

try:
    # Ensure the 'language_folder' key is available in the configuration
    if "language_folder" not in config:
        raise KeyError("The 'language_folder' key is missing from the configuration. Please define it in your config file.")

    # Retrieve the language folder from the configuration
    base_path = config["language_folder"]

    # Define base directories
    en_path = os.path.join(base_path, "EN")
    fr_path = os.path.join(base_path, "FR")
    original_en_path = os.path.join(base_path, "original_EN")

    # Check if the original_EN folder exists as a backup
    if not os.path.exists(original_en_path):
        raise FileNotFoundError("The 'original_EN' backup folder does not exist. Please ensure you have a backup of the original English files before installing the translation.")

    # Check if the French translation folder exists
    if not os.path.exists(fr_path):
        raise FileNotFoundError(f"The 'FR' folder does not exist. Please ensure the French translation is available in {fr_path}.")

    # DELETE the current EN folder if it exists
    if os.path.exists(en_path):
        shutil.rmtree(en_path)
        logger.info(f"The folder {en_path} has been deleted.")

    # COPY FRENCH TO EN
    shutil.copytree(fr_path, en_path)
    logger.info(f"The folder {fr_path} has been copied to {en_path}. The French translation is now installed.")

    # Log a final confirmation message
    logger.info("French translation has been successfully installed.")

except KeyError as key_error:
    logger.error(f"Configuration error: {key_error}")
    raise key_error  # Re-raise the exception to notify the user
except FileNotFoundError as fnf_error:
    logger.error(f"File not found error: {fnf_error}")
    raise fnf_error  # Re-raise the exception to notify the user
except Exception as e:
    logger.error(f"An unexpected error occurred: {e}")
