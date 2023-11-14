#!/usr/bin/env python
# coding: utf-8

# In[9]:


from pprint import pformat
import pyodide_http
from shiny import App, reactive, render, ui
import requests
pyodide_http.patch_all()

app_ui = ui.page_fluid(
    ui.input_selectize(
        "selection",
        "choisir selection",
        [
            "pres","nom"
        ],
    ),
    ui.output_text_verbatim("info"),
)

def server(input, output, session):
    @reactive.Calc
    def url():
        return f"https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/donnees-synop-essentielles-omm/records?select={input.selection()}"

    @reactive.Calc
    def data():
        response = requests.get(url()).json()
        return response

    @output
    @render.text
    async def info():
        if input.selection() == "":
            return ""
        else:
            data_str = pformat(data())
            return f"Request URL: {url()}\nResult type: {type(data())}\n{data_str}"

app = App(app_ui, server)
