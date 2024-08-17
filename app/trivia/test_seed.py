from psycopg2 import connect
from decouple import config


DB_PARAMS = {
    "host": config("POSTGRES_HOST"),
    "database": config("POSTGRES_DB"),
    "user": config("POSTGRES_USER"),
    "password": config("POSTGRES_PASSWORD"),
}

sql_script = """
DROP SCHEMA IF EXISTS anime CASCADE;
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS anime;

DROP TABLE IF EXISTS raw.anime;

CREATE TABLE raw.anime(
    id serial PRIMARY KEY,
    external_id integer,
    image text,
    title text,
    award text,
    type text,
    episodes text,
    rating text,
    average text,
    reviews text,
    users integer,
    aired text,
    ended text,
    popularity text,
    favorites text,
    rating_number text,
    rating_rank text
);

COPY raw.anime (
    id,
    external_id,
    image,
    title,
    award,
    type,
    episodes,
    rating,
    average,
    reviews,
    users,
    aired,
    ended,
    popularity,
    favorites,
    rating_number,
    rating_rank
)
FROM '/usr/local/anime.csv' CSV HEADER DELIMITER ',' QUOTE '"';

DROP TABLE IF EXISTS raw.character;

CREATE TABLE raw.character(
    external_id integer,
    image text,
    name text,
    type text,
    anime_appearance text,
    age text,
    gender text,
    blood_type text,
    dob text,
    rating text,
    waifu text,
    trash text,
    id serial PRIMARY KEY
);

COPY raw.character (
    external_id ,
    image,
    name,
    type,
    anime_appearance,
    age,
    gender,
    blood_type,
    dob,
    rating,
    waifu,
    trash
)
FROM '/usr/local/character.csv' CSV HEADER DELIMITER ',' QUOTE '"';

DROP TABLE IF EXISTS raw.character_desc;

CREATE TABLE raw.character_desc(
    external_id integer,
    name text,
    description text
);

COPY raw.character_desc (
    external_id ,
    name,
    description
)
FROM '/usr/local/character_desc.csv' CSV HEADER DELIMITER '|' QUOTE '"';

CREATE TABLE anime.trivia_question(
    id serial PRIMARY KEY,
    level text,
    answer_id integer
);
"""
cursor = None
connection = None
try:
    # Connect to the PostgreSQL database
    connection = connect(**DB_PARAMS)

    # Create a cursor object
    cursor = connection.cursor()

    # Execute the SQL script, passing the full paths as parameters
    cursor.execute(sql_script)

    # Commit the changes
    connection.commit()

    print("SQL script executed successfully.")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()
