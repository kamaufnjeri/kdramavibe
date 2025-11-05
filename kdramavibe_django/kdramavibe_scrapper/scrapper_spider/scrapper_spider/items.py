import scrapy


class DramaBeansKdramaItem(scrapy.Item):
    """
    Scrapy item for storing drama information from DramaBeans.
    """
    title = scrapy.Field()  # Title of the drama
    year = scrapy.Field()  # Release year
    rating = scrapy.Field()  # Drama rating
    no_of_votes = scrapy.Field()  # Number of votes for the rating
    dramabeans_url = scrapy.Field()  # URL of the drama page on DramaBeans


class DramaBeansKactorItem(scrapy.Item):
    """
    Scrapy item for storing actor/actress information from DramaBeans.
    """
    name = scrapy.Field()  # Name of the actor
    image_url = scrapy.Field()  # Profile image URL
    birthplace = scrapy.Field()  # Birthplace of the actor
    birthday = scrapy.Field()  # Birth date
    no_of_votes = scrapy.Field()  # Number of votes for popularity
    dramabeans_url = scrapy.Field()  # URL of the actor page on DramaBeans


class KdramaItem(scrapy.Item):
    """
    Scrapy item for storing drama information from Wikipedia.
    """
    title = scrapy.Field()  # Title of the drama
    start_year = scrapy.Field()  # Start year of airing
    end_year = scrapy.Field()  # End year of airing (or PRESENT)
    plot = scrapy.Field()  # Plot summary
    languages = scrapy.Field()  # Original languages
    country = scrapy.Field()  # Country of origin
    writers = scrapy.Field()  # List of writers
    directors = scrapy.Field()  # List of directors
    wikipedia_url = scrapy.Field()  # Wikipedia page URL
    alternate_titles = scrapy.Field()  # List of alternate titles
    genres = scrapy.Field()  # List of genres
    episodes = scrapy.Field()  # Number of episodes
    seasons = scrapy.Field()  # Number of seasons
    networks = scrapy.Field()  # Networks where aired
    running_time = scrapy.Field()  # Running time per episode
    image_url = scrapy.Field()  # Drama poster/image URL
    kactors = scrapy.Field()  # List of actors/characters


class KactorItem(scrapy.Item):
    """
    Scrapy item for storing actor/actress information from Wikipedia.
    """
    name = scrapy.Field()  # Actor's name
    gender = scrapy.Field()  # Gender of the actor
    description = scrapy.Field()  # Biography/description
    birthday = scrapy.Field()  # Birth date
    birthplace = scrapy.Field()  # Birthplace
    age = scrapy.Field()  # Calculated age
    occupations = scrapy.Field()  # List of occupations
    years_active = scrapy.Field()  # Active years
    agents = scrapy.Field()  # Agents/representation
    height = scrapy.Field()  # Height of the actor
    partner_or_spouse = scrapy.Field()  # Partner or spouse info
    wikipedia_url = scrapy.Field()  # Wikipedia page URL
    image_url = scrapy.Field()  # Profile image URL
    alternate_names = scrapy.Field()  # List of alternate names/stage names
    children = scrapy.Field()  # Children info or names
