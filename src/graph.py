"""LangGraph implementation for AI Research Lab."""

import os
from typing import TypedDict, Optional
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from config.openai_config import get_llm
from .prompts import (
    HYPOTHESIS_PROMPT,
    RESEARCH_PROMPT,
    EXPERIMENT_PROMPT,
    REVIEWER_PROMPT,
    PAPER_GENERATOR_PROMPT,
)
from .tools import get_tools

load_dotenv()


class ResearchState(TypedDict):
    """State for the research workflow."""

    topic: str
    field: str
    hypothesis: Optional[str]
    literature: Optional[str]
    experiment: Optional[str]
    review: Optional[str]
    paper: Optional[str]
    current_step: str
    error: Optional[str]


class ResearchLabGraph:
    """LangGraph for AI Research Lab."""

    def __init__(self):
        self.llm = get_llm()
        self.tools = get_tools()
        self.memory = None
        self.graph = self._build_graph()
        self.executor = self.graph.compile(checkpointer=MemorySaver())

    def _call_llm(self, system_prompt: str, user_message: str) -> str:
        """Calls the LLM with system prompt and user message."""

        response = self.llm.invoke(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ]
        )
        return response.content

    # ===== NODES (AGENTS) =====

    def hypothesis_agent(self, state: ResearchState) -> dict:
        """Node 1: Generates a research hypothesis."""

        print("\n🔬 [Hypothesis Agent] Generating hypothesis...")

        prompt = HYPOTHESIS_PROMPT.format(
            field=state.get("field", "artificial intelligence"), topic=state["topic"]
        )

        result = self._call_llm(prompt, "")

        print(f"✅ Hypothesis generated.\n")

        return {"hypothesis": result, "current_step": "hypothesis"}

    def research_agent(self, state: ResearchState) -> dict:
        """Node 2: Searches for literature and data."""

        print("\n📚 [Research Agent] Searching for literature...")

        prompt = RESEARCH_PROMPT.format(hypothesis=state["hypothesis"])

        result = self._call_llm(prompt, "")

        print(f"✅ Literature review completed.\n")

        return {"literature": result, "current_step": "research"}

    def experiment_agent(self, state: ResearchState) -> dict:
        """Node 3: Analyzes existing research."""

        print("\n🧪 [Experiment Agent] Analyzing existing research...")

        prompt = EXPERIMENT_PROMPT.format(
            hypothesis=state["hypothesis"], literature=state["literature"]
        )

        result = self._call_llm(prompt, "")

        print(f"✅ Research analysis completed.\n")

        return {"experiment": result, "current_step": "experiment"}

    def reviewer_agent(self, state: ResearchState) -> dict:
        """Node 4: Reviews the research."""

        print("\n📝 [Reviewer Agent] Reviewing research...")

        prompt = REVIEWER_PROMPT.format(
            hypothesis=state["hypothesis"],
            literature=state["literature"],
            experiment=state["experiment"],
        )

        result = self._call_llm(prompt, "")

        print(f"✅ Review completed.\n")

        return {"review": result, "current_step": "review"}

    def paper_generator_agent(self, state: ResearchState) -> dict:
        """Node 5: Generates a research paper."""

        print("\n📄 [Paper Generator] Writing research paper...")

        prompt = PAPER_GENERATOR_PROMPT.format(
            topic=state["topic"],
            hypothesis=state["hypothesis"],
            literature=state["literature"],
            experiment=state["experiment"],
            review=state["review"],
        )

        result = self._call_llm(prompt, "")

        print(f"✅ Paper generated.\n")

        return {"paper": result, "current_step": "paper"}

    # ===== BUILD GRAPH =====

    def _build_graph(self) -> StateGraph:
        """Builds the LangGraph workflow."""

        workflow = StateGraph(ResearchState)

        workflow.add_node("hypothesis", self.hypothesis_agent)
        workflow.add_node("research", self.research_agent)
        workflow.add_node("experiment", self.experiment_agent)
        workflow.add_node("reviewer", self.reviewer_agent)
        workflow.add_node("paper", self.paper_generator_agent)

        workflow.set_entry_point("hypothesis")
        workflow.add_edge("hypothesis", "research")
        workflow.add_edge("research", "experiment")
        workflow.add_edge("experiment", "reviewer")
        workflow.add_edge("reviewer", "paper")
        workflow.add_edge("paper", END)

        return workflow

    # ===== RUN =====

    def run(
        self,
        topic: str,
        field: str = "artificial intelligence",
        thread_id: str = "research-lab-default",
    ) -> dict:
        """Runs the research workflow."""

        initial_state = ResearchState(
            topic=topic,
            field=field,
            hypothesis=None,
            literature=None,
            experiment=None,
            review=None,
            paper=None,
            current_step="start",
            error=None,
        )

        print("\n" + "=" * 60)
        print("🧠 AI RESEARCH LAB — Scientific Agent")
        print("=" * 60)
        print(f"📝 Topic: {topic}")
        print(f"🔬 Field: {field}")
        print(f"🆔 Session ID: {thread_id}")
        print("=" * 60 + "\n")

        config = {"configurable": {"thread_id": thread_id}}
        result = self.executor.invoke(initial_state, config=config)

        return result


def run_research_lab(
    topic: str, field: str = "artificial intelligence", thread_id: str = None
) -> str:
    """Convenience function to run the research lab."""

    lab = ResearchLabGraph()

    if thread_id is None:
        thread_id = "research-lab-default"

    result = lab.run(topic, field, thread_id=thread_id)

    return result.get("paper", "No paper generated.")
