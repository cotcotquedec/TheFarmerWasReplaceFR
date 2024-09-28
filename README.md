# The Farmer Was Replaced: French Translation Project

![Logo](./logo.png)

## Project Overview
This project focuses on translating the game **[The Farmer Was Replaced](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/)** from English to French. The game involves programming and automating a drone to optimize farming tasks using a Python-like language.

## Features
- **Automatic Translation**: Translates in-game text files (`.txt`, `.md`) to French while preserving structure.
- **Customizable Prompts**: Supports specific translation prompts for each file type.
- **Error Handling**: Logs errors during translation and handles edge cases.
- **Backup & Restore**: Automatically backs up the original game files and provides scripts to install and uninstall the translation.

## Requirements
- `Python 3.8+`
- `openai`, `pyyaml`, `tqdm`

## Setup
1. Purchase and install the game from [Steam](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/). The game is an excellent tool for learning programming, and projects like these help share the passion for coding.
2. Clone the repository.
   ```bash
   git clone https://github.com/your-repo/TheFarmerWasReplaced-FR-Translator.git
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the example configuration file and add your OpenAI API key to `config.yaml`:
   ```bash
   cp config.yaml.exemple config.yaml
   ```
   Edit `config.yaml` to add your OpenAI API key:
   ```yaml
   openai:
     apikey: sk-ABC********************************

   language_folder: '/path/to/SteamLibrary/steamapps/common/The Farmer Was Replaced/TheFarmerWasReplaced_Data/StreamingAssets/Languages'
   ```

## Translation Process

### 1. Generate the French Translation
To generate the French translation for the game files, run the `translate.py` script:
```bash
python translate.py
```
This will process all the English game files, translate them into French, and store them in a `FR` folder.

### 2. Install the French Translation
Once the translation is generated, install it by running the `install.py` script:
```bash
python install.py
```
This script will:
- Back up the original English files (if not already backed up).
- Replace the English files with the French translations.

### 3. Uninstall the French Translation
If you want to revert to the original English version of the game, run the `uninstall.py` script:
```bash
python uninstall.py
```
This script will:
- Remove the French translation.
- Restore the original English files from the backup.

## Folder Structure
- **Languages folder**: The game's language files are located in:
  ```bash
  SteamLibrary\steamapps\common\The Farmer Was Replaced\TheFarmerWasReplaced_Data\StreamingAssets\Languages
  ```
- **FR folder**: This folder is generated by the `translate.py` script and contains the translated files.

## Launch the Game
Once the French translation is installed, launch the game, and it should now be displayed in French!

## Contribution
Feel free to contribute by submitting issues, providing feedback, or creating pull requests. All contributions are welcome!