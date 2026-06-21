"""
Day 26 - ReAct Agent
Wires calculator_tool, web_search_tool, and rag_tool into a single
LangChain ReAct agent that picks the right tool per query.
"""

from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_groq import ChatGroq

from tools.calculator_tool import calculator as calculate
from tools.web_search_tool import web_search
from tools.rag_tool import rag_search


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


TOOLS = [calculator, web_search_tool, rag_tool]

REACT_PROMPT = PromptTemplate.from_template("""
Answer the following question as best you can. You have access to the
following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")


def build_agent():
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    agent = create_react_agent(llm, TOOLS, REACT_PROMPT)
    return AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=6,
    )


if __name__ == "__main__":
    executor = build_agent()
    test_questions = [
        "What is 23 * 45?",
        "What is self-attention according to the paper?",
        "What's the latest news on LangChain agents?",
    ]
    for q in test_questions:
        print("\n" + "=" * 60)
        print("Q:", q)
        result = executor.invoke({"input": q})
        print("A:", result["output"])