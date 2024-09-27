### README: The Farmer Was Replaced Translation Project

## Project Overview
This project focuses on translating the game **[The Farmer Was Replaced](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/)** from English to French. The game involves programming and automating a drone to optimize farming tasks using a Python-like language.

## Features
- **Automatic Translation**: Translates in-game text files (`.txt`, `.md`) to French while preserving structure.
- **Customizable Prompts**: Supports specific translation prompts for each file type.
- **Error Handling**: Logs errors during translation and handles edge cases.

## Requirements
- `Python 3.8+`
- `openai`, `pyyaml`, `tqdm`

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Add your OpenAI API key to `config.yaml`.

## Usage
Run the translation script:
```bash
python main.py
```

## Contribution
Feel free to contribute or report issues.