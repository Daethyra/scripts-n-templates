import json
import re
import argparse

class RegexGenerator:
    def __init__(self, config=None):
        self.substitutions = config.get("substitutions", {}) if config else self.generate_substitutions()

    def generate_substitutions(self):
        """
        Generate a dictionary of common substitutions for vowels and consonants.
        Returns:
            dict: A dictionary mapping each character to its possible substitutions.
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

    def generate_regex_pattern(self, words):
        """
        Generate a regex pattern based on the input words and substitutions.
        Args:
            words (list): List of words to generate regex for.
        Returns:
            str: The generated regex pattern.
        """
        regex_parts = []
        for word in words:
            pattern = ''.join([self.substitutions.get(char, char) for char in word])
            regex_parts.append(f"^{pattern}$")
        return '|'.join(regex_parts)

    def save_to_json(self, regex_pattern):
        """
        Save the generated regex pattern to a JSON file.
        Args:
            regex_pattern (str): The regex pattern to save.
        """
        with open('regex_pattern.json', 'w') as f:
            json.dump({'regex_pattern': regex_pattern}, f)

    def load_from_file(self, file_path):
        """
        Load words or configuration from a file.
        Args:
            file_path (str): The path to the file to load from.
        Returns:
            dict: A dictionary containing words and optional substitutions.
        """
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading from file: {e}")
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate regex patterns.')
    parser.add_argument('-h', '--help', action='help', help='Show this help message and exit.')
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
