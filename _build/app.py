from pprint import pformat
import pyodide.http
from shiny import App, reactive, render, ui

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
    async def data():
        response = await pyodide.http.pyfetch(url())
        dat = await response.json()
        return dat

    @output
    @render.text
    async def info():
        if input.selection() == "":
            return ""
        else:
            d=await data()
            data_str = pformat(d)
            return f"Request URL: {url()}\nResult type: {type(data())}\n{data_str}"

app = App(app_ui, server)

