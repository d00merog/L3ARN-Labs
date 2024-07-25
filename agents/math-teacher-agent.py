import random
import requests
import json
import os

class MathTeacherAgent:
    def __init__(self):
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Please set the ANTHROPIC_API_KEY environment variable")
        self.base_url = "https://api.anthropic.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        self.topics = ["addition", "subtraction", "multiplication", "division", "algebra", "geometry"]
        
    def claude_request(self, messages):
        data = {
            "model": "claude-3-opus-20240229",
            "messages": messages,
            "max_tokens": 1000
        }
        response = requests.post(self.base_url, headers=self.headers, json=data)
        return response.json()['content'][0]['text']

    def greet(self):
        messages = [{"role": "user", "content": "You are a friendly math teacher AI. Greet the student and ask what topic they'd like to practice. The available topics are: " + ", ".join(self.topics) + ". Keep your response concise."}]
        return self.claude_request(messages)

    def generate_problem(self, topic):
        messages = [
            {"role": "user", "content": f"You are a math teacher. Generate a {topic} problem suitable for a middle school student. Provide the problem statement and the correct answer. Format your response as JSON with 'problem' and 'answer' keys."}
        ]
        response = self.claude_request(messages)
        try:
            problem_data = json.loads(response)
            return problem_data['problem'], problem_data['answer']
        except json.JSONDecodeError:
            return "I'm sorry, I couldn't generate a proper problem. Let's try again.", None

    def check_answer(self, user_answer, correct_answer, problem):
        messages = [
            {"role": "user", "content": f"You are a supportive math teacher. The problem was: '{problem}'. The correct answer is {correct_answer}. The student's answer was {user_answer}. Evaluate if the student's answer is correct. If it's wrong, explain why and provide a hint for solving similar problems. Keep your response concise and encouraging."}
        ]
        return self.claude_request(messages)

    def run(self):
        print(self.greet())
        while True:
            topic = input("Choose a topic (or 'quit' to exit): ").lower()
            if topic == 'quit':
                print("Thank you for learning with me. Goodbye!")
                break
            if topic not in self.topics:
                print(f"I'm sorry, I don't have problems for that topic yet. Please choose from {', '.join(self.topics)}.")
                continue
            problem, answer = self.generate_problem(topic)
            print(problem)
            user_answer = input("Your answer: ")
            print(self.check_answer(user_answer, answer, problem))

if __name__ == "__main__":
    teacher = MathTeacherAgent()
    teacher.run()
