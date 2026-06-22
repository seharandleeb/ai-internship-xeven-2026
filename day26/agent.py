"""
Day 26/27 - Tool-calling agent (faster + more reliable than text-based ReAct).
Wires calculator_tool, web_search_tool, rag_tool, and weather_tool into a
single LangChain agent using native tool calling.
"""

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_groq import ChatGroq

from tools.calculator_tool import calculator as calculate
from tools.web_search_tool import web_search
from tools.rag_tool import rag_search
from tools.weather_tool import weather as weather_lookup


@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression, e.g. 23 * 45. Input must be the raw
    expression with no quotes around it."""
    return str(calculate.invoke(expression))


@tool
def web_search_tool(query: str) -> str:
    """Search the live web for current information or news."""
    return str(web_search.invoke(query))


@tool
def rag_tool(query: str) -> str:
    """Search the ingested arXiv papers (RAG index) for grounded answers."""
    return str(rag_search.invoke(query))


@tool
def weather_tool(city: str) -> str:
    """Get the current weather for a city. Input should be a city name."""
    return str(weather_lookup.invoke(city))


TOOLS = [calculator, web_search_tool, rag_tool, weather_tool]

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful, friendly chatbot. Talk naturally like a normal "
     "assistant — never describe your own internal tools, rules, mistakes, "
     "or reasoning process. Just give the final answer."
     "\n\n"
     "If the user's message contains a section marked "
     "'--- DOCUMENT CONTENT START ---' / '--- DOCUMENT CONTENT END ---', "
     "or '--- RELEVANT EXCERPTS START ---' / '--- RELEVANT EXCERPTS END ---', "
     "a document has been uploaded and relevant text is included in the "
     "message. Answer entirely from that content, don't use a tool."
     "\n\n"
     "Tool usage:\n"
     "- calculator: for math expressions only\n"
     "- weather_tool: for any question about current weather in a city\n"
     "- rag_tool: for questions about the ingested arXiv research paper\n"
     "- web_search_tool: for current events, news, or anything you don't "
     "already know confidently\n"
     "For anything else (general knowledge, definitions, explanations), "
     "answer directly without using a tool.\n\n"
     "If a user says something unclear like 'I don't understand', look "
     "at the recent conversation and clarify your previous answer."),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])


def build_agent():
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    agent = create_tool_calling_agent(llm, TOOLS, PROMPT)
    return AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=4,
    )


if __name__ == "__main__":
    executor = build_agent()
    test_questions = [
        "What is AI?",
        "What is 23 * 45?",
        "What is self-attention according to the paper?",
        "What's the latest news on LangChain agents?",
        "What's the weather in Lahore right now?",
    ]
    for q in test_questions:
        print("\n" + "=" * 60)
        print("Q:", q)
        result = executor.invoke({"input": q})
        print("A:", result["output"])