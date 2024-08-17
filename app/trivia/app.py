from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from main import TriviaGenerator

origins = ["http://localhost", "http://localhost:5173", "*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnswerCheck(BaseModel):
    question_id: int
    answer_id: int


@app.get("/trivia")
async def get_trivia(level: str, questions: int = 5):
    trivia_questions = []
    trivia_generator = TriviaGenerator(level)
    while len(trivia_questions) != questions:
        trivia_question = trivia_generator.generate_trivia()
        trivia_questions.append(trivia_question)
    return jsonable_encoder(trivia_questions)


@app.post("/trivia")
async def check_answer(data: AnswerCheck):
    trivia = TriviaGenerator()
    is_correct = trivia.check_answer(data.question_id, data.answer_id)
    return jsonable_encoder({"result": is_correct})
