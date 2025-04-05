from crewai import Agent
from tools import google_search_tool, nutrition_filter_tool, recipe_tool, presentation_tool, duckduckgo_search_tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
os.environ['API_KEY'] = os.getenv('API_KEY')
print("Loaded Google API Key:", os.getenv("API_KEY"))

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("API_KEY")
)

# 🧠 Web Analyzer Agent
web_analyzer_agent = Agent(
    role="Web Analyzer",
    goal="Analyze user preferences and enrich with relevant food and ingredient info from trusted sources.",
    backstory="Expert in understanding user context like meal type, dish preferences, and ingredient usage.",
    tools=[google_search_tool,duckduckgo_search_tool],
    llm=llm,
    verbose=True,    
    allow_delegation=True
)

# 🥗 Nutritionist Agent
nutritionist_agent = Agent(
    role="Nutritionist",
    goal="Filter ingredients based on user input and suggest safe options. Must strictly follow user constraints.",
    backstory="Certified AI dietitian that always prioritizes user input (e.g., allergies, dislikes) when giving advice.",
    tools=[nutrition_filter_tool,google_search_tool, duckduckgo_search_tool],
    llm=llm,
    verbose=True,
    allow_delegation=True
)

# 👨‍🍳 Chef Agent
chef_agent = Agent(
    role="Chef",
    goal="Generate 3 creative, healthy recipes based strictly on safe ingredients provided by the nutritionist.",
    backstory="AI-based culinary expert. Never adds or changes ingredients beyond what the user approved.",
    tools=[recipe_tool,google_search_tool, duckduckgo_search_tool],
    llm=llm,
    verbose=True,
    allow_delegation=True
)

# 🎁 Presenter Agent
presenter_agent = Agent(
    role="Presenter",
    goal="Format recipes into a beautiful, easy-to-follow output with related tutorial links.",
    backstory="A formatting specialist AI who makes content look great without changing the recipe logic.",
    tools=[presentation_tool, google_search_tool , duckduckgo_search_tool],
    llm=llm,
    verbose=True,
    allow_delegation=True
)

all_agents = [web_analyzer_agent, nutritionist_agent, chef_agent, presenter_agent]
