from rapidfuzz import fuzz
from kdramavibe_scrapper.models import Kdrama, Kactor


class CompareKdramas:
    """
    Compare two Kdrama model instances by title similarity and year match.
    """

    def __init__(self, dramabeans_kdrama, wiki_kdrama, threshold=80):
        """
        Initialize the comparison instance.

        :param dramabeans_kdrama: Dramabeans Kdrama model instance
        :param wiki_kdrama: Wikipedia Kdrama model instance
        :param threshold: minimum fuzzy score to consider a match
        """
        self.dramabeans_kdrama = dramabeans_kdrama
        self.wiki_kdrama = wiki_kdrama
        self.threshold = threshold

    def _get_alternates(self, instance):
        """
        Return a clean list of lowercase alternate titles.

        :param instance: Kdrama instance
        :return: list of alternate titles
        """
        if not instance.alternate_titles:
            return []
        # Handle comma-separated alternates
        return [t.strip().lower() for t in instance.alternate_titles]

    def _compare_titles(self):
        """
        Compare titles (and alternates) using fuzzy logic.

        :return: highest similarity score
        """
        scores = []

        title_a = self.dramabeans_kdrama.title.lower().strip()
        title_b = self.wiki_kdrama.title.lower().strip()

        # Direct title comparison
        scores.append(fuzz.ratio(title_a, title_b))

        # Compare against alternates from Wiki
        for alt in self._get_alternates(self.wiki_kdrama):
            scores.append(fuzz.ratio(title_a, alt))

        return max(scores) if scores else 0

    def _compare_years(self):
        """
        Check if Dramabeans year fits within the Wiki's start–end range or exact match.

        :return: True if years match, False otherwise
        """
        if not self.dramabeans_kdrama.year or not self.wiki_kdrama.start_year:
            return False

        # Check if year is within start–end range
        if self.wiki_kdrama.end_year:
            return self.wiki_kdrama.start_year <= self.dramabeans_kdrama.year <= self.wiki_kdrama.end_year
        # Exact match if only start year exists
        return self.dramabeans_kdrama.year == self.wiki_kdrama.start_year

    def is_match(self):
        """
        Determine if the Kdramas are a match based on title and year.

        :return: True if match, False otherwise
        """
        score = self._compare_titles()
        return score >= self.threshold and self._compare_years()

    def match_details(self):
        """
        Return a dictionary summarizing match details.

        :return: dict with comparison info
        """
        return {
            "dramabeans_title": self.dramabeans_kdrama.title,
            "dramabeans_id": self.dramabeans_kdrama.id,
            "wiki_id": self.wiki_kdrama.id,
            "wiki_title": self.wiki_kdrama.title,
            "alternate_titles": self.wiki_kdrama.alternate_titles,
            "start_year": self.wiki_kdrama.start_year,
            "end_year": self.wiki_kdrama.end_year,
            "dramabeans_year": self.dramabeans_kdrama.year,
            "best_score": self._compare_titles(),
            "years_match": self._compare_years(),
            "is_match": self.is_match(),
        }


class CompareKactors:
    """
    Compare two Kactor model instances by name similarity and birthday match.
    """

    def __init__(self, dramabeans_kactor, wiki_kactor, threshold=50):
        """
        Initialize the comparison instance.

        :param dramabeans_kactor: Dramabeans Kactor model instance
        :param wiki_kactor: Wikipedia Kactor model instance
        :param threshold: minimum fuzzy score to consider a match
        """
        self.dramabeans_kactor = dramabeans_kactor
        self.wiki_kactor = wiki_kactor
        self.threshold = threshold

    def _normalize_name(self, name: str) -> str:
        """
        Normalize a name for comparison by removing spaces, hyphens, underscores, dots, and dashes.

        :param name: original name
        :return: normalized lowercase name
        """
        import re

        if not name:
            return ""

        # Remove spaces, hyphens, underscores, dots, and all Unicode dash variants
        cleaned = re.sub(r"[\s\-\u2010-\u2015._]", "", name)
        return cleaned.lower().strip()

    def _get_alternates(self, instance):
        """
        Return a clean list of lowercase alternate names.

        :param instance: Kactor instance
        :return: list of normalized alternate names
        """
        if not instance.alternate_names:
            return []
        # Normalize each alternate name
        return [self._normalize_name(n) for n in instance.alternate_names]

    def _compare_names(self):
        """
        Compare actor names (and alternates) using fuzzy logic.

        :return: highest similarity score
        """
        scores = []

        name_a = self._normalize_name(self.dramabeans_kactor.name)
        name_b = self._normalize_name(self.wiki_kactor.name)

        # Direct name comparison
        scores.append(fuzz.ratio(name_a, name_b))

        # Compare against alternates from Wiki
        for alt in self._get_alternates(self.wiki_kactor):
            scores.append(fuzz.ratio(name_a, alt))

        return max(scores) if scores else 0

    def _compare_birthday(self):
        """
        Check if birthdays match exactly.

        :return: True if birthdays match, False otherwise
        """
        if not self.dramabeans_kactor.birthday or not self.wiki_kactor.birthday:
            return False

        return self.dramabeans_kactor.birthday == self.wiki_kactor.birthday

    def is_match(self):
        """
        Determine if the Kactors are a match based on name similarity and birthday.

        :return: True if match, False otherwise
        """
        score = self._compare_names()
        return score >= self.threshold and self._compare_birthday()

    def match_details(self):
        """
        Return a dictionary summarizing match details.

        :return: dict with comparison info
        """
        return {
            "dramabeans_name": self.dramabeans_kactor.name,
            "dramabeans_id": self.dramabeans_kactor.id,
            "wiki_id": self.wiki_kactor.id,
            "wiki_birthday": self.wiki_kactor.birthday,
            "dramabeans_birthday": self.dramabeans_kactor.birthday,
            "wiki_name": self.wiki_kactor.name,
            "alternate_names": self.wiki_kactor.alternate_names,
            "wiki_image_url": self.wiki_kactor.image_url,
            "dramabeans_image_url": self.dramabeans_kactor.image_url,
            "best_score": self._compare_names(),
            "birthday_match": self._compare_birthday(),
            "is_match": self.is_match(),
        }
