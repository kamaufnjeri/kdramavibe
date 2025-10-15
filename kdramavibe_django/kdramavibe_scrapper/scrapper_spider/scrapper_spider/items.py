import scrapy

class KdramaItem(scrapy.Item):
    title = scrapy.Field()
    start_year = scrapy.Field()
    end_year = scrapy.Field()
    rating = scrapy.Field()
    total_rating = scrapy.Field()
    plot = scrapy.Field()
    languages = scrapy.Field()
    country = scrapy.Field()
    writers = scrapy.Field()
    directors = scrapy.Field()
    wikipedia_url = scrapy.Field()
    alternate_titles = scrapy.Field()
    genres = scrapy.Field()
    episodes = scrapy.Field()
    seasons = scrapy.Field()
    networks = scrapy.Field()
    running_time = scrapy.Field()
    image_url = scrapy.Field()
    kactors = scrapy.Field()

   
class KactorItem(scrapy.Item):
    name = scrapy.Field()
    gender = scrapy.Field()
    description = scrapy.Field()
    birthday =scrapy.Field()
    birthplace = scrapy.Field()
    age = scrapy.Field()
    occupations = scrapy.Field()      
    years_active = scrapy.Field()  
    agent = scrapy.Field()
    height = scrapy.Field()  
    partner_or_spouse = scrapy.Field()
    wikipedia_url = scrapy.Field()
    image_url = scrapy.Field()
    alternate_names = scrapy.Field()
    children = scrapy.Field()

   