# Trip Planner Chatbot 🧳

Welcome to the Trip Planner Chatbot! This is a dynamic and interactive chatbot application built with Streamlit, Groq, and OpenWeather API. It helps users plan their trips by generating a personalized itinerary, providing weather updates, and engaging in an interactive conversation.

## Table of Contents
- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [How to Run](#how-to-run)
- [Technical Details](#technical-details)
  - [Neo4j Integration](#neo4j-integration)
  - [Ollama Integration](#ollama-integration)
  - [Prompting and Conversation Flow](#prompting-and-conversation-flow)
- [Contributing](#contributing)
- [License](#license)

## Overview
The Trip Planner Chatbot allows users to plan their trips with ease. It helps users:
- Choose a destination city.
- Set a budget for the trip.
- Share trip preferences (e.g., culture, food, adventure).
- Generate a one-day itinerary based on the input.
- Provide real-time weather information for the selected city.

The app also includes a login page to ensure that only authorized users can interact with the chatbot.

## Technologies Used
- **Streamlit**: A powerful tool for creating interactive web applications in Python.
- **Groq API**: For natural language processing (NLP) and generating trip itineraries based on the user’s inputs. This chatbot uses Groq's language model (`llama3-groq-70b-8192-tool-use-preview`).
- **OpenWeather API**: To fetch real-time weather data of the user's selected city.
- **Neo4j**: A graph database used to store and query city data, itineraries, and preferences for future use (not implemented in this version, but available for integration).
- **Ollama**: A tool for generating natural language responses to structured prompts (used for itinerary generation).

## Features
- **User Login**: Secure login functionality with predefined credentials.
- **Chatbot Conversation**: The chatbot guides the user through multiple stages, such as selecting a city, setting a budget, choosing preferences, and generating a detailed itinerary.
- **Weather Integration**: Fetches and displays real-time weather data of the selected city using the OpenWeather API.
- **Dynamic Itinerary Generation**: The bot uses the Groq API to generate personalized itineraries based on user inputs.
- **Responsive UI**: Built with Streamlit for a smooth, interactive user experience.

## How to Run

### Prerequisites
Install dependencies:

```bash
pip install streamlit requests groq

```
You will need a Groq API key to interact with the Groq language model. You can get an API key by signing up on the Groq website.

You will also need an OpenWeather API key to fetch weather data. You can get one by signing up at OpenWeather.

Running the App
Once you have the dependencies installed and the necessary API keys, you can run the app:

```bash

streamlit run app.py

```
This will launch the application in your default web browser.

Technical Details
1. Groq Integration
Groq is used for language generation, and it powers the core functionality of the chatbot, particularly the generation of personalized itineraries. The llama3-groq-70b-8192-tool-use-preview model is utilized to handle user prompts and generate responses.

Here is an example of how the Groq API is used to generate an itinerary:

```bash
response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "system", "content": "You are a helpful travel assistant."},
              {"role": "user", "content": prompt}],
    max_tokens=1000,
)
itinerary = response.choices[0].message.content

```
2. Streamlit UI
The application interface is built using Streamlit, which allows rapid development of interactive web apps. The conversation state is maintained using st.session_state to track user inputs and bot responses across stages of the conversation.

3. Weather Data Integration
The OpenWeather API is used to fetch the current weather of the selected city. Here's how the weather data is fetched:

```bash
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
response = requests.get(url)

```
The data is then processed and displayed to the user, including temperature, humidity, and wind speed.

4. Login Functionality
To ensure secure access to the chatbot, a basic login page is provided. The credentials are hardcoded for simplicity, but in production, you would use a more secure method (e.g., OAuth or database authentication).

5. Neo4j Integration (Future Work)
While Neo4j is not directly integrated in the current code, it can be used to store user interactions, cities, itineraries, and preferences as graph data. Neo4j provides a powerful graph database that can be queried to offer personalized recommendations based on previous trips.

Example Neo4j usage:

```bash
# Connecting to Neo4j
from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
username = "neo4j"
password = "password"

driver = GraphDatabase.driver(uri, auth=(username, password))

# Example query
with driver.session() as session:
    result = session.run("MATCH (c:City) RETURN c.name")
    for record in result:
        print(record["c.name"])

```
6. Ollama Integration
Ollama can be used to generate text-based responses using natural language processing techniques. This is particularly useful for generating chat responses like trip itineraries.

## Example usage of Ollama for itinerary generation:

```bash
prompt = f"Generate a detailed itinerary for a trip to {city} with a budget of {budget}."
response = ollama.chat(prompt)
itinerary = response["message"]

```
### Prompting and Conversation Flow
The conversation is designed to be intuitive and follows a structured flow:

Login: Users must first log in with a username and password.
City Selection: The bot asks the user to select a city.
Budget: The bot prompts the user for their trip budget.
Preferences: The bot asks the user for their trip preferences (culture, food, etc.).
Starting Point: The user specifies the starting point for the itinerary.
Itinerary Generation: Using the gathered information, the bot generates a detailed itinerary.
Weather Information: Finally, the bot provides weather information for the selected city if requested.
