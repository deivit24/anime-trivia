import os
from v1.anime_scraper import html_table_to_csv, html_grid_to_csv
from v2.anime_scrapper import AnimeScraperV2

SOURCE_FILES = [
    # Anime Scrapping Source V1. This is what I originally used as my source to scrape data but
    # issue was that their image hosting site would not let load images to HTML
    {
        "url": "https://anidb.net/anime/?h=1&noalias=1&orderby.rank_popularity=0.1&page={}",
        "pages": 27,  # 27 it is 500 animes per page
        "filename": "anime.csv",
        "type": "Table",
    },
    {
        "url": "https://anidb.net/character/?h=1&noalias=1&orderby.name=0.1&view=list&page={}",
        "pages": 253,  # 253 is is 500 characters per page
        "filename": "character.csv",
        "type": "Table",
    },
    {
        "url": "https://anidb.net/character/?noalias=1&orderby.name=0.1&page={}&view=grid",
        "pages": 253,
        "filename": "character_desc.csv",
        "type": "Grid",
    },
    {
        "api": "https://api.jikan.moe/v4/top/anime?page={}",
        "filename": "top_anime.csv",
        "path": os.path.dirname(os.path.realpath(__file__)),
        "attrib_type": "anime",
    },
    {
        "api": "https://api.jikan.moe/v4/top/characters?page={}",
        "filename": "top_characters.csv",
        "path": os.path.dirname(os.path.realpath(__file__)),
        "attrib_type": "character",
    },
]

for source in SOURCE_FILES:
    url = source.get("url")
    pages = source.get("pages")
    filename = source.get("filename")
    t = source.get("type")
    if t == "Grid":
        html_grid_to_csv(url, filename, pages)
    elif t == "Table":
        html_table_to_csv(url, filename, pages)
    # api = source.get("api")
    # path = source.get("path")
    # filename = source.get("filename")
    # attrib_type = source.get("attrib_type")
    # anime_scraper = AnimeScraperV2(api, filename, path, attrib_type)
    # anime_scraper.scrape()
