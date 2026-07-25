# Persian Text-to-Phonetic Transcriber & Lexicon Lookup

A Python-based utility for Persian natural language processing that extracts phonetics, applies Ezafe additions based on context, spells out unknown words letter-by-letter, and simulates structured lexicon dictionary lookups.

---

## Features

* **Knowledge Base Loader (`load_knowledge_base`)**: Parses a dynamic Excel file (`Flexicon.xlsx`) into words, phonetic representations, POS tags, and spelling rules.
* **Persian Text Phonetic Transcriber (`process_text_file`)**:
  * Translates known Persian text into phonetic transcriptions.
  * Automatically detects and appends the **Ezafe** (`-e`) suffix for noun constructs.
  * Fallbacks to character-by-character spelling (`spell_out_word`) for terms absent from the lexicon.
* **Dictionary Attribute Lookup (`DictLookup`)**: Simulates structured dictionary API query functions using reference-like list containers.

---

## Requirements

Ensure you have Python installed along with the required dependencies:

```bash
pip install pandas openpyxl
```

## Usage
1. **Preparing the Knowledge Base**
    * Word
    * Phonetic Transcription
    * POS (Part-of-Speech Tag)
2. **Running the Script**
Execute the main script:
```Bash
python main.py
```
3. **Processing Input Text**
Write any Persian text in `input.txt`. For instance:
```Plaintext
رایانش کوانتومی
```
Running the code generates `output_phonetic.txt` containing the transcribed output with appropriate Ezafe connections:
```Plaintext
rAyAneS-e kiyubit
```

---

## Key Functions
`load_knowledge_base(excel_path)`
Reads the Excel dataset, extracts lexical maps, and builds a comprehensive dictionary database (`master_db`).

`DictLookup(word, att, val_container, database)`
Searches for a specific word and attribute in the database.
```Python
val_result = []
if DictLookup("رایانش", "POS", val_result, master_db):
    print(f"POS: {val_result[0]}")  # Output: N1
```
`spell_out_word(word, alphabet_map)`
Converts unrecognized terms into their spell-out phonetic equivalent using individual mapped letter pronunciations.
