AI-Powered Interview Preparation Bot

This project is an AI-powered bot designed to help candidates prepare for job interviews by simulating an interactive Q&A session. It was developed as a final submission for the Mission UpSkill India Hackathon.

Features
Customizable Interviews: Choose your mock interview role, domain, difficulty, and number of questions.

Dynamic Question Generation: The bot generates relevant interview questions tailored to your selections.

Real-time Feedback: Receive immediate, constructive feedback and a score out of 100 for each answer.

Comprehensive Summary: After the interview, get a detailed report of your performance, including strengths, weaknesses, and a personalized improvement plan.

Session History: Review a complete history of all questions and answers from your interview session.

Downloadable Report: Save your interview session as a JSON file for future reference.

Technologies Used
Python: The core programming language for the bot's logic.

Streamlit: Used to create the interactive, web-based user interface.

Groq API: Powers the AI's ability to generate questions, evaluate answers, and provide detailed feedback.

Dotenv: Used for managing environment variables securely.

Setup and Installation
Follow these steps to set up and run the project on your local machine.

Step 1: Clone the Repository
Clone this repository to your local machine using Git.

git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name

Step 2: Set Up the Groq API Key
You will need an API key from Groq to run the bot.

Go to the Groq Console.

Sign up or log in.

Navigate to the API keys section and create a new key.

Copy your API key.

Create a new file named .env in the root of your project directory.

Add your API key to this file in the following format:

GROQ_API_KEY="your_api_key_here"

Step 3: Install Dependencies
Make sure you have Python installed. Then, install the required libraries using pip.

pip install -r requirements.txt

Note: If you don't have a requirements.txt file, you can create one by running:

pip freeze > requirements.txt

Alternatively, you can install the dependencies manually:

pip install streamlit groq python-dotenv

Step 4: Run the Application
Once everything is set up, run the Streamlit application from your terminal.

streamlit run app.py

The application will open in your web browser. You can then begin your mock interview.

Documentation
The project consists of two main Python files:

app.py: This file contains the Streamlit application code, managing the user interface, session state, and user interactions.

bot_engine.py: This file handles the core logic of the interview bot, including all calls to the Groq API for question generation, evaluation, and summary creation.
