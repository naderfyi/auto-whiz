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
   git clone https://github.com/naderfyi/auto-whiz.git
   cd auto-whiz
   ```

2. Install the dependencies:
   ```bash
    pip install -r requirements.txt
   ```

3. Create a .env file in the root directory and add your OpenAI API key:
    ```bash
    OPENAI_API_KEY='your_openai_api_key_here'
    ```

4. Run the Flask app:
    ```bash
    flask run
    ```

5. Run the frontend server:
    ```bash
    cd frontend
    npm install
    npm start
    ```

6. Open your browser and navigate to `http://localhost:3000` to access the application.

## Usage
1. Enter your preferences for Mercedes-Benz electric vehicles.
2. Chat with the AI to receive personalized recommendations.
3. View the recommended vehicles and their attributes.
4. Explore the details of each vehicle.
