from langgraph.graph import StateGraph, END
from typing import TypedDict

from qa_agent.parser import parse_allure_results
from qa_agent.analyzer import classify_error
from qa_agent.llm import llm
import allure


# Определяем состояние графа
class AgentState(TypedDict):
    test_name: str
    status: str
    message: str
    classification: str
    recommendation: str


# === Узлы ===
def parse_node(state: AgentState) -> AgentState:
    results = parse_allure_results()
    if not results:
        return {**state, "status": "no_results"}
    first = results[0]  # пока возьмём один тест
    return {
        **state,
        "test_name": first["name"],
        "status": first["status"],
        "message": first["message"]
    }


def classify_node(state: AgentState) -> AgentState:
    error_type = classify_error(state.get("message", ""))
    return {**state, "classification": error_type}


def llm_node(state: AgentState) -> AgentState:
    prompt = (
        f"Тест '{state['test_name']}' упал со статусом {state['status']}.\n"
        f"Сообщение: {state['message']}\n"
        f"Тип ошибки: {state['classification']}\n\n"
        "Сгенерируй понятную рекомендацию для QA-инженера."
    )
    response = llm.invoke(prompt)
    return {**state, "recommendation": response.content}


def output_node(state: AgentState) -> AgentState:
    if state.get("recommendation"):
        allure.attach(
            state["recommendation"],
            name=f"AI Recommendation: {state['test_name']}",
            attachment_type=allure.attachment_type.TEXT
        )
    return state


# === Построение графа ===
def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("parse", parse_node)
    workflow.add_node("classify", classify_node)
    workflow.add_node("llm", llm_node)
    workflow.add_node("output", output_node)

    workflow.set_entry_point("parse")
    workflow.add_edge("parse", "classify")
    workflow.add_edge("classify", "llm")
    workflow.add_edge("llm", "output")
    workflow.add_edge("output", END)

    return workflow.compile()
