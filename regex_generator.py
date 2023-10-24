"""
EXAMPLE CONFIG FILE:
{
  "words": ["damon", "daemon", "daethyra"],
  "substitutions": {
    "a": "[aA@4]",
    "e": "[eE3]",
    "o": "[oO0]",
    "d": "[dD]",
    "m": "[mM]",
    "n": "[nN]",
    "c": "[cC]",
    "r": "[rR]",
    "i": "[iI]"
  }
}
"""

import json
import re
import argparse
import datetime
from typing import List, Optional, Dict, Union

class RegexGenerator:
    def __init__(self, config: Optional[Dict[str, Union[str, List[str]]]] = None) -> None:
        """
        Initialize RegexGenerator with substitutions.
        """
        self.substitutions = config.get("substitutions", {}) if config else self.generate_substitutions()

    def generate_substitutions(self) -> Dict[str, str]:
        """
        Generate common substitutions.
        Returns:
            Dictionary of character substitutions.
        """
        return {
            'a': '[aA@4]',
            'e': '[eE3]',
            'o': '[oO0]',
            'd': '[dD]',
            'm': '[mM]',
            'n': '[nN]',
            'c': '[cC]',
            'r': '[rR]',
            'i': '[iI]'
        }

    def generate_regex_pattern(self, words: List[str]) -> str:
        """
        Generate a regex pattern.
        Args:
            words: List of words to generate regex for.
        Returns:
            Generated regex pattern.
        """
        regex_parts = [f"^{''.join([self.substitutions.get(char, char) for char in word])}$" for word in words]
        return '|'.join(regex_parts)

    def save_to_json(self, regex_pattern: str) -> None:
        """
        Save the generated regex pattern to a JSON file, appending to existing patterns.
        Args:
            regex_pattern: The regex pattern to save.
        """
        try:
            try:
                # Load existing data from the JSON file
                with open('regex_pattern.json', 'r') as f:
                    existing_data = json.load(f)
                patterns = existing_data.get('regex_patterns', [])
            except FileNotFoundError:
                patterns = []
            
            # Append the new pattern
            patterns.append(regex_pattern)

            # Ask the user for saving preferences
            while True:
                try:
                    choice = input("Do you want to save the pattern? (y/n): ").strip().lower()
                    if choice == 'y':
                        break
                    elif choice == 'n':
                        return
                except KeyboardInterrupt:
                    continue
            
            while True:
                try:
                    choice = input("Append to latest file or create a new file with a timestamp? (a/n): ").strip().lower()
                    if choice == 'a':
                        file_name = 'regex_pattern.json'
                        break
                    elif choice == 'n':
                        file_name = f"regex_pattern_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        break
                except KeyboardInterrupt:
                    continue

            # Save the updated data back to the chosen JSON file
            with open(file_name, 'w') as f:
                json.dump({'regex_patterns': patterns}, f)
        except Exception as e:
            print(f"An error occurred: {e}")

    def load_from_file(self, file_path: str) -> Optional[Dict[str, Union[str, List[str]]]]:
        """
        Load words or configuration from a file.
        Args:
            file_path: File path to load from.
        Returns:
            Dictionary containing words and optional substitutions, or None if loading fails.
        """
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading from file: {e}")
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate regex patterns.')
    parser.add_argument('-r', '--read', type=str, help='Load words or configuration from a file.')

    args = parser.parse_args()

    config = None
    if args.read:
        config = RegexGenerator().load_from_file(args.read)

    generator = RegexGenerator(config)

    if not config:
        words_input = input("Enter the words you want to generate regex for, separated by commas: ").split(',')
    else:
        words_input = config.get('words', [])

    regex_pattern = generator.generate_regex_pattern(words_input)
    print(f"Generated regex pattern: {regex_pattern}")
    generator.save_to_json(regex_pattern)