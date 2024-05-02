import fitz
import gradio as gr
from dotenv import load_dotenv

load_dotenv(override=True)
from rag import RAG
from utils import format_page


def add_message(history, message):
    if message["files"] is not None and len(message["files"]) > 0:
        file_path = message["files"][0]
        history.append([file_path, ""])
    else:
        if message["text"] is not None:
            history.append((message["text"], None))

    return history


def bot(history, message, pdf_file_content):
    rag = RAG()
    if message["files"] is not None and len(message["files"]) > 0:
        file_path = message["files"][0]
        if file_path.endswith(".pdf"):
            with fitz.open(file_path) as doc:
                history[-1][1] = ""
                for page in doc:
                    cont, page_content = format_page(page)
                    if cont:
                        continue
                    pdf_file_content += "\n\n" + page_content
                    history[-1][1] += "\n\n" + page_content
                    yield history, gr.MultimodalTextbox(value=None, interactive=False), pdf_file_content
                rag.ingest_text(pdf_file_content)
    else:
        for answer in rag(message, stream=True):
            history[-1][1] = answer
            yield history, gr.MultimodalTextbox(value=None, interactive=False), pdf_file_content


with gr.Blocks() as demo:
    pdf_file_content = gr.State("")

    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False
    )

    chat_input = gr.MultimodalTextbox(interactive=True, file_types=[".pdf"], placeholder="Enter message or upload file...", show_label=False)

    chat_msg = chat_input.submit(add_message, [chatbot, chat_input], chatbot)
    bot_msg = chat_msg.then(bot, [chatbot, chat_input, pdf_file_content], [chatbot, chat_input, pdf_file_content], api_name="bot_response")
    bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])

demo.queue()
demo.launch()
