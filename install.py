import os
import shutil
from helpers import logger, client_openai, config  # Import config for language directories
from pydantic import BaseModel
from tqdm import tqdm

try:
    # Ensure the language configuration is available
    if "language_folder" not in config:
        raise KeyError("The 'language_folder' key is missing from the configuration. Please define it in your config file.")

    # Define base language directories
    en_directory = os.path.join(config["language_folder"], "EN")
    fr_directory = os.path.join(config["language_folder"], "FR")
    original_en_directory = os.path.join(config["language_folder"], "original_EN")

    # BACKUP ORIGINAL
    if not os.path.exists(original_en_directory):
        if not os.path.exists(en_directory):
            raise FileNotFoundError(f"The directory {en_directory} does not exist and no backup is available. Please ensure the game is correctly installed.")
        # Copy the EN directory to original_EN
        shutil.copytree(en_directory, original_en_directory)
        logger.info(f"Directory {en_directory} copied to {original_en_directory} as a backup.")

    # Load prompt files for translation
    prompt_md_file = "prompt_md.txt"
    prompt_txt_file = "prompt_txt.txt"

    # Check if prompt files are available
    if not os.path.isfile(prompt_md_file):
        raise FileNotFoundError(f"Unable to find {prompt_md_file}. Make sure the file exists in the working directory.")
    if not os.path.isfile(prompt_txt_file):
        raise FileNotFoundError(f"Unable to find {prompt_txt_file}. Make sure the file exists in the working directory.")

    # Read prompt contents
    with open(prompt_md_file, 'r', encoding='utf-8') as file:
        prompt_md = file.read()

    with open(prompt_txt_file, 'r', encoding='utf-8') as file:
        prompt_txt = file.read()

    # STRUCTURE FOR OPENAI RESPONSE
    class TranslatedContent(BaseModel):
        content: str

    # Function to translate content based on file type
    def translate_content(content, file_extension):
        # Select the appropriate prompt based on the file extension
        if file_extension == ".txt":
            prompt = prompt_txt
        elif file_extension == ".md":
            prompt = prompt_md
        else:
            raise ValueError(f"No prompt available for the file extension: {file_extension}")

        # Send the message to the OpenAI API
        response = client_openai.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[{"role": "user", "content": [{"type": "text", "text": prompt.format(content=content)}]}],
            response_format=TranslatedContent,
            temperature=0.3
        )

        # Handle the response
        if not response.choices or len(response.choices) == 0:
            raise RuntimeError("No choices returned from the LLM call.")
        choice = response.choices[0]

        if not choice.message:
            raise RuntimeError("No message content returned from the LLM call.")
        message = choice.message

        # Parse the assistant's reply into the Page data model
        translated_content: TranslatedContent = message.parsed

        return translated_content

    # Count the total number of files for progress tracking
    total_files = sum(len(files) for _, _, files in os.walk(original_en_directory))
    logger.info(f"Number of files to translate: {total_files}")

    # Create the tqdm progress bar
    with tqdm(total=total_files, desc="Translating files", unit="file") as pbar:
        for root_dir, sub_dirs, files in os.walk(original_en_directory):
            for file in files:
                full_path = os.path.join(root_dir, file)
                try:
                    # Read the content of the file
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Call the translate function with content and file extension
                    file_extension = os.path.splitext(file)[1]
                    translated_content = translate_content(content, file_extension.strip())

                    # Create the new path by replacing 'original_EN' with 'FR'
                    new_path = root_dir.replace('original_EN', 'FR')
                    os.makedirs(new_path, exist_ok=True)  # Create the directories if they don't exist

                    # Full path for the translated file
                    translated_file_path = os.path.join(new_path, file)

                    # Write the translated content to the new file
                    with open(translated_file_path, 'w', encoding='utf-8') as f:
                        f.write(translated_content.content)

                except Exception as e:
                    logger.error(f"Error processing file [{full_path}]: {e}", exc_info=True)

                # Update the progress bar
                pbar.update(1)

except KeyError as key_error:
    logger.error(f"Configuration error: {key_error}")
    raise key_error  # Re-raise the exception to notify the user
except FileNotFoundError as fnf_error:
    logger.error(f"File not found error: {fnf_error}")
except Exception as e:
    logger.error(f"An unexpected error occurred: {e}")
    raise e  # Re-raise the exception to notify the user
