from requests import HTTPError, Response, request, Session
import json
import csv
import time
import os

from utils import ANIME_ATTRIBUTES, CHARACTER_ATTRIBUTES


class AnimeScraperV2:
    def __init__(self, api: str, filename: str, path: str, attrib_type: str):
        self.api = api
        self.filename = filename
        self.path = path
        self.attributes = (
            ANIME_ATTRIBUTES if attrib_type == "anime" else CHARACTER_ATTRIBUTES
        )

    def flatten_dict(self, d, parent_key="", sep="_", index_offset=1):
        """
        Flatten a nested dictionary and generate flattened keys.

        Parameters:
        - d (dict): The dictionary to flatten.
        - parent_key (str): The parent key for recursion.
        - sep (str): The separator to use between parent and child keys.
        - index_offset (int): The starting index for list elements.

        Returns:
        - dict: A flattened dictionary.
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k

            if isinstance(v, dict):
                items.extend(
                    self.flatten_dict(
                        v, new_key, sep=sep, index_offset=index_offset
                    ).items()
                )
            elif isinstance(v, list):
                for i, item in enumerate(v, start=index_offset):
                    items.extend(
                        self.flatten_dict(
                            {f"{k}_{i}": item},
                            new_key,
                            sep=sep,
                            index_offset=index_offset,
                        ).items()
                    )
            else:
                items.append((new_key, v))
        return dict(items)

    def get_data(self, url):
        """
        Fetch data from the API.

        Parameters:
        - url (str): The URL to fetch data from.

        Returns:
        - dict: The JSON response from the API.
        """

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        try:
            response = request("get", url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx status codes)

            # Assuming the response content is JSON, you can use response.json()
            result = response.json()
            return result
        except HTTPError as http_err:
            # Handle HTTP errors (e.g., 404 Not Found, 500 Internal Server Error)
            print(f"HTTP error occurred: {http_err}")
            raise  # Re-raise the exception after handling
        except Exception as err:
            # Handle other types of exceptions
            print(f"An error occurred: {err}")
            raise  # Re-raise the exception after handling

    def dict_csv_list(self, data):
        """
        Convert a dictionary to a CSV list based on ANIME_ATTRIBUTES.

        Parameters:
        - data (dict): The dictionary containing anime data.

        Returns:
        - list: A list representing the CSV row.
        """

        flattened_dict = self.flatten_dict(data)
        csv_row = [flattened_dict.get(key, None) for key in self.attributes]
        return csv_row

    def scrape(self):
        """
        Fetch anime data from the API, convert it to a CSV list, and save it to a CSV file.
        """

        csv_list = [self.attributes]
        page = 1
        base_url = self.api.format(page)
        result = self.get_data(base_url)

        last_page = result["pagination"]["last_visible_page"]
        print("Got results for page 1")

        for data in result["data"]:
            csv_list.append(self.dict_csv_list(data))

        while page < last_page:
            page += 1
            base_url = self.api.format(page)

            result = self.get_data(base_url)
            print(f"Got results for page {page} out of {last_page}")

            for data in result["data"]:
                csv_list.append(self.dict_csv_list(data))

            if page % 5 == 0:
                print("Sleeping for a minute now")
                time.sleep(2)

        # Construct the full path to the CSV file in the specified directory
        parent_dir = os.path.join(self.path, "csv_files_v2")
        os.makedirs(parent_dir, exist_ok=True)
        csv_filepath = os.path.join(parent_dir, self.filename)

        # Write all data to a single CSV file
        with open(csv_filepath, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile, delimiter="|")
            csv_writer.writerows(csv_list)

        print(f"CSV file '{self.filename}' created successfully.")
