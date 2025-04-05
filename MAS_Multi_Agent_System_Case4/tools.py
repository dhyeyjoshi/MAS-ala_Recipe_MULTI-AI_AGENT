from phi.tools.googlesearch import GoogleSearch
from phi.tools.duckduckgo import DuckDuckGo
import crewai_tools
from langchain.tools import Tool
from urllib.parse import quote
from dotenv import load_dotenv
load_dotenv()

import os
os.environ["API_KEY"] = os.getenv("API_KEY")

# ✅ Wrap GoogleSearch in LangChain-compatible Tool
_google = GoogleSearch()
duckduckgo = DuckDuckGo()

google_search_tool = Tool(
    name="Google Search",
    func=lambda q: _google.google_search(q)["result"],
    description="Use Google Search to find food info, recipe inspiration, or diet suggestions."
)
duckduckgo_search_tool = Tool(
    name="DuckDuckGo Search",
    func=lambda query: duckduckgo.duckduckgo_search(query)["result"],
    description="Search the web using DuckDuckGo to find information about meals, recipes, or ingredients."
)

# ✅ Nutrition Filter Tool
def filter_ingredients(_: str = "") -> str:
    """Filter ingredients based on allergies provided by user input."""
    ingredients = crewai_tools.shared_memory.get("ingredients", [])
    allergies = crewai_tools.shared_memory.get("allergies", [])

    if not ingredients:
        return "No ingredients provided."

    if not allergies:
        return ", ".join(ingredients)

    # Strict filtering - preserve only safe ingredients
    safe_ingredients = [i for i in ingredients if i.lower() not in [a.lower() for a in allergies]]
    return ", ".join(safe_ingredients) if safe_ingredients else "No safe ingredients found after filtering."

nutrition_filter_tool = Tool(
    name="Nutrition Filter",
    func=filter_ingredients,
    description="Filters ingredients based on user allergies or dietary restrictions. Always respects user input."
)

# ✅ Recipe Generator Tool (Safe)
def generate_recipes(_: str = "") -> str:
    """Generates recipe steps using user-approved ingredients only."""
    ingredients = crewai_tools.shared_memory.get("ingredients", [])
    allergies = crewai_tools.shared_memory.get("allergies", [])
    dish_type = crewai_tools.shared_memory.get("dish_type", "")

    if not ingredients:
        return "No ingredients provided."

    # Simulated recipes (safe, not fetched externally)
    return (
        f"1. {dish_type.title()} Delight: Use {', '.join(ingredients)} in a balanced way...\n"
        f"2. Easy {dish_type.title()}: Toss {', '.join(ingredients[:3])} with herbs...\n"
        f"3. Classic {dish_type.title()}: Combine all ingredients and bake for 30 minutes."
    )

recipe_tool = Tool(
    name="Recipe Generator",
    func=generate_recipes,
    description="Suggests safe recipes using only user-provided ingredients. Never fetches external recipes that may violate restrictions."
)

# ✅ Recipe Formatter Tool
def format_recipes(data: str) -> str:
    """Format the recipes and attach a YouTube search link."""
    top_dish = data.splitlines()[0].split('.')[1].strip() if data else "healthy cooking tutorial"
    youtube_url = f"https://www.youtube.com/results?search_query={quote(top_dish)}"
    return f"🍽️ Formatted Recipes:\n{data}\n\n🎥 Related YouTube Tutorial: {youtube_url}"

presentation_tool = Tool(
    name="Recipe Formatter",
    func=format_recipes,
    description="Formats final recipe list and attaches a relevant YouTube search link. Does not alter recipes."
)