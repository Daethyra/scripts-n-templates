import concurrent.futures
import argparse
import os
from bs4 import BeautifulSoup

class HTMLFontStyleConverter:
    """
    A class to convert HTML font styles including color, highlight, and additional CSS styles.

    Attributes:
    font_color (str): Default font color in CSS format, defaults to black.
    highlight_color (str): Default background (highlight) color in CSS format, optional.
    font_style (str): Default additional font styles in CSS format, optional.

    Methods:
    remove_background_color_from_style(style): Static method to remove background color from CSS style.
    parse_style(style_str): Static method to parse CSS style string into a dictionary.
    serialize_style(style_dict): Static method to serialize dictionary of CSS styles back into a string.
    convert_HTML(html_content): Convert HTML content based on instance's font style attributes.
    process_html_file(file_path, output_file_path): Process a single HTML file.
    batch_process_html_files(file_paths, output_dir): Process multiple HTML files in parallel.
    """
    def __init__(self, font_color="#000000", highlight_color=None, font_style=None):
        self.font_color = font_color
        self.highlight_color = highlight_color
        self.font_style = font_style

    @staticmethod
    def remove_background_color_from_style(style):
        """
        Remove background color properties from a CSS style string.

        Parameters:
        style (str): A CSS style string.

        Returns:
        str: A modified CSS style string without background color properties.
        """
        properties = style.split(';')
        properties = [prop for prop in properties if "background-color" not in prop]
        return '; '.join(properties)

    @staticmethod
    def parse_style(style_str):
        """
        Parse a CSS style string into a dictionary.

        Parameters:
        style_str (str): A CSS style string.

        Returns:
        dict: A dictionary representation of the style.
        """
        styles = [s.strip() for s in style_str.split(';') if s.strip()]
        return dict(style.split(':') for style in styles)

    @staticmethod
    def serialize_style(style_dict):
        """
        Serialize a dictionary of CSS styles back into a string.

        Parameters:
        style_dict (dict): A dictionary of CSS styles.

        Returns:
        str: A CSS style string.
        """
        return '; '.join([f'{k}: {v}' for k, v in style_dict.items()])

    def convert_HTML(self, html_content):
        """
        Modify the HTML content to apply specified font color, highlight color, and font style.

        Parameters:
        html_content (str): A string containing HTML content.

        Returns:
        str: Modified HTML content with specified styling.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        for tag in soup.find_all(True):
            style_dict = self.parse_style(tag.get('style', ''))

            # Set font color
            style_dict['color'] = self.font_color

            # Set or remove highlight color
            if self.highlight_color is not None:
                style_dict['background-color'] = self.highlight_color
            elif 'background-color' in style_dict:
                del style_dict['background-color']

            # Apply additional font styles
            if self.font_style:
                additional_styles = self.parse_style(self.font_style)
                style_dict.update(additional_styles)

            tag['style'] = self.serialize_style(style_dict)

        return str(soup)

    def process_html_file(self, file_path, output_file_path):
        """
        Process an HTML file to apply specified font style, color, and background color.

        Parameters:
        file_path (str): Path to the input HTML file.
        output_file_path (str): Path to save the modified HTML file.
        """
        try:
            with open(file_path, "r") as file:
                html_content = file.read()
            modified_html = self.convert_HTML(html_content)
            with open(output_file_path, "w") as file:
                file.write(modified_html)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    def batch_process_html_files(self, file_paths, output_dir):
        """
        Process multiple HTML files in parallel.

        Parameters:
        file_paths (list of str): List of paths to input HTML files.
        output_dir (str): Directory to save modified HTML files.
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for file_path in file_paths:
                output_file_path = f"{output_dir}/{os.path.basename(file_path)}"
                futures.append(executor.submit(self.process_html_file, file_path, output_file_path))
            concurrent.futures.wait(futures)

def convert_HTML_font_style(file_paths, output_dir, font_color="#000000", highlight_color=None, font_style=None):
    """
    Process HTML files with specified font styles and colors using an instance of HTMLFontStyleConverter.

    Parameters:
    file_paths (list of str): Paths to the input HTML files.
    output_dir (str): Directory to save modified HTML files.
    font_color (str): Font color in CSS format.
    highlight_color (str, optional): Background (highlight) color in CSS format.
    font_style (str, optional): Additional font styles in CSS format.
    """
    converter = HTMLFontStyleConverter(font_color, highlight_color, font_style)
    converter.batch_process_html_files(file_paths, output_dir)

def main():
    parser = argparse.ArgumentParser(description="Process HTML files with specified font styles and colors.")
    parser.add_argument("file_paths", nargs="+", help="Paths to the input HTML files")
    parser.add_argument("-o", "--output_dir", default=".", help="Directory to save modified HTML files")
    parser.add_argument("--font_color", default="#000000", help="Font color in CSS format, e.g., '#FF5733'. Defaults to black.")
    parser.add_argument("--highlight_color", default=None, help="Background (highlight) color in CSS format, e.g., '#FFFF00'. If not set, highlights are removed.")
    parser.add_argument("--font_style", default=None, help="Additional CSS font styles as a string, e.g., 'font-size: 12px; font-weight: bold;'.")

    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    convert_HTML_font_style(args.file_paths, args.output_dir, args.font_color, args.highlight_color, args.font_style)

if __name__ == "__main__":
    main()
