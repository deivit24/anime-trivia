from typing import Optional
from enum import Enum, auto

from transformers import AnimeCharacter


ANIME_TABLE = "anime.anime_character_description"
ANIME_TRIVIA_ANSWERS = "anime.trivia_question"

class DifficultyLevel(Enum):
    SUPER_EASY = auto()
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()
    IMPOSSIBLE = auto()


def difficulty_level_where_clause(level: DifficultyLevel) -> str:
    """
    Generate the WHERE clause for the specified difficulty level.

    Parameters:
    - level (DifficultyLevel): The difficulty level for character generation.

    Returns:
    str: The WHERE clause for the specified difficulty level.
    """
    if level == DifficultyLevel.SUPER_EASY:
        return "anime_popularity <= 10 AND character_rating IS NOT NULL"
    elif level == DifficultyLevel.EASY:
        return "anime_popularity BETWEEN 10 AND 20 AND character_rating IS NOT NULL"
    elif level == DifficultyLevel.MEDIUM:
        return "(anime_popularity + anime_favorited) / 2 BETWEEN 21 AND 50 AND character_rating IS NOT NULL"
    elif level == DifficultyLevel.HARD:
        return "(anime_popularity + anime_favorited) / 2 BETWEEN 51 AND 100 AND character_rating IS NOT NULL"
    elif level == DifficultyLevel.IMPOSSIBLE:
        return "(anime_popularity + anime_favorited) / 2 => 101 AND character_rating IS NOT NULL"


def build_query(
    table_name: str, 
    columns: str = "*", 
    where_clause: Optional[str] = None,
    order_by: Optional[str] = None, 
    limit: Optional[int] = None
) -> str:
    """
    Build a SQL query based on the provided parameters.

    Parameters:
    - table_name (str): The name of the table.
    - columns (str, optional): Comma-separated list of columns. Default is "*".
    - where_clause (str, optional): The WHERE clause for the query. Default is None.
    - order_by (str, optional): The ORDER BY clause for the query. Default is None.
    - limit (int, optional): The LIMIT for the query. Default is None.

    Returns:
    - str: The generated SQL query.
    """
    query = f"SELECT {columns} FROM {table_name}"

    if where_clause:
        query += f" WHERE {where_clause}"

    if order_by:
        query += f" ORDER BY {order_by}"

    if limit is not None:
        query += f" LIMIT {limit}"

    return query


def random_character_generator_query(level: DifficultyLevel) -> None:
    """
    Generate a random character based on the specified difficulty level.

    Parameters:
    - level (DifficultyLevel): The difficulty level for character generation.

    Returns:
    None
    """
    if level not in DifficultyLevel:
        raise ValueError("Invalid difficulty level")

    where_clause = difficulty_level_where_clause(level)
    
    result = build_query(
        table_name=ANIME_TABLE,
        columns="character_id, character_description, anime_id, character_name, character_rating, character_image",
        where_clause=where_clause,
        order_by="random()",
        limit=1
    )

    return result

def trivia_pool_query(answer_character: AnimeCharacter) -> str:
    """
    Build a SQL query for generating a trivia pool based on the provided answer_character.

    Parameters:
    - answer_character (AnimeCharacter): The character for which to generate the trivia pool.

    Returns:
    str: The generated SQL query for the trivia pool.
    """
    
    correct_answer_query = build_query(
        table_name=ANIME_TABLE,
        where_clause=f"anime_id = {answer_character.anime_id} AND character_id = {answer_character.character_id}"
    )

    random_characters_query = build_query(
        table_name=ANIME_TABLE,
        columns="character_id, character_description, anime_id, character_name, character_rating, character_image",
        where_clause=f"anime_id = (SELECT anime_id FROM correct_answer) AND character_id != (SELECT character_id FROM correct_answer) AND character_rating IS NOT NULL",
        order_by="random()",
        limit=4
    )

    correct_character_query = build_query(
        table_name=ANIME_TABLE,
        columns="character_id, character_description, anime_id, character_name, character_rating, character_image",
        where_clause=f"anime_id = {answer_character.anime_id} AND character_id = {answer_character.character_id}"
    )

    final_query = f"""
        WITH correct_answer as ({correct_answer_query}),
        random_characters as ({random_characters_query}),
        correct_character as ({correct_character_query})
        SELECT * FROM random_characters
        UNION
        SELECT * FROM correct_character;
    """
    return final_query

def create_trivia_sql(answer_character: AnimeCharacter, level: str):
    return f"""
        INSERT INTO {ANIME_TRIVIA_ANSWERS} (level, answer_id) VALUES ({level.value}, {answer_character.character_id})
        RETURNING id;
    """

def get_question(question_id: int):
    return f"SELECT answer_id FROM {ANIME_TRIVIA_ANSWERS} WHERE id = {question_id};"
