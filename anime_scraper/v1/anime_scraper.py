import re
import os
import csv
import time

from bs4 import BeautifulSoup

from utils import (
    IMAGE,
    TITLE,
    NO,
    fetch_html_from_url,
    auth_login,
    fetch_session_from_url,
)


def clean_text(cell: BeautifulSoup) -> str:
    """
    Clean the text content of a BeautifulSoup cell.

    Args:
        cell (BeautifulSoup): The BeautifulSoup cell containing text or an image.

    Returns:
        str: The cleaned text.
    """

    label = cell.get("data-label")

    if label == IMAGE:
        img_tag = cell.find("img")
        if img_tag:
            text = img_tag.get("src")
        else:
            text = None
    elif label == TITLE:
        a_tag = cell.find("a")
        text = a_tag.get_text(strip=True)
    elif label == NO:
        text = cell.get_text(strip=True)
        parts = text.split("/")
        text = parts[-1] if len(parts) > 2 else None
    else:
        text = cell.get_text(strip=True)

    return text


def html_table_to_csv(base_url: str, csv_filename: str, num_pages: int) -> None:
    """
    Extract data from HTML tables across multiple pages and write it to a single CSV file.

    Args:
        base_url (str): The base URL of the webpages containing the HTML tables.
        csv_filename (str): The filename for the CSV file.
        num_pages (int): The number of pages to loop through.

    Returns:
        None
    """
    # Initialize an empty list to store the data
    all_data = []

    session = auth_login()

    # Loop through the specified number of pages
    for page in range(num_pages):
        current_url = base_url.format(page)
        # Fetch HTML content from the URL
        soup = fetch_session_from_url(current_url, session)
        # Find the table with the specified ID
        table = soup.table
        if table:
            # Extract data from the table
            rows = table.find_all("tr")
            data = []

            for row in rows:
                # Extract text from each cell in the row
                cells = row.find_all(["th", "td"])
                # Find the cell with data-label equal to "No"
                no_cell = row.find("td", {"data-label": "No"})
                title_cell = row.find("td", {"data-label": "Title"})
                x_cell = row.find("td", {"data-label": "x"})

                if x_cell and no_cell:
                    x_cell.string = no_cell.get_text()
                if no_cell and title_cell:
                    no_cell.string = title_cell.find("a").get("href")

                # Check if it's the first loop to exclude 'th' elements
                if page == 0:
                    row_data = [clean_text(cell) for cell in cells]
                    data.append(row_data)

                else:
                    # Skip 'th' elements in subsequent loops
                    row_data = [clean_text(cell) for cell in cells if cell.name == "td"]
                    if row_data:
                        data.append(row_data)

            # Append data to the list
            all_data.extend(data)
            print(f"Table number {page} downloaded for {csv_filename}.")
        else:
            print(f"Table not found on page {page}.")
            return
        if page % 50 == 49:
            print("Sleeping for a minute now")
            time.sleep(60)

    # Get the current script's directory
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Construct the full path to the CSV file in the root of the current file
    csv_filepath = os.path.join(script_dir, "csv_files_v1", csv_filename)
    os.makedirs(os.path.dirname(csv_filepath), exist_ok=True)
    header = all_data[0]

    column_to_remove = "Action"
    if column_to_remove in header:
        column_index = header.index(column_to_remove)
        all_data = [row[:column_index] + row[column_index + 1 :] for row in all_data]

    # Write all data to a single CSV file
    with open(csv_filepath, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(all_data)

    print(f"CSV file '{csv_filename}' created successfully.")


def html_grid_to_csv(base_url: str, csv_filename: str, num_pages: int) -> None:
    """
    Extract data from HTML grid across multiple pages and write it to a single CSV file.

    Args:
        base_url (str): The base URL of the webpages containing the HTML grid.
        csv_filename (str): The filename for the CSV file.
        num_pages (int): The number of pages to loop through.

    Returns:
        None
    """
    # Initialize an empty list to store the data
    all_data = [["external_id", "name", "description"]]

    session = auth_login()

    # Loop through the specified number of pages
    for page in range(num_pages):
        current_url = base_url.format(page)
        # Fetch HTML content from the URL
        soup = fetch_session_from_url(current_url, session)
        # Find the grid with the specified class
        grid_div = soup.find("div", {"class": "characterlist_grid"})
        # print(grid)
        if grid_div:
            # Extract data from the grid
            grids = grid_div.find_all("div", {"class": "g_bubble box"})
            data = []
            for grid in grids:
                grid_data = grid.find("div", {"class": "data"})
                grid_desc = grid_data.find("div", {"class": "desc"})
                grid_name = grid_data.find("a", {"class": "name-colored"})
                if grid_desc and grid_name:
                    desc = grid_desc.get_text(strip=True)
                    name = grid_name.get_text(strip=True)
                    href = grid_name.get("href")
                    parts = href.split("/")
                    href = parts[-1] if len(parts) > 2 else None
                    data.append([href, name, desc])

            # Append data to the list
            all_data.extend(data)
            print(f"Page number {page} downloaded for {csv_filename}.")
        else:
            print(f"Page not found on page {page}.")
            return
        if page % 50 == 49:
            print("Sleeping for a minute now")
            time.sleep(60)

    # Get the current script's directory
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Construct the full path to the CSV file in the root of the current file
    csv_filepath = os.path.join(script_dir, "csv_files_v1", csv_filename)
    os.makedirs(os.path.dirname(csv_filepath), exist_ok=True)
    # Write all data to a single CSV file
    with open(csv_filepath, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter="|")
        csv_writer.writerows(all_data)

    print(f"CSV file '{csv_filename}' created successfully.")
