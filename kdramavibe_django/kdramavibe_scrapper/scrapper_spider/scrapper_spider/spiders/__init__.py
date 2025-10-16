# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from .kdramas import KdramasSpider
from .kactors import KactorsSpider
from .wikipedia_kdrama import WikipediaKdramasSpider
from .wikipedia_kactor import WikipediaKactorsSpider
from .single_kdrama import SingleKdramaSpider
from .single_kactor import SingleKactorSpider