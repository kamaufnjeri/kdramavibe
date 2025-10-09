import re
import ftfy

class DataCleaner:
    def __init__(self):
        self.ref_pattern = re.compile(r'\[\d+\]')  # remove numeric references like [1], [2]
        self.edge_pattern = re.compile(r'^[,–\[\]\s]+|[,–\[\]\s]+$')  # strip edge punctuation/whitespace
        self.space_pattern = re.compile(r'\s+')  # collapse multiple spaces

    def clean_text(self, text: str) -> str:
        """Clean a single text string."""
        if not text:
            return ''
        text = ftfy.fix_text(text)
        text = self.ref_pattern.sub('', text)
        text = text.replace(', ', ' ')
        text = self.edge_pattern.sub('', text)
        text = self.space_pattern.sub(' ', text)
        return text.strip()

    def clean_list(self, items: list) -> list:
        """Clean a list of items, removing single/two character strings, numbers, commas, or slashes."""
        cleaned = []
        for item in items:
            item = str(item).strip()
            item = ftfy.fix_text(item)
            item = self.ref_pattern.sub('', item)
            item = item.replace(', ', '')  # remove stray ', ' in list item
            item = self.edge_pattern.sub('', item)
            item = self.space_pattern.sub(' ', item)
            # Remove single or two characters, numbers, commas, or slashes
            if len(item) > 2 and not item.isdigit() and item not in [',', '/', ', ']:
                cleaned.append(item)
        return cleaned

    def clean_dict(self, data: dict) -> dict:
        """Clean all text and list fields in a dictionary."""
        cleaned_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                cleaned_data[key] = self.clean_text(value)
            elif isinstance(value, list):
                cleaned_data[key] = self.clean_list(value)
            else:
                cleaned_data[key] = value
        return cleaned_data

raw_data = {
    'title': 'The Frog [1]',
    'genres': ['\n', 'Mystery', '\n', 'Crime thriller', '\n', '/', ',', 'K'],
    'plot': 'A man moves to a forest town. [2][3]',
    'directors': ['Mo Wan-il', '\xa0[', 'ko', ']']
}

cleaner = DataCleaner()
cleaned_data = cleaner.clean_dict(raw_data)

print(cleaned_data)