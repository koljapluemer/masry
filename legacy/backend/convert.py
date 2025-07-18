import os
import json
import shutil
from pathlib import Path

# Configuration: Set the absolute path where data should be outputted
OUTPUT_DIR = "/home/brokkoli/GITHUB/linguanodon/public/data"  # Change this to your desired output path

def clear_public_folder():
    """Clear all folders and files in output directory"""
    output_path = Path(OUTPUT_DIR)
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(exist_ok=True, parents=True)
    print(f"Cleared {OUTPUT_DIR}/ folder")


def copy_data_files():
    """Copy JSON files from data/ to output directory organized by language code"""
    data_dir = Path("data")
    output_path = Path(OUTPUT_DIR)
    
    if not data_dir.exists():
        raise FileNotFoundError("data/ folder not found")
    
    # Check that data/ contains only JSON files (flat structure)
    json_files = list(data_dir.glob("*.json"))
    all_files = list(data_dir.iterdir())
    
    if len(json_files) != len(all_files):
        non_json_files = [f for f in all_files if f.suffix.lower() != '.json']
        raise ValueError(f"data/ folder must contain only JSON files. Found non-JSON files: {non_json_files}")
    
    if not json_files:
        raise ValueError("No JSON files found in data/ folder")
    
    language_codes = set()
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Get language code from top-level "language" property
            language_code = data.get("language")
            if not language_code:
                raise ValueError(f"JSON file {json_file.name} missing 'language' property")
            
            language_codes.add(language_code)
            
            # Create language subfolder
            lang_dir = output_path / language_code
            lang_dir.mkdir(exist_ok=True)
            
            # Copy JSON file to language subfolder (compressed)
            dst_path = lang_dir / json_file.name
            with open(dst_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
            
            print(f"Copied {json_file.name} to {language_code}/")
            
        except Exception as e:
            print(f"Error processing {json_file.name}: {e}")
            raise
    
    return language_codes

def generate_language_indexes(language_codes):
    """Generate index files for each language subfolder"""
    output_path = Path(OUTPUT_DIR)
    
    for lang_code in language_codes:
        lang_dir = output_path / lang_code
        if not lang_dir.exists():
            continue
        
        # Find all JSON files in this language folder
        json_files = list(lang_dir.glob("*.json"))
        sets_data = {}
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Get the "name" property from the JSON
                name = data.get("name", f"Set {json_file.stem}")
                sets_data[json_file.name] = name
                
            except Exception as e:
                print(f"Error reading JSON file {json_file}: {e}")
                sets_data[json_file.name] = f"Set {json_file.stem}"
        
        # Write index file for this language
        index_path = lang_dir / "index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(sets_data, f, ensure_ascii=False, separators=(',', ':'))
        
        print(f"Generated index for {lang_code}/ with {len(sets_data)} entries")

def generate_languages_json(language_codes):
    """Generate root-level languages.json with available language codes"""
    output_path = Path(OUTPUT_DIR)
    languages_path = output_path / "languages.json"
    
    # Convert set to sorted list for consistent output
    languages_list = sorted(list(language_codes))
    
    with open(languages_path, 'w', encoding='utf-8') as f:
        json.dump(languages_list, f, ensure_ascii=False, separators=(',', ':'))
    
    print(f"Generated languages.json with {len(languages_list)} language codes: {languages_list}")

def main():
    """Main conversion process"""
    print("Starting conversion process...")
    
    # Step 1: Clear public/ folder
    clear_public_folder()
    
    # Step 3: Copy data/ files organized by language
    try:
        language_codes = copy_data_files()
    except Exception as e:
        print(f"Error during file processing: {e}")
        return
    
    # Step 4: Generate language-specific indexes
    generate_language_indexes(language_codes)
    
    # Step 5: Generate root-level languages.json
    generate_languages_json(language_codes)
    
    print("Conversion complete!")

if __name__ == "__main__":
    main()
