# Pywebio
from pywebio.output import *
from pywebio.input import *
from pywebio.session import *
from pywebio.platform import *

# Other
import sys as s
from typing import Tuple, List

# Plotting libraries
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

from first_page import first_page
from dashboard import discussion_dashboard

CSS = """
    * {margin: 0; padding: 0; font-family: "Roboto", sans-serif; font-size: 18px; text-align: left; }
    """

def main():
    config(css_style=CSS)
    first_page()

if __name__ == '__main__':
    start_server(main, port=8157)  # Use a single port
