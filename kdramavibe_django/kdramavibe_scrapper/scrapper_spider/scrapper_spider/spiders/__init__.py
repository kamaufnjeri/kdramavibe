# This package contains all the spiders for your Scrapy project.
# Each spider is responsible for crawling and extracting data from specific sources.
# Refer to the Scrapy documentation for guidance on creating and managing spiders.

# Import the Kdramas spider to crawl K-drama related data
from .kdramas import KdramasSpider

# Import the Kactors spider to crawl K-actor related data
from .kactors import KactorsSpider

# Import Wikipedia spiders for K-drama and K-actor data
from .wikipedia_kdrama import WikipediaKdramasSpider
from .wikipedia_kactor import WikipediaKactorsSpider

# Import spiders for crawling single K-drama or K-actor pages
from .single_kdrama import SingleKdramaSpider
from .single_kactor import SingleKactorSpider
