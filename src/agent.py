from langgraph.graph import StateGraph, END
from typing import TypedDict, List

from vector_store import LocalFileLoader
from langchain.chat_models import init_chat_model
from config import Config


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
    results = vector_db.retrieve(state["question"])
    docs = [doc.page_content for doc in results]
    return {**state, "retrieved_docs": docs}

# Generator node
def generator_node(state: RAGState):
    context = "\n\n".join(state["retrieved_docs"])
    prompt = f"Context:\n{context}\n\nQuestion: {state['question']}\nAnswer:"
    response = llm.invoke(prompt)
    return {**state, "answer": response}

# 4. Create LangGraph
builder = StateGraph(RAGState)

builder.add_node("planner", planner_node)
builder.add_node("retriever", retriever_node)
builder.add_node("generator", generator_node)

builder.set_entry_point("planner")
builder.add_edge("planner", "retriever")
builder.add_edge("retriever", "generator")
builder.add_edge("generator", END)

rag_graph = builder.compile()
