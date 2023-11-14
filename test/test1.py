#!/usr/bin/env python
# coding: utf-8

# In[3]:

from pprint import pformat
import pyodide_http
from shiny import App, reactive, render, ui
import requests
pyodide_http.patch_all()

app_ui = ui.page_fluid(
    ui.input_selectize(
        "city",
        "Select a city:",
        [
            "",
            "Berlin",
            "Cairo",
            "Chicago",
            "Kyiv",
            "London",
            "Lima",
            "Los Angeles",
            "Mexico City",
            "Mumbai",
            "New York",
            "Paris",
            "São Paulo",
            "Seoul",
            "Shanghai",
            "Taipei",
            "Tokyo",
        ],
    ),
    ui.input_radio_buttons(
        "data_type",
        "Data conversion type",
        {
            "json": "Parse JSON and return dict/list",
            "string": "String",
            "bytes": "Byte object",
        },
    ),
    ui.output_text_verbatim("info"),
)


def server(input, output, session):
    # Weather data API: https://github.com/robertoduessmann/weather-api
    @reactive.Calc
    def url():
        return f"https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/donnees-synop-essentielles-omm/records/{input.city()}"

    @reactive.Calc
    async def weather_data():
        if input.city() == "":
            return

        response = requests.get(url())
        #if response.status != 200:
            #raise Exception(f"Error fetching {url()}: {response.status}")

        if input.data_type() == "json":
            # .json() parses the response as JSON and converts to dictionary.
            data = response.json()
        elif input.data_type() == "string":
            # .string() returns the response as a string.
            data = await response.string()
        else:
            # .bytes() returns the response as a byte object.
            data = await response.bytes()

        return data

    @output
    @render.text
    async def info():
        if input.city() == "":
            return ""

        data = await weather_data()
        if isinstance(data, (str, bytes)):
            data_str = data
        else:
            data_str = pformat(data)
        return f"Request URL: {url()}\nResult type: {type(data)}\n{data_str}"


app = App(app_ui, server)


# In[4]:


app


# In[ ]:




