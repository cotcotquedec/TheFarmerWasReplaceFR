import os
from helpers import logger, client_openai
from pydantic import BaseModel
from tqdm import tqdm

# Load prompt files
prompt_md_file = "prompt_md.txt"
if not os.path.isfile(prompt_md_file):
    raise Exception(f"Unable to find {prompt_md_file}")
with open(prompt_md_file, 'r', encoding='utf-8') as file:
    prompt_md = file.read()

prompt_txt_file = "prompt_txt.txt"
if not os.path.isfile(prompt_txt_file):
    raise Exception(f"Unable to find {prompt_txt_file}")
with open(prompt_txt_file, 'r', encoding='utf-8') as file:
    prompt_txt = file.read()

# Class to store the translated content
class TranslatedContent(BaseModel):
    content: str

# Function to translate the content based on the file type
def translate_content(content, file_extension):
    # Select the appropriate prompt based on the file extension
    if file_extension == ".txt":
        prompt = prompt_txt
    elif file_extension == ".md":
        prompt = prompt_md
    else:
        raise Exception(f"No prompt available for the file extension: {file_extension}")   

    # Send the message to the OpenAI API
    response = client_openai.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": [{"type": "text","text": prompt.format(content=content)}]}],
        response_format=TranslatedContent,
        temperature=0.3
    )

    # Handle the response
    if not response.choices or len(response.choices) == 0:
        raise Exception("No choices returned from the LLM call.")
    choice = response.choices[0]

    if not choice.message:
        raise Exception("No message content returned from the LLM call.")
    message = choice.message

    # Parse the assistant's reply into the Page data model
    content: TranslatedContent = message.parsed

    return content

if __name__ == "__main__":
    # Count the total number of files for progress tracking
    total_files = sum(len(files) for _, _, files in os.walk('game_files/EN'))

    logger.info(f"Number of files to translate: {total_files}")

    # Create the tqdm progress bar
    with tqdm(total=total_files, desc="Translating files", unit="file") as pbar:

        for root_dir, sub_dirs, files in os.walk('game_files/EN'):
            for file in files:
                try:
                    # Full path of the current file
                    full_path = os.path.join(root_dir, file)

                    # Read the content of the file
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Call the translate function with content and file extension
                    file_extension = os.path.splitext(file)[1]
                    translated_content = translate_content(content, file_extension.strip())

                    # Create the new path by replacing 'EN' with 'FR'
                    new_path = root_dir.replace('/EN/', '/FR/')
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
