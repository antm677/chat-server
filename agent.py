import logging
import os
from typing import TypedDict
from langgraph.graph import StateGraph
from tools import Tools


class AgentState(TypedDict):
    user_input: str
    intents: dict
    results: dict
    final_output: list[dict]


def invoke_lang_graph(user_request: str):
    tools = Tools()

    def detect_intents(state: AgentState) -> AgentState:
        intents = tools.detect_intents(state['user_input'])
        state['intents'] = intents
        return state


    def search_tool(state: AgentState) -> AgentState:        
        if len(state['intents']) > 0:
            search_results = tools.search_tool(state['intents'])
            state['results'] = search_results
            
        return state


    def generate_output(state: AgentState) -> AgentState:
        try:
            file_path = os.path.join(os.path.dirname(__file__), "./prompts/generate_output.md")
            with open(file_path, "r", encoding="utf-8") as file:
                system_prompt = file.read()
        except:
            logging.warning("Prompt `generate_output` not found locally.")
            return state

        prompt = system_prompt.format(
            user_input=state["user_input"],
            supporting_information=state["results"],
        )
        response = tools.llm.invoke(prompt)

        state['final_output'] = {
            "message": response,
        }

        return state
    
    graph = StateGraph(AgentState)

    graph.set_entry_point("detect_intents")
    graph.add_node("detect_intents", detect_intents)
    graph.add_node("search_tool", search_tool)
    graph.add_node("generate_output", generate_output)

    graph.add_edge("detect_intents", "search_tool")
    graph.add_edge("search_tool", "generate_output")

    agent_app = graph.compile()

    results = agent_app.invoke({
        "user_input": user_request,
        "intents": [],
        "results": [],
        "final_output": "",
    })

    return results.get("final_output","")

