import gradio as gr
from search_agent import rag_graph
import os
from config import Config


os.environ["LANGSMITH_TRACING"] = Config.LANGSMITH_TRACING
if Config.LANGSMITH_API_KEY =="true":
    os.environ["LANGSMITH_API_KEY"] = Config.LANGSMITH_API_KEY
    os.environ["LANGSMITH_PROJECT"] = Config.LANGSMITH_PROJECT

def history_to_message(history):
    content = ""
    for i in history:
        if i['role']=='user':
            content+="User: " + i['content'] +"\n"
        elif i['role']=='assistant':
            content+= "assistant: " + i['content'] + '\n'
    return content


def process_input(message , history):
    history = history_to_message(history[-1:])
    message += history
    response = rag_graph.invoke({"question":message})
    return response['answer'].content

# def handle_file(file):
#     vector_db = LocalFileLoader()
#     vector_db.load()


demo = gr.ChatInterface(
    process_input,
    type="messages",
    chatbot=gr.Chatbot(),
    textbox=gr.Textbox(placeholder="Ask any question", container=False, scale=7),
    title="RAG ChatBot",
    description="Let's Chat",
    theme="ocean",
    examples=["What is Machine Learning", "What is 2+2?", "What is RAG?"],
    cache_examples=False,
)


if __name__ =="__main__":
    demo.launch(debug = True)


