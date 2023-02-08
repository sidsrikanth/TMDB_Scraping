# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from scrapy.http import Request

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    start_urls = ['https://www.themoviedb.org/tv/60059-better-call-saul']

    cast_link_extractor = LinkExtractor(allow="https://www.themoviedb\.org/tv/60059-better-call-saul.+")

    actor_link_extractor = LinkExtractor(allow="https://www.themoviedb\.org/person.+",
        restrict_css = "ol.people.credits:not(.crew)")

    def parse(self, response):
        '''
        Navigates to the Cast & Crew page from specified movie/TV show page
        Parameters:
        - self
        - response: response to parse request
        Yields Request with callback to parse_full_credits()
        '''
        # extracts all links on page that matches specfied format
        links = self.cast_link_extractor.extract_links(response)
        target = links[1] # hard-coded link to Cast & Crew page
        yield Request(target.url, callback = self.parse_full_credits)

    def parse_full_credits(self, response):
        '''
        Navigates to each actor's page from the specified Cast & Crew page
        Parameters:
        - self
        - response: response to parse request
        Yields Request with callback to parse_actor_page()
        '''
        # extracts all actor links on page
        links = self.actor_link_extractor.extract_links(response)
        for link in links:
            # navigate to each actor's page
            yield Request(link.url, callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        '''
        Collects all movies/TV shows listed on the specified actor's page
        Parameters:
        - self
        - response: response to parse request
        Yields a dictionary of the form {"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name}.
        for each of the movies or TV shows the actor has worked on
        '''
        # extract name of actor
        name = response.css("div.title a::text").get()
        # extract list of all movies/TV shows actor has worked on
        works = response.css("table.credit_group a.tooltip")
        for work in works:
            yield {"actor": name,"movie_or_TV_name": work.css("a bdi::text").get()}
