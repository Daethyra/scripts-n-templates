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
            # Load existing data from the JSON file
            with open('regex_pattern.json', 'r') as f:
                existing_data = json.load(f)
            patterns = existing_data.get('regex_patterns', [])
        except FileNotFoundError:
            patterns = []
            
        # Append the new pattern
        patterns.append(regex_pattern)

        # Save the updated data back to the JSON file
        with open('regex_pattern.json', 'w') as f:
            json.dump({'regex_patterns': patterns}, f)

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