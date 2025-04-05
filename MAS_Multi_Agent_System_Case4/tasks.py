from crewai import Task
from agents import web_analyzer_agent, nutritionist_agent, chef_agent, presenter_agent
from dotenv import load_dotenv
from tools import google_search_tool, nutrition_filter_tool, recipe_tool, presentation_tool, duckduckgo_search_tool

load_dotenv()

import os
os.environ["API_KEY"] = os.getenv("API_KEY")

task1 = Task(
    description="Analyze user preferences like {meal_type}, {dish_type}, and ingredients: {ingredients}.",
    expected_output="Detailed context for nutrition filtering.",
    tools=[google_search_tool, duckduckgo_search_tool],
    agent=web_analyzer_agent
)

task2 = Task(
    description="Filter ingredients: {ingredients}, by removing allergens: {allergies}.",
    expected_output="Safe and suitable ingredient list for recipe creation.",
    tools=[nutrition_filter_tool,google_search_tool, duckduckgo_search_tool],
    agent=nutritionist_agent
)

task3 = Task(
    description="Generate top 3 recipes based on cleaned ingredients and dish type: {dish_type}.",
    expected_output="Step-by-step instructions for 3 recipes.",
    tools=[recipe_tool,google_search_tool, duckduckgo_search_tool ],
    agent=chef_agent
)

task4 = Task(
    description="Format recipes nicely and provide tutorial YouTube links for each if available.",
    expected_output="A clean, final document of 3 recipes with links.",
    tools=[presentation_tool,google_search_tool, duckduckgo_search_tool ],
    agent=presenter_agent
)

all_tasks = [task1, task2, task3, task4]
