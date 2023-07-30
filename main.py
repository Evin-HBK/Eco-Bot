import textbase
from textbase.message import Message
from textbase import models
import os
import random
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "YOUR_API_KEY"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Context prompt for GPT-3.5 Turbo for Green Energy Advisor
GREEN_ENERGY_PROMPT = """You are chatting with a Green Energy Advisor. Ask anything related to adopting renewable energy solutions at home, and I'll provide personalized guidance to help you go green!
"""

# Context prompt for GPT-3.5 Turbo for Cleanup Organizer/Advicer
CLEANUP_PROMPT = """You are chatting with the Environmental Cleanup Organizer. Feel free to ask about organizing cleanup events, connecting with others interested in environmental conservation, or any other related topics!
"""

# Sample data for existing events(Replace this with data from an actual db)
cleanup_events = {
    1: {
        "title": "Beach Cleanup",
        "date": "10/08/2023",
        "location": "Beachfront Park",
        "description": "Join us for a beach cleanup event to keep our shores clean and protect marine life.",
    },
    2: {
        "title": "Community Park Cleanup",
        "date": "15/08/2023",
        "location": "Community Park",
        "description": "Help us tidy up the park and create a cleaner environment for everyone to enjoy.",
    },
    3: {
        "title": "River Cleanup",
        "date": "20/08/2023",
        "location": "Riverside Park",
        "description": "Let's work together to remove litter from the riverbank and promote a healthy aquatic ecosystem.",
    },
    4: {
        "title": "Lake Cleanup",
        "date": "25/08/2023",
        "location": "Lakeview Park",
        "description": "Participate in the cleanup of the lake area and preserve the beauty of our local water bodies.",
    },
    5: {
        "title": "Forest Cleanup",
        "date": "01/09/2023",
        "location": "Greenwood Forest",
        "description": "Contribute to the conservation of the forest by removing trash and maintaining its natural habitat.",
    }
}

@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """

    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1

    # Get the user's last message
    user_message = message_history[-1].content.lower()

    # Default response when user says usual greeting message like hello
    if "hello" in user_message or "hi" in user_message or "hey" in user_message:
        bot_response = "Hello! I'm your friendly AI chatbot. I can help you with two main things:\n\n1. Green Energy Advisor: I can provide tips on adopting renewable energy solutions at home.\n2. Environmental Cleanup Organizer: I can help you join existing cleanup events or organize new ones.\n\nFeel free to ask me anything related to these topics!"
        return bot_response, state

    # This displays a random event from the list of events (from the data given above)
    elif "join" in user_message or "existing event" in user_message or "be part of" in user_message:
        # Get the event IDs
        event_ids = list(cleanup_events.keys())

        # Select a random event
        event_id = random.choice(event_ids)

        # Get the event details
        event_details = cleanup_events[event_id]
        title = event_details["title"]
        date = event_details["date"]
        location = event_details["location"]
        description = event_details["description"]

        bot_response = f"Sure, here's an existing cleanup event you can join:\n\nTitle: {title}\nDate: {date}\nLocation: {location}\nDescription: {description}"

    # This provides tip if the user wants to host a new event for cleanup
    elif "organize" in user_message or "new event" in user_message or "create" in user_message or "host" in user_message or "organise" in user_message or "announce" in user_message:
        bot_response = models.OpenAI.generate(
            system_prompt=CLEANUP_PROMPT,
            message_history=message_history,
            model="gpt-3.5-turbo",
        )

    # This provides tips for user regarding anything related to green energy/ sustainability
    elif "energy" in user_message or "green" in user_message or "conservative" in user_message or "conservation" in user_message or "sustainable" in user_message or "solar" in user_message or "clean" in user_message or "eco-friendly" in user_message or "efficient" in user_message or "reduce" in user_message or "reduction" in user_message or "efficiency" in user_message:
        bot_response = models.OpenAI.generate(
            system_prompt=GREEN_ENERGY_PROMPT,
            message_history=message_history,
            model="gpt-3.5-turbo",
        )

        # increase readability because ui doesn't show newline
        bot_response = bot_response.replace("\n", "\n- ")
        bot_response = "- " + bot_response

    # Shows all events(events provided above)
    elif "all events" in user_message or "list events" in user_message or "available events" in user_message:
        event_list = "\n\n".join([f"Title: {event['title']}\nDate: {event['date']}\nLocation: {event['location']}\nDescription: {event['description']}" for event in cleanup_events.values()])
        bot_response = f"Sure, here are all the available cleanup events:\n\n{event_list}"

    #default response given when user asks for random stuff like jokes or quotes, it will automatically be regarding sustainability
    else:
        bot_response = models.OpenAI.generate(
            system_prompt=GREEN_ENERGY_PROMPT,
            message_history=message_history,
            model="gpt-3.5-turbo",
        )

    return bot_response, state

if __name__ == "__main__":
    # Start the UI
    textbase.start_ui("talking-bot")
