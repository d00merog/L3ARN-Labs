import requests
import json
import os
import random

class HistoryTeacherAgent:
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
        self.eras = [
            "Ancient Civilizations", "Medieval Period", "Renaissance", 
            "Age of Exploration", "Industrial Revolution", "World Wars", 
            "Cold War", "Modern Era"
        ]
        self.lesson_types = ["event", "figure", "civilization", "invention"]
        
    def claude_request(self, messages):
        data = {
            "model": "claude-3-opus-20240229",
            "messages": messages,
            "max_tokens": 1000
        }
        response = requests.post(self.base_url, headers=self.headers, json=data)
        return response.json()['content'][0]['text']

    def greet(self):
        messages = [{"role": "user", "content": f"You are a friendly history teacher AI. Greet the student and ask which historical era they'd like to learn about. The available eras are: {', '.join(self.eras)}. Keep your response concise and engaging."}]
        return self.claude_request(messages)

    def generate_lesson(self, era, lesson_type):
        messages = [
            {"role": "user", "content": f"You are a history teacher. Generate a brief, engaging lesson about a significant {lesson_type} from the {era}. Include key facts, its historical importance, and an interesting anecdote. Format your response as JSON with 'topic', 'content', and 'quiz_question' keys. The 'quiz_question' should be a multiple-choice question with 4 options (A, B, C, D) and the correct answer. Keep the entire response under 250 words."}
        ]
        response = self.claude_request(messages)
        try:
            lesson_data = json.loads(response)
            return lesson_data
        except json.JSONDecodeError:
            return {"topic": "Error", "content": "I'm sorry, I couldn't generate a proper lesson. Let's try again.", "quiz_question": {}}

    def evaluate_answer(self, user_answer, correct_answer, question):
        messages = [
            {"role": "user", "content": f"You are a supportive history teacher. The question was: '{question}'. The correct answer is {correct_answer}. The student's answer was {user_answer}. Evaluate if the student's answer is correct. If it's wrong, explain why and provide a brief additional historical fact related to the topic. Keep your response concise and encouraging."}
        ]
        return self.claude_request(messages)

    def discussion_prompt(self, topic):
        messages = [
            {"role": "user", "content": f"You are a history teacher. Generate a thought-provoking discussion question related to the topic: '{topic}'. The question should encourage critical thinking about historical events, their causes, and their impacts. Keep your response concise."}
        ]
        return self.claude_request(messages)

    def run(self):
        print(self.greet())
        while True:
            era = input("Choose a historical era to learn about (or 'quit' to exit): ")
            if era.lower() == 'quit':
                print("Thank you for learning history with me. Goodbye!")
                break
            if era not in self.eras:
                print(f"I'm sorry, I don't have lessons for that era yet. Please choose from {', '.join(self.eras)}.")
                continue
            
            lesson_type = random.choice(self.lesson_types)
            print(f"\nLet's learn about a significant {lesson_type} from the {era}!")
            
            lesson = self.generate_lesson(era, lesson_type)
            print(f"\nToday's topic: {lesson['topic']}")
            print("\nLesson:")
            print(lesson['content'])
            
            input("\nPress Enter when you're ready for a quiz question.")
            
            quiz = lesson['quiz_question']
            print("\n" + quiz['question'])
            for option, answer in quiz['options'].items():
                print(f"{option}: {answer}")
            user_answer = input("Your answer (A, B, C, or D): ").upper()
            print(self.evaluate_answer(user_answer, quiz['correct_answer'], quiz['question']))

            print("\nLet's discuss this topic further.")
            discussion_question = self.discussion_prompt(lesson['topic'])
            print("\nDiscussion question:")
            print(discussion_question)
            input("Take a moment to think about this question. Press Enter when you're ready to move on.")

if __name__ == "__main__":
    teacher = HistoryTeacherAgent()
    teacher.run()
