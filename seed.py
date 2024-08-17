import os
import subprocess


DOCKER_DB_CONTAINER = "anime-db"
DOCKER_API_CONTAINER = "anime-api"
DOCKER_PATH = "/usr/local"

CSV_PATH = "anime_scraper/v1/csv_files_v1"
ANIME_FILE = "anime.csv"
CHARACTER_FILE = "character.csv"
CHARACTER_DESC_FILE = "character_desc.csv"

ANIME_PATH = os.path.abspath(os.path.join(CSV_PATH, ANIME_FILE))
CHARACTER_PATH = os.path.abspath(os.path.join(CSV_PATH, CHARACTER_FILE))
CHARACTER_DESC_PATH = os.path.abspath(os.path.join(CSV_PATH, CHARACTER_DESC_FILE))

CSV_PATH_LIST = [ANIME_PATH, CHARACTER_PATH, CHARACTER_DESC_PATH]


def copy_to_docker(from_path, container_name, to_path):
    try:
        subprocess.run(
            ["docker", "cp", from_path, f"{container_name}:{to_path}"],
            check=True,
            text=True,
        )
        print(
            f"File copied from {from_path} to {container_name}:{to_path} successfully."
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running the 'docker cp' command: {e}")
    except FileNotFoundError:
        print(
            "Docker command not found. Make sure Docker is installed and available in your PATH."
        )


def run_command_in_docker(container_name, command):
    try:
        result = subprocess.run(
            ["docker", "exec", container_name, "sh", "-c", command],
            check=True,
            text=True,
            capture_output=True,
        )
        print(f"Command executed successfully:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running command in Docker container: {e}\n{e.stderr}")


for csv_path in CSV_PATH_LIST:
    copy_to_docker(csv_path, DOCKER_DB_CONTAINER, DOCKER_PATH)

run_command_in_docker(DOCKER_API_CONTAINER, "python /usr/src/trivia/test_seed.py")

run_command_in_docker(DOCKER_API_CONTAINER, "cd /usr/src/dbt_anime && dbt run")
