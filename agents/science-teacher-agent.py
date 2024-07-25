import requests
import json
import os

class ScienceTeacherAgent:
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
        self.topics = ["biology", "chemistry", "physics", "earth science", "astronomy"]
        
    def claude_request(self, messages):
        data = {
            "model": "claude-3-opus-20240229",
            "messages": messages,
            "max_tokens": 1000
        }
        response = requests.post(self.base_url, headers=self.headers, json=data)
        return response.json()['content'][0]['text']

    def greet(self):
        messages = [{"role": "user", "content": "You are a friendly science teacher AI. Greet the student and ask what topic they'd like to learn about. The available topics are: " + ", ".join(self.topics) + ". Keep your response concise and engaging."}]
        return self.claude_request(messages)

    def generate_lesson(self, topic):
        messages = [
            {"role": "user", "content": f"You are a science teacher. Generate a brief, engaging lesson on a specific concept in {topic} suitable for a high school student. Include a fun fact and a thought-provoking question at the end. Keep your response under 200 words."}
        ]
        return self.claude_request(messages)

    def generate_quiz(self, topic):
        messages = [
            {"role": "user", "content": f"You are a science teacher. Create a multiple-choice quiz question related to {topic} for a high school student. Provide the question, four answer options (A, B, C, D), and the correct answer. Format your response as JSON with 'question', 'options', and 'correct_answer' keys."}
        ]
        response = self.claude_request(messages)
        try:
            quiz_data = json.loads(response)
            return quiz_data
        except json.JSONDecodeError:
            return None

    def evaluate_answer(self, user_answer, correct_answer, question):
        messages = [
            {"role": "user", "content": f"You are a supportive science teacher. The question was: '{question}'. The correct answer is {correct_answer}. The student's answer was {user_answer}. Evaluate if the student's answer is correct. If it's wrong, explain why and provide a brief additional fact related to the topic. Keep your response concise and encouraging."}
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
                print(f"I'm sorry, I don't have lessons for that topic yet. Please choose from {', '.join(self.topics)}.")
                continue
            
            print("\nHere's a brief lesson on " + topic + ":")
            print(self.generate_lesson(topic))
            
            input("\nPress Enter when you're ready for a quiz question.")
            
            quiz = self.generate_quiz(topic)
            if quiz:
                print("\n" + quiz['question'])
                for option, answer in quiz['options'].items():
                    print(f"{option}: {answer}")
                user_answer = input("Your answer (A, B, C, or D): ").upper()
                print(self.evaluate_answer(user_answer, quiz['correct_answer'], quiz['question']))
            else:
                print("I'm sorry, I couldn't generate a quiz question. Let's try another topic.")

if __name__ == "__main__":
    teacher = ScienceTeacherAgent()
    teacher.run()
