import requests
import json
import os
import random

class LanguageTeacherAgent:
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
        self.languages = ["Dutch", "English", "Chinese", "Spanish"]
        self.lesson_types = ["vocabulary", "grammar", "conversation", "translation"]
        
    def claude_request(self, messages):
        data = {
            "model": "claude-3-opus-20240229",
            "messages": messages,
            "max_tokens": 1000
        }
        response = requests.post(self.base_url, headers=self.headers, json=data)
        return response.json()['content'][0]['text']

    def greet(self):
        messages = [{"role": "user", "content": f"You are a friendly language teacher AI. Greet the student and ask which language they'd like to learn. The available languages are: {', '.join(self.languages)}. Keep your response concise and encouraging."}]
        return self.claude_request(messages)

    def generate_lesson(self, language, lesson_type):
        messages = [
            {"role": "user", "content": f"You are a {language} language teacher. Generate a brief, engaging {lesson_type} lesson suitable for a beginner. Include 3-5 examples or practice items. For vocabulary and translation, provide both the {language} and English versions. For grammar and conversation, explain in English and provide examples in {language} with translations. Format your response as JSON with 'explanation' and 'examples' keys. Keep the entire response under 200 words."}
        ]
        response = self.claude_request(messages)
        try:
            lesson_data = json.loads(response)
            return lesson_data
        except json.JSONDecodeError:
            return {"explanation": "I'm sorry, I couldn't generate a proper lesson. Let's try again.", "examples": []}

    def practice_exercise(self, language, lesson_type, examples):
        if not examples:
            return "I'm sorry, I couldn't generate a practice exercise. Let's try another lesson."
        
        exercise = random.choice(examples)
        if lesson_type in ["vocabulary", "translation"]:
            question = f"Translate this {language} word or phrase to English: {exercise[language]}"
            answer = exercise['English']
        elif lesson_type == "grammar":
            question = f"Complete this {language} sentence using the correct grammar: {exercise[language]}"
            answer = exercise['English']
        else:  # conversation
            question = f"Respond to this {language} phrase appropriately: {exercise[language]}"
            answer = exercise['English']
        
        return question, answer

    def evaluate_answer(self, user_answer, correct_answer, language):
        messages = [
            {"role": "user", "content": f"You are a supportive {language} teacher. The correct answer is '{correct_answer}'. The student's answer was '{user_answer}'. Evaluate if the student's answer is correct or close enough. If it's wrong or could be improved, explain why and provide a helpful tip. Keep your response concise and encouraging."}
        ]
        return self.claude_request(messages)

    def run(self):
        print(self.greet())
        while True:
            language = input("Choose a language to learn (or 'quit' to exit): ").capitalize()
            if language.lower() == 'quit':
                print("Thank you for learning with me. Goodbye!")
                break
            if language not in self.languages:
                print(f"I'm sorry, I don't teach that language yet. Please choose from {', '.join(self.languages)}.")
                continue
            
            lesson_type = random.choice(self.lesson_types)
            print(f"\nLet's have a {lesson_type} lesson in {language}!")
            
            lesson = self.generate_lesson(language, lesson_type)
            print("\nLesson:")
            print(lesson['explanation'])
            print("\nExamples:")
            for example in lesson['examples']:
                print(f"{example[language]} - {example['English']}")
            
            input("\nPress Enter when you're ready for a practice exercise.")
            
            question, answer = self.practice_exercise(language, lesson_type, lesson['examples'])
            print("\n" + question)
            user_answer = input("Your answer: ")
            print(self.evaluate_answer(user_answer, answer, language))

if __name__ == "__main__":
    teacher = LanguageTeacherAgent()
    teacher.run()
