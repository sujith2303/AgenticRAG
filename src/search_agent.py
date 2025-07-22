from langgraph.graph import StateGraph, END
from typing import TypedDict, List

from vector_store import LocalFileLoader
from langchain.chat_models import init_chat_model
from config import Config
from Tools import Search

model_name = Config.MODEL
vector_db = LocalFileLoader()
llm = init_chat_model(model_name, model_provider="google_genai")

class RAGState(TypedDict):
    question: str
    retrieved_docs: List[str]
    answer: str

# 3. Define nodes

# Planner node
def planner_node(state: RAGState):
    print("Planning...")
    return state  

# Retriever node
def retriever_node(state: RAGState):
    print("Retrieving")
    SIMILARITY_THRESHOLD = 0.75
    results = vector_db.retrieve(state["question"])
    filtered = [
        doc.page_content for doc, score in results if score < SIMILARITY_THRESHOLD
    ]
    if not filtered:
        print("Context not found")
        return {**state,"retrieved_docs":None}
    return {**state, "retrieved_docs": filtered}

# Generator node
def generator_node(state: RAGState):
    print("Generating")
    context = "\n\n".join(state["retrieved_docs"])
    prompt = f"Context:\n{context}\n\nQuestion: {state['question']}\nAnswer:"
    response = llm.invoke(prompt)
    return {**state, "answer": response}

def search_node(state: RAGState):
    print("No context found in DB, searching the web...")
    results = Search(state["question"])
    docs = [res['content'] for res in results]
    return {**state, "retrieved_docs": docs}

def route_after_retriever(state: RAGState):
    print("Routing")
    if state["retrieved_docs"]:
        return "generator"
    else:
        return "search"

# 4. Create LangGraph
builder = StateGraph(RAGState)

builder.add_node("planner", planner_node)
builder.add_node("retriever", retriever_node)
builder.add_node("generator", generator_node)
builder.add_node("search", search_node)

builder.set_entry_point("planner")
builder.add_edge("planner", "retriever")
builder.add_conditional_edges(
    "retriever",
    route_after_retriever,
    {
        "generator": "generator",
        "search": "search"
    }
)
builder.add_edge("search", "generator")
builder.add_edge("generator", END)

rag_graph = builder.compile()
