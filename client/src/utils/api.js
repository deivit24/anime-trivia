const API_BASE = "http://localhost:8000/trivia";

export class TriviaApi {
  constructor(baseURL = API_BASE) {
    /**
     * @property {string} baseURL - The base URL for the API.
     * @property {string} this.baseURL - The base URL assigned to the class instance.
     */
    this.baseURL = baseURL;
  }

  /**
   * Fetches trivia data by difficulty level.
   *
   * @param {string} level - The difficulty level of the trivia data (e.g., 'easy', 'medium', 'hard').
   * @param {number} questions - The number of questions
   * @returns {Promise<Object>} - A promise that resolves to the fetched data.
   * @throws Will throw an error if the fetch request fails.
   */
  async fetchDataByLevel(level, questions = 5) {
    try {
      const response = await fetch(
        `${this.baseURL}?level=${level}&questions=${questions}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            // Add more headers here if needed
          },
        },
      );

      if (!response.ok) {
        throw new Error(`Error fetching data: ${response.statusText}`);
      }

      const data = await response.json();

      // Handle the data as needed, e.g., return it
      return data;
    } catch (error) {
      // Handle errors
      console.error("Error fetching data:", error);
      throw error;
    }
  }

  async checkAnswer(questionId, answerId) {
    try {
      const response = await fetch(`${this.baseURL}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question_id: questionId, answer_id: answerId }),
      });

      if (!response.ok) {
        throw new Error("Error");
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
}
