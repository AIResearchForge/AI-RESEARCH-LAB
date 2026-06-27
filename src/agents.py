"""LangChain agent definitions for Business Analyst (LangChain 1.2.18)."""

import os
from typing import List, Optional

from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from .prompts import (
    AGENT_1_BUSINESS_PLANNER_PROMPT,
    AGENT_2_MARKET_ANALYST_PROMPT,
    AGENT_3_COMPETITOR_ANALYST_PROMPT,
    AGENT_4_FINANCE_ANALYST_PROMPT,
)
from .tools import get_tools

load_dotenv()


def get_llm(model_name: Optional[str] = None) -> ChatOpenAI:
    """Returns an LLM instance (OpenAI)."""
    if model_name is None:
        model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
    return ChatOpenAI(
        model=model_name,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        temperature=0.1,
        max_tokens=4096,
    )


def create_agent(
    system_prompt: str,
    tools: List = None,
    memory=None,
    model_name: Optional[str] = None,
) -> AgentExecutor:
    """Creates a LangChain agent."""

    if tools is None:
        tools = []

    llm = get_llm(model_name)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True,
    )


def create_business_planner_agent(model_name: Optional[str] = None) -> AgentExecutor:
    """Agent 1: Business Planner."""
    return create_agent(
        AGENT_1_BUSINESS_PLANNER_PROMPT, tools=[], model_name=model_name
    )


def create_market_analyst_agent(model_name: Optional[str] = None) -> AgentExecutor:
    """Agent 2: Market Analyst."""
    tools = get_tools()
    return create_agent(
        AGENT_2_MARKET_ANALYST_PROMPT, tools=tools, model_name=model_name
    )


def create_competitor_analyst_agent(model_name: Optional[str] = None) -> AgentExecutor:
    """Agent 3: Competitor Analyst."""
    tools = get_tools()
    return create_agent(
        AGENT_3_COMPETITOR_ANALYST_PROMPT, tools=tools, model_name=model_name
    )


def create_finance_analyst_agent(
    model_name: Optional[str] = None,
    memory=None,
) -> AgentExecutor:
    """Agent 4: Finance & Risk Analyst."""
    return create_agent(
        AGENT_4_FINANCE_ANALYST_PROMPT, tools=[], memory=memory, model_name=model_name
    )


__all__ = [
    "get_llm",
    "create_business_planner_agent",
    "create_market_analyst_agent",
    "create_competitor_analyst_agent",
    "create_finance_analyst_agent",
]
