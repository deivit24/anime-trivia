from db_connector import DbConnector
from transformers import AnimeCharacter
from utils import (
    trivia_pool_query,
    random_character_generator_query,
    get_question,
    create_trivia_sql,
    DifficultyLevel,
)


class TriviaGenerator:
    def __init__(self, difficulty_string: str = "SUPER_EASY"):
        self.difficulty_mapping = {
            "SUPER_EASY": DifficultyLevel.SUPER_EASY,
            "EASY": DifficultyLevel.EASY,
            "MEDIUM": DifficultyLevel.MEDIUM,
            "HARD": DifficultyLevel.HARD,
            "IMPOSSIBLE": DifficultyLevel.IMPOSSIBLE,
        }

        # Convert the string to the corresponding DifficultyLevel enum value
        self.difficulty_level = self.difficulty_mapping.get(difficulty_string)
        self.db_connector = DbConnector()

    def create_record(self, answer_character):
        query = create_trivia_sql(answer_character, self.difficulty_level)
        result = self.db_connector.execute_query(query)

        # Commit the transaction
        self.db_connector.save()

        return result

    def check_answer(self, question_id: int, answer_id: int) -> bool:
        try:
            # Connect to the database
            self.db_connector.connect()
            query = get_question(question_id)
            result = self.db_connector.execute_query(query)
            if not result:
                return False
            return int(result[0][0]) == answer_id
        finally:
            # Disconnect from the database in a finally block to ensure it happens even if an exception occurs
            self.db_connector.disconnect()

    def generate_trivia(self):
        try:
            # Connect to the database
            self.db_connector.connect()

            # Generate the answer character
            answer_character_query = random_character_generator_query(
                self.difficulty_level
            )

            answer_result = self.db_connector.execute_query(
                query=answer_character_query
            )
            answer_character = AnimeCharacter(*answer_result[0])
            answer = self.create_record(answer_character)
            question_id = answer[0][0]
            # Generate the trivia pool
            questions_query = trivia_pool_query(answer_character)
            questions = self.db_connector.execute_query(query=questions_query)
            anime_characters = []
            for question in questions:
                char = AnimeCharacter(*question).to_dict()
                anime_characters.append(
                    {
                        "name": char.get("character_name", None),
                        "character_id": char.get("character_id", None),
                    }
                )
            return {
                "characters": anime_characters,
                "question_id": question_id,
                "image": answer_character.to_dict()["character_image"],
            }
        finally:
            # Disconnect from the database in a finally block to ensure it happens even if an exception occurs
            self.db_connector.disconnect()


# Example usage
# difficulty_string = "MEDIUM"
# trivia_generator = TriviaGenerator(difficulty_string)
# anime_characters = trivia_generator.generate_trivia()
