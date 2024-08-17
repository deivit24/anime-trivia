import "./style.css";
import van from "vanjs-core";
import { TriviaApi } from "./utils/api";
import { Question } from "./question";
const { h1, div, input, select, option } = van.tags;
const app = document.querySelector("#app");
const triviaApi = new TriviaApi();

const levels = [
  {
    name: "Super Easy",
    value: "SUPER_EASY",
  },
  {
    name: "Easy",
    value: "EASY",
  },
  {
    name: "Medium",
    value: "MEDIUM",
  },
  {
    name: "Hard",
    value: "HARD",
  },
  {
    name: "Impossible",
    value: "IMPOSSIBLE",
  },
];

const questions = van.state([]);

const getTrivia = async (level) => {
  try {
    const data = await triviaApi.fetchDataByLevel(level);
    questions.val = data;
  } catch (error) {
    console.error(error);
  }
};
const Options = ({ items }) =>
  select(
    { name: "Level", onchange: (e) => getTrivia(e.target.value) },
    option({ text: "Select a level", disabled: true, selected: true }),
    items.map((it) => option({ text: it.name, value: it.value })),
  );

const Questions = ({ items }) =>
  items.map((i) =>
    Question({
      imgSrc: i.image,
      characters: i.characters,
      question: i.question_id,
    }),
  );

const view = van.derive(() => {
  return questions.val.length > 0
    ? div(Questions({ items: questions.val }))
    : Options({ items: levels });
});
const Main = () => {
  return div(h1("Test VanJS"), div(view));
};

van.add(app, Main());
