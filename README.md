# AutoWhiz: Mercedes-Benz EV Consultant App

## Overview
AutoWhiz is a Flask-based web application designed to serve as an AI consultant for Mercedes-Benz electric vehicles. Leveraging the power of OpenAI's GPT models and FAISS vector search, it provides personalized vehicle recommendations based on user preferences.

## Features
- **Data-Driven Recommendations:** Utilizes a FAISS vector store built from a dataset of electric vehicle attributes.
- **Interactive AI Chat:** Engages users with a conversational AI that provides responses tailored to their specific needs regarding Mercedes-Benz electric vehicles.
- **Session-Based Query History:** Maintains a history of user queries and AI responses within a session to provide context-aware interactions.

## Installation
To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/autowhiz.git
   cd autowhiz
   ```

2. Install the dependencies:
   ```bash
    pip install flask python-dotenv pandas langchain-community langchain-openai
   ```

3. Create a .env file in the root directory and add your OpenAI API key:
    ```bash
    OPENAI_API_KEY='your_openai_api_key_here'
    ```

4. Run the Flask app:
    ```bash
    python app.py
    ```

5. Usage
    - Open your browser and navigate to `http://127.0.0.1:5000/` to access the AutoWhiz web application.
    - Enter your preferences and interact with the AI chatbot to receive personalized vehicle recommendations.
