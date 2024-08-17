import van from "vanjs-core";
import { TriviaApi } from "./utils/api";
const { img, fieldset, legend, div, input, label } = van.tags;

const handle = async (questionId, answerId) => {
  const triviaApi = new TriviaApi();
  const response = await triviaApi.checkAnswer(questionId, answerId);
  if (response.result) {
    alert("Good Job!");
  } else {
    alert("You are one dumb mother fucker");
  }
  document.getElementById(questionId).style.display = "none";
};

export const Question = ({ imgSrc, characters, question }) => {
  const Names = ({ items }) =>
    items.map((i) =>
      div(
        {
          style:
            "display: flex; justify-content: start; padding:2px; margin-top: 5px; margin-bottom: 5px;",
        },
        input({
          type: "radio",
          name: question,
          id: i.character_id,
          value: i.character_id,
          onclick: () => handle(question, i.character_id),
        }),
        label({ for: i.character_id }, i.name),
      ),
    );

  return div(
    { id: question, style: "margin-bottom:15px" },
    fieldset(
      legend(
        img({
          style: "margin-top: 10px;",
          src: imgSrc,
          referrerPolicy: "no-referrer",
        }),
      ),
      Names({ items: characters }),
    ),
  );
};
