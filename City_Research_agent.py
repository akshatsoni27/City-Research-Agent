from dotenv import load_dotenv
load_dotenv()

import os 
import requests

from langchain_groq import ChatGroq
from langchain.tools import tool
from tavily import TavilyClient
from langchain.agents import create_agent

#tools from here

# weather tool 
@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
    
    response = requests.get(url)
    data = response.json()
    
    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"
    
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    
    return f"Weather in {city}: {desc}, {temp}°C"

#Tavily news tool
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_news(city : str) -> str:
    """Get latest news about the city"""
    response = tavily_client.search(
        query = f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}."

    news_list = []

    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")

        news_list.append(
            f" -{title}\n {url}\n {snippet[:100]}..."
        )

    return f"Latest news in {city}:\n" + "\n".join(news_list)

llm = ChatGroq(model="openai/gpt-oss-120b")

tools ={
    "get_weather": get_weather,
    "get_news": get_news
}

llm_with_tools = llm.bind_tools([get_weather, get_news])

agent = create_agent(
    llm,
    tools = [get_weather, get_news],
    system_prompt = "You are a helpful city assistant."
)

def run_city_agent(message: str) -> str:
    """Run the city assistant and return its final response text."""
    result = agent.invoke({"messages": [{"role": "user", "content": message}]})
    final_message = result["messages"][-1].content

    if isinstance(final_message, list):
        return "\n".join(
            part.get("text", "") for part in final_message if isinstance(part, dict)
        ).strip()

    return str(final_message)


if __name__ == "__main__":
    print("City Agent | Type 'Exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting City Agent. Goodbye!")
            break
        print(run_city_agent(user_input))