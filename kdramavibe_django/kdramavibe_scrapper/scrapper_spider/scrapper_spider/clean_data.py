import re
import ftfy

class DataCleaner:
    def __init__(self):
        self.ref_pattern = re.compile(r'\[\d+\]')  # remove [1], [2]
        self.edge_pattern = re.compile(r'^[,–\[\]\s]+|[,\[\]\s]+$')  # trim commas/brackets
        self.space_pattern = re.compile(r'\s+')  # collapse multiple spaces

    def clean_text(self, text: str) -> str:
        if not text:
            return ''
        text = ftfy.fix_text(str(text))
        text = self.ref_pattern.sub('', text)
        text = self.edge_pattern.sub('', text)
        text = self.space_pattern.sub(' ', text)
        return text.strip()

    def clean_list(self, items: list) -> list:
        cleaned = []
        for item in items:
            if isinstance(item, dict):
                cleaned_dict = self.clean_dict(item)
                if any(v for v in cleaned_dict.values() if v not in [None, '', []]):
                    cleaned.append(cleaned_dict)
            elif isinstance(item, str):
                text = self.clean_text(item)
                # Skip junk like numbers or empty text
                if len(text) > 2 and not text.isdigit():
                    cleaned.append(text)
        return cleaned

    def clean_dict(self, data: dict) -> dict:
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


cleaner = DataCleaner()