from crewai import Crew, Process
from agents import all_agents
from tasks import all_tasks
from dotenv import load_dotenv
from pathlib import Path
import json
import os
import re
import crewai_tools
from langchain.callbacks import StdOutCallbackHandler
from langchain.callbacks.tracers.run_collector import RunCollectorCallbackHandler
from urllib.parse import quote

tracer = RunCollectorCallbackHandler()
handler = StdOutCallbackHandler()

load_dotenv()


import os
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')    
    
# Step 1: Get user input
print("\n🍽 Welcome to the Smart Recipe Assistant! Please enter a few details.")
meal_type = input("What type of meal are you planning? (e.g., breakfast, lunch, dinner): ").strip()
dish_type = input("What type of dish do you want? (e.g., soup, curry, dessert): ").strip()
ingredients = input("List ingredients you have in your fridge (comma-separated): ").strip().split(',')
allergies = input("Any allergies? (comma-separated, or type 'none'): ").strip()
dietary_restriction = input("Any dietary restriction? (e.g., vegan, keto, gluten-free, none): ").strip()

# Clean inputs
ingredients = [item.strip() for item in ingredients]
allergies = [] if allergies.lower() == 'none' else [item.strip() for item in allergies.split(',')]
dietary_restriction = dietary_restriction if dietary_restriction else "none"

# Store user preferences in shared memory
user_preferences = {
    "meal_type": meal_type,
    "dish_type": dish_type,
    "ingredients": ingredients,
    "allergies": allergies,
    "dietary_restriction": dietary_restriction
}

# Optional: share with tools
import crewai_tools
crewai_tools.shared_memory = user_preferences

print(f"\n🚀 Generating recipe recommendations for your {meal_type} ({dish_type})...\n")

# Format task descriptions using user input
for task in all_tasks:
    task.description = task.description.format(**user_preferences)
    if hasattr(task, "expected_output") and task.expected_output:
        task.expected_output = task.expected_output.format(**user_preferences)

# Assemble the crew
recipe_recommendation_crew = Crew(
    agents=all_agents,
    tasks=all_tasks,
    process=Process.sequential,
    verbose=True,
    planning=True
)

# === MAIN EXECUTION ===
if __name__ == "__main__":
    try:
        # Run the crew and capture the result
        result = recipe_recommendation_crew.kickoff()

        # Handle result format (Pydantic, dict, or string)
        if hasattr(result, "dict"):
            json_data = result.dict()
        elif isinstance(result, str):
    # Remove json ...  if present
            cleaned = re.sub(r"^json|$", "", result.strip(), flags=re.IGNORECASE).strip()
            try:
                json_data = json.loads(cleaned)
            except json.JSONDecodeError:
                json_data = {"result": cleaned}
        else:
            json_data = result

        # Save result to JSON file
        output_path = Path("output.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Output saved to {output_path.resolve()}\n")
        def generate_image_urls_from_recipes(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                recipes = data.get("recipes", [])
                if not recipes:
                    print("❗ No recipes found in the JSON.")
                    return

                print("\n🖼️ Generating Pollinations image prompts...\n")
                for recipe in recipes:
                    title = recipe.get("title", "")
                    if title:
                        prompt = f"high-quality photo of {title}, plated on a table, cinematic lighting"
                        encoded_prompt = quote(prompt)
                        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
                        print(f"🍲 {title} → {url}")
                        # Optional: you can save this to recipe['image_url'] or a file
            except Exception as e:
                print(f"❌ Failed to generate image URLs: {e}")

        # Call the function after saving output.json
        generate_image_urls_from_recipes(output_path)
        
    except Exception as e:
        print(f"\n❌ Error encountered: {str(e)}")