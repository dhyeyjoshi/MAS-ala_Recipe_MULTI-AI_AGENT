from crewai import Crew, Process
from agents import all_agents
from tasks import all_tasks
from dotenv import load_dotenv
load_dotenv()

import os
os.environ["API_KEY"] = os.getenv("API_KEY")

# Step 1: Get user input
print("\n🍽️ Welcome to the Smart Recipe Assistant! Please enter a few details.")
meal_type = input("What type of meal are you planning? (e.g., breakfast, lunch, dinner): ").strip()
dish_type = input("What type of dish do you want? (e.g., soup, curry, dessert): ").strip()
ingredients = input("List ingredients you have in your fridge (comma-separated): ").strip().split(',')
allergies = input("Any allergies? (comma-separated, or type 'none'): ").strip()

# Clean inputs
ingredients = [item.strip() for item in ingredients]
allergies = [] if allergies.lower() == 'none' else [item.strip() for item in allergies.split(',')]

# Store user preferences in shared memory
user_preferences = {
    "meal_type": meal_type,
    "dish_type": dish_type,
    "ingredients": ingredients,
    "allergies": allergies
}

import crewai_tools
crewai_tools.shared_memory = user_preferences

print(f"\n🚀 Generating recipe recommendations for your {meal_type} ({dish_type})...\n")

# Update task descriptions with formatted inputs
for task in all_tasks:
    task.description = task.description.format(**user_preferences)
    task.expected_output = task.expected_output.format(**user_preferences)

# Assemble the crew
recipe_recommendation_crew = Crew(
    agents=all_agents,
    tasks=all_tasks,
    process=Process.sequential,
    verbose=True,
    planning=True
)

if __name__ == "__main__":
    try:
        recipe_recommendation_crew.kickoff()
    except Exception as e:
        print(f"\n❌ Error encountered: {str(e)}")
