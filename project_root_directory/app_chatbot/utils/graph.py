from pprint import pprint
from typing import List

from langchain_core.documents import Document
from typing_extensions import TypedDict

from langgraph.graph import END, StateGraph
from .nodes.node_web_search import web_search
from .nodes.node_generate import generate
from .nodes.node_grade_documents import grade_documents
from .nodes.node_retrieve import retrieve
from .conditionals.conditional_route_question import route_question
from .conditionals.conditional_generate import decide_to_generate
from .conditionals.conditional_grader import grade_generation_v_documents_and_question


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents
    """

    question: str
    generation: str
    web_search: str
    documents: List[str]


workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("websearch", web_search)  # web search
workflow.add_node("retrieve", retrieve)  # retrieve
workflow.add_node("grade_documents", grade_documents)  # grade documents
workflow.add_node("generate", generate)  # generatae


# Build graph
workflow.set_conditional_entry_point(
    route_question,
    {
        "websearch": "websearch",
        "vectorstore": "retrieve",
    },
)

workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "websearch": "websearch",
        "generate": "generate",
    },
)
workflow.add_edge("websearch", "generate")
workflow.add_conditional_edges(
    "generate",
    grade_generation_v_documents_and_question,
    {
        "not supported": "generate",
        "useful": END,
        "not useful": "websearch",
    },
)

# Compile
rag_app = workflow.compile()


def respond(question: str) -> Document:
    inputs = {"question": question}
    print(f"Question: {question}")
    for output in rag_app.stream(inputs):
        for key, value in output.items():
            pprint(f"Finished running: {key}:")
    return value['generation']
