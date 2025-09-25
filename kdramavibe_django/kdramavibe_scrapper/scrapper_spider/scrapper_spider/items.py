import scrapy

class KdramaItem(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()
    rating = scrapy.Field()
    total_rating = scrapy.Field()
    description = scrapy.Field()
    writers = scrapy.Field()
    directors = scrapy.Field()
    dramabeans_url = scrapy.Field()
    wikipedia_url = scrapy.Field()
    alternate_titles = scrapy.Field()
    genre = scrapy.Field()
    episodes = scrapy.Field()
    network = scrapy.Field()
    release_date =scrapy.Field()
    running_time = scrapy.Field()
    image_url = scrapy.Field()
    kactors = scrapy.Field()

   
class KactorItem(scrapy.Item):
    name = scrapy.Field()
    alternate_names = scrapy.Field()
    description = scrapy.Field()
    bio = scrapy.Field()
    birthday =scrapy.Field()
    birthplace = scrapy.Field()
    age = scrapy.Field()
    education = scrapy.Field()       
    occupations = scrapy.Field()      
    years_active = scrapy.Field()  
    agent = scrapy.Field()
    height = scrapy.Field()  
    partner_or_spouse = scrapy.Field()
    dramabeans_url = scrapy.Field()
    wikipedia_url = scrapy.Field()
    image_url = scrapy.Field()
    kdramas = scrapy.Field()

   