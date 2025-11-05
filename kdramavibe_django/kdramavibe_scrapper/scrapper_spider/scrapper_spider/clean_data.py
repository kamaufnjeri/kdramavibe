import re
import ftfy


class DataCleaner:
    """
    A utility class to clean text, lists, and dictionaries by removing
    references, extra whitespace, unwanted characters, and fixing text encoding.
    """

    def __init__(self):
        # Pattern to remove citations like [1], [a], etc.
        self.ref_pattern = re.compile(r'\[(\d+|[a-z]+)\]', re.IGNORECASE)

        # Pattern to trim leading/trailing commas, dashes, brackets, and spaces
        self.edge_pattern = re.compile(r'^[,–\[\]\s]+|[,\[\]\s]+$')

        # Pattern to collapse multiple spaces into one
        self.space_pattern = re.compile(r'\s+')

    def clean_text(self, text: str) -> str:
        """
        Clean a single text string.

        Steps:
        - Fix text encoding using ftfy.
        - Remove reference markers like [1], [a].
        - Trim leading/trailing commas, brackets, and spaces.
        - Collapse multiple spaces into a single space.
        """
        if not text:
            return ''

        text = ftfy.fix_text(str(text))  # fix encoding issues
        text = self.ref_pattern.sub('', text)
        text = self.edge_pattern.sub('', text)
        text = self.space_pattern.sub(' ', text)
        return text.strip()

    def clean_list(self, items: list) -> list:
        """
        Clean a list of strings or dictionaries.

        For dictionaries, uses `clean_dict`.
        Filters out short strings or numeric junk.
        """
        cleaned = []

        for item in items:
            if isinstance(item, dict):
                cleaned_dict = self.clean_dict(item)
                # Only include dicts with meaningful values
                if any(v for v in cleaned_dict.values() if v not in [None, '', []]):
                    cleaned.append(cleaned_dict)
            elif isinstance(item, str):
                text = self.clean_text(item)
                # Skip junk like numbers or empty text
                if len(text) > 2 and not text.isdigit():
                    cleaned.append(text)

        return cleaned

    def clean_dict(self, data: dict) -> dict:
        """
        Recursively clean a dictionary.

        Applies `clean_text` to strings, `clean_list` to lists,
        and recursively cleans nested dictionaries.
        """
        cleaned_data = {}

        for key, value in data.items():
            if isinstance(value, str):
                cleaned_data[key] = self.clean_text(value)
            elif isinstance(value, list):
                cleaned_data[key] = self.clean_list(value)
            elif isinstance(value, dict):
                cleaned_data[key] = self.clean_dict(value)
            else:
                cleaned_data[key] = value

        return cleaned_data


# Create a single instance for convenience
cleaner = DataCleaner()
