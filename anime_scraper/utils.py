import typing
import json
from requests import Response, request, Session
from bs4 import BeautifulSoup
from decouple import config

IMAGE = "Image"
TITLE = "Title"
NO = "No"
NAME = "Name"
AUTH_URL = "https://anidb.net/perl-bin/animedb.pl"
USERNAME = config("USERNAME")
PASSWORD = config("PASSWORD")
ANIME_ATTRIBUTES = [
    "mal_id",
    "url",
    "images_jpg_image_url",
    "images_jpg_small_image_url",
    "images_jpg_large_image_url",
    "images_webp_image_url",
    "images_webp_small_image_url",
    "images_webp_large_image_url",
    "trailer_youtube_id",
    "trailer_url",
    "trailer_embed_url",
    "trailer_images_image_url",
    "trailer_images_small_image_url",
    "trailer_images_medium_image_url",
    "trailer_images_large_image_url",
    "trailer_images_maximum_image_url",
    "approved",
    "titles_titles_1_type",
    "titles_titles_1_title",
    "titles_titles_2_type",
    "titles_titles_2_title",
    "titles_titles_3_type",
    "titles_titles_3_title",
    "titles_titles_4_type",
    "titles_titles_4_title",
    "title",
    "title_english",
    "title_japanese",
    "title_synonyms_title_synonyms_1",
    "type",
    "source",
    "episodes",
    "status",
    "airing",
    "aired_from",
    "aired_to",
    "aired_prop_from_day",
    "aired_prop_from_month",
    "aired_prop_from_year",
    "aired_prop_to_day",
    "aired_prop_to_month",
    "aired_prop_to_year",
    "aired_string",
    "duration",
    "rating",
    "score",
    "scored_by",
    "rank",
    "popularity",
    "members",
    "favorites",
    "synopsis",
    "background",
    "season",
    "year",
    "broadcast_day",
    "broadcast_time",
    "broadcast_timezone",
    "broadcast_string",
    "producers_producers_1_mal_id",
    "producers_producers_1_type",
    "producers_producers_1_name",
    "producers_producers_1_url",
    "producers_producers_2_mal_id",
    "producers_producers_2_type",
    "producers_producers_2_name",
    "producers_producers_2_url",
    "producers_producers_3_mal_id",
    "producers_producers_3_type",
    "producers_producers_3_name",
    "producers_producers_3_url",
    "producers_producers_4_mal_id",
    "producers_producers_4_type",
    "producers_producers_4_name",
    "producers_producers_4_url",
    "producers_producers_5_mal_id",
    "producers_producers_5_type",
    "producers_producers_5_name",
    "producers_producers_5_url",
    "producers_producers_6_mal_id",
    "producers_producers_6_type",
    "producers_producers_6_name",
    "producers_producers_6_url",
    "studios_studios_1_mal_id",
    "studios_studios_1_type",
    "studios_studios_1_name",
    "studios_studios_1_url",
    "genres_genres_1_mal_id",
    "genres_genres_1_type",
    "genres_genres_1_name",
    "genres_genres_1_url",
    "genres_genres_2_mal_id",
    "genres_genres_2_type",
    "genres_genres_2_name",
    "genres_genres_2_url",
    "genres_genres_3_mal_id",
    "genres_genres_3_type",
    "genres_genres_3_name",
    "genres_genres_3_url",
    "demographics_demographics_1_mal_id",
    "demographics_demographics_1_type",
    "demographics_demographics_1_name",
    "demographics_demographics_1_url",
]
CHARACTER_ATTRIBUTES = [
    "mal_id",
    "url",
    "images_jpg_image_url",
    "images_webp_image_url",
    "images_webp_small_image_url",
    "name",
    "name_kanji",
    "nicknames_nicknames_1",
    "nicknames_nicknames_2",
    "nicknames_nicknames_3",
    "nicknames_nicknames_4",
    "nicknames_nicknames_5",
    "nicknames_nicknames_6",
    "favorites",
    "about",
]


def validate_response(result: Response) -> typing.Union[str, dict]:
    try:
        body = json.dumps(result.text)
    except Exception:
        body = {}

    if type(body) is dict and body.get("code", None) is not None:
        raise Exception(body.get("description"))
    elif result.status_code >= 400:
        raise Exception(" ".join([str(result.status_code), result.reason]))
    elif len(result.text) == 0:
        return "OK"
    else:
        return result.text


def fetch_html_from_url(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    result = request("get", url, headers=headers)
    html = validate_response(result)
    soup = BeautifulSoup(html, features="html.parser")
    return soup


def fetch_session_from_url(url: str, session: Session):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    result = session.get(url, headers=headers)
    html = validate_response(result)
    soup = BeautifulSoup(html, features="html.parser")
    return soup


def auth_login():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9,es-US;q=0.8,es;q=0.7",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
    }

    data = {
        "show": "main",
        "xuser": USERNAME,
        "xpass": PASSWORD,
        "xdoautologin": "on",
        "do.auth": "login",
    }
    session = Session()
    session.post(AUTH_URL, headers=headers, data=data)

    session.cookies

    return session
