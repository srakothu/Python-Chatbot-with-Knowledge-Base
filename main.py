import json
from difflib import get_close_matches

def load_knowledge_base(file_path : str) -> dict:
  with open(file_path, 'r') as file:
    data : dict = json.load(file)
  return data

def save_knowledge_base(file_path : str, data: dict):
  with open(file_path, 'w') as file:
    json.dump(data, file, indent = 2)

def find_best_match(user_question: str, questions: list) -> str:
  matches : list = get_close_matches(user_question, questions, n = 1, cutoff = 0.5)
  return matches[0] if matches else ""

def get_answer_for_question(question: str, knowledge_base: dict) -> str:
  for q in knowledge_base["questions"]:
    if q["questions"] == question:
      return q["answer"]
  return ""

def chatbot():
  knowledge_base: dict = load_knowledge_base('knowledge_base.json')

  while True:
    user_input: str = input("You : ")

    if user_input.lower() == 'quit':
      break

    best_match: str | None = find_best_match(user_input, [q["questions"] for q in knowledge_base["questions"]])

    if best_match:
      answer: str = get_answer_for_question(best_match, knowledge_base)
      print(f'Chatbot: {answer}')
    else:
      print('Chatbot: I do not know the answer to that question.')
      new_answer: str = input('Type what you would like to be the answer to that question: OR "skip" to skip : ')

      if new_answer.lower() != 'skip':
        knowledge_base["questions"].append({"questions": user_input, "answer": new_answer})
        save_knowledge_base('knowledge_base.json', knowledge_base)
        print('Chatbot: Thank you for teaching me!')

if __name__ == '__main__':
  chatbot()
