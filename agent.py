import streamlit as st
import requests
from groq import Groq

# Initialize Groq client
client = Groq(api_key="Your_api_key")
MODEL = "llama3-groq-70b-8192-tool-use-preview"

# Predefined login credentials (Replace with a more secure authentication method in production)
VALID_USERNAME = ""
VALID_PASSWORD = ""

# Fetch weather data function
def fetch_weather(city):
    OPENWEATHER_API_KEY = "Your_api_key"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "weather": data["weather"][0]["description"].capitalize(),
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
            }
        else:
            return {"error": response.json().get("message", "Unknown error")}
    except Exception as e:
        return {"error": str(e)}

# Login Function
def login():
    st.title("🔐 Login to Trip Planner Chatbot")
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")
    if st.button("Login"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.success("✅ Login successful!")
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("🚫 Invalid username or password. Please try again.")

# Streamlit app
def main():
    st.set_page_config(page_title="Trip Planner Bot 🗺️", page_icon="🧳")

    # Ensure user is logged in
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()
        return  # Exit the main function until logged in

    # Title and chatbot initialization
    st.title("🗺️ Dynamic Trip Planner Chatbot")

    # Conversation history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_stage" not in st.session_state:
        st.write("Which city you want to visit?")
        st.session_state.conversation_stage = "ask_city"

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").markdown(f"👤 **You**: {message['content']}")
        else:
            st.chat_message("assistant").markdown(f"🤖 **Bot**: {message['content']}")

    # User input
    user_input = st.chat_input("💬 Type your message here...")

    # Conversation logic
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Conversation stages
        if st.session_state.conversation_stage == "ask_city":
            
            city = user_input
            st.session_state.city = city
            bot_response = f"🌆 Great choice! What is your budget for visiting **{city}**? 💰"
            st.session_state.conversation_stage = "ask_budget"

        elif st.session_state.conversation_stage == "ask_budget":
            budget = float(user_input) if user_input.isdigit() else 100
            st.session_state.budget = budget
            bot_response = "🎯 Got it! What's your main preference for this trip? 🏞️ (e.g., culture, food, adventure)"
            st.session_state.conversation_stage = "ask_preferences"

        elif st.session_state.conversation_stage == "ask_preferences":
            preferences = user_input
            st.session_state.preferences = preferences
            bot_response = "🚆 Understood! What is your starting point for the itinerary? 🛤️"
            st.session_state.conversation_stage = "ask_starting_point"

        elif st.session_state.conversation_stage == "ask_starting_point":
            starting_point = user_input
            st.session_state.starting_point = starting_point

            prompt = (
                f"Generate a detailed one-day itinerary for visiting {st.session_state.city}. "
                f"The user has a budget of {st.session_state.budget} rupees and prefers {st.session_state.preferences}. "
                f"The starting point is {starting_point}. Provide the itinerary and total estimated cost."
            )

            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "system", "content": "You are a helpful travel assistant."},
                          {"role": "user", "content": prompt}],
                max_tokens=1000,
            )
            itinerary = response.choices[0].message.content
            st.session_state.itinerary = itinerary

            bot_response = f"📋 Here's your detailed itinerary:\n\n{itinerary} 🗓️"
            st.session_state.conversation_stage = "ask_weather"

        elif st.session_state.conversation_stage == "ask_weather":
            bot_response = "🌤️ Would you like to know the current weather for this city? (Yes/No)"
            st.session_state.conversation_stage = "weather_query"

        elif st.session_state.conversation_stage == "weather_query":
            if "yes" in user_input.lower():
                weather = fetch_weather(st.session_state.city)
                if "error" in weather:
                    bot_response = f"⚠️ Sorry, I couldn't fetch the weather data. Error: {weather['error']}"
                else:
                    bot_response = (
                        f"🌡️ The current weather in **{st.session_state.city}** is:\n"
                        f"- **{weather['weather']}**\n"
                        f"- Temperature: **{weather['temperature']}°C** (Feels like {weather['feels_like']}°C)\n"
                        f"- Humidity: **{weather['humidity']}%**\n"
                        f"- Wind Speed: **{weather['wind_speed']} m/s** 💨"
                    )
            else:
                bot_response = "👍 Alright! Let me know if there's anything else you'd like help with."

        st.session_state.messages.append({"role": "bot", "content": bot_response})
        st.rerun()

if __name__ == "__main__":
    main()
