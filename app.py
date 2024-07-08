from flask import Flask, request, jsonify, render_template
import nltk
from nltk.chat.util import Chat, reflections
from textblob import TextBlob
import datetime

app = Flask(__name__)

def get_time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")

def analyze_sentiment(text):
    blob = TextBlob(text)
    if blob.sentiment.polarity > 0:
        return "You seem to be in a good mood!"
    elif blob.sentiment.polarity < 0:
        return "I'm sorry to hear that you're feeling down."
    else:
        return "It seems like you're feeling neutral."

# Custom chat class to handle callable responses
class CustomChat(Chat):
    def respond(self, statement):
        response = super().respond(statement)
        if callable(response):
            return response(statement)
        return response

pairs = [
    (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
    (r'how are you?', ['I am good, thank you! How are you?', 'Doing well, how about you?']),
    (r'(.*) your name?', ['My name is Sachi Chatbot.', 'You can call me Sachi Chatbot.']),
    (r'what is (.*) favorite color?', ['My favorite color is blue.', 'I love all colors!']),
    (r'bye|goodbye', ['Goodbye!', 'See you later!', 'Have a nice day!']),
    (r'what time is it?', [lambda _: get_time()]),
    (r'(.*) weather (.*)', ['I am unable to provide weather updates right now.']),
    (r'I feel (.*)', [lambda matches: analyze_sentiment(matches)]),
    (r'(.*) created you?', ['I was created by a team of developers.']),
    (r'can you help me with (.*)?', ['I can try to help you with {0}.', 'Sure, what do you need help with?']),
    (r'what is your purpose?', ['I am here to chat with you and provide assistance.']),
    (r'what is (.*)', ['f{0} is a very interesting topic!', 'I don’t have the exact answer, but f{0} is fascinating!']),
    (r'tell me a joke', ['Why don’t scientists trust atoms? Because they make up everything!', 'Why did the scarecrow win an award? Because he was outstanding in his field!']),
    (r'what do you like to do?', ['I enjoy chatting with people and learning new things!', 'Talking to you is my favorite activity!']),
    (r'(.*) book', ['There are so many great books out there! Do you have a favorite?', 'I can’t read, but I hear that books are wonderful sources of knowledge.']),
    (r'how old are you?', ['I am timeless, as I am a computer program.', 'I don’t age, but I was created recently.']),
    (r'can you (.*)', ['I can try to {0}.', 'I’m not sure if I can {0}, but I can certainly try!']),
    (r'where are you from?', ['I exist in the digital world, created by developers.']),
    (r'(.*) favorite food?', ['I don’t eat, but I hear pizza is pretty popular!', 'Food is a human thing, but I imagine sushi is quite interesting.']),
    (r'what do you think about (.*)?', ['I think {0} is quite intriguing!', 'I don’t have opinions, but {0} seems worth thinking about.']),
    (r'how are you',['I am just a bunch of code, but thanks for asking!', 'I am here to assist you.', 'Doing great, how about you?']),
    (r'what is your name', ['I am Sachi Chatbot, your virtual assistant.', 'You can call me Sachi.']),
    (r'i feel tired', ['You should get some rest.', 'Maybe a nap would help.', 'Do not forget to take care of yourself.']),
    (r'i am good', ['That is great to hear!', 'Glad to know you are doing well.', 'Awesome!']),
    (r'(.*)', ['I am not sure I understand you.', 'Can you rephrase that?', 'Interesting... tell me more!'])

]

reflections = {
    "i am": "you are",
    "i was": "you were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "you are": "I am",
    "you were": "I was",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}

chatbot = CustomChat(pairs, reflections)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message")
    response = chatbot.respond(user_input)
    if callable(response):
        response = response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
