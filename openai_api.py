# -*- coding: utf-8 -*-
# !/usr/bin/env python

import gradio as gr
import openai
import os

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

message_history = []


def get_completion(prompt: str, role: str = "user", model="gpt-3.5-turbo"):
    global message_history
    message_history.append({"role": role, "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=message_history,
        temperature=0.2,  # The degree of randomness of
    )
    reply_content = completion.choices[0].message["content"]
    print(reply_content)
    message_history.append({"role": "assistant", "content": reply_content})
    response = [(message_history[i]["content"], message_history[i + 1]["content"]) for i in
                range(0, len(message_history), 2)]
    return response


user_input = ""

prompt = f"""
Answer the question or the request inside the following text: 
{user_input} .
Answer it like a professional customer service employee .
"""


with gr.Blocks() as block:
    chatbot = gr.Chatbot()
    txt = gr.Textbox(show_label=True, placeholder="Type your message here").style(container=False)
    txt.submit(get_completion, txt, chatbot)
    txt.submit(None, None, txt, _js="() => {' '}")


block.launch()
