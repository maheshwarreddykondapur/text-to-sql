from pydantic import ValidationError
import pandas as pd
import plotly.express as px

from response_structures.visualizations import PlotlyFigureParameters, ChartTypes

# Function to generate Plotly figures dynamically
def generate_plotly_chart(gpt_response: dict, data_frame: pd.DataFrame):
    # Validate the GPT response using the Pydantic model
    try:
        figure_data = PlotlyFigureParameters(**gpt_response.__dict__)
    except ValidationError as e:
        return None

    # Retrieve the chart type and parameters
    chart_type = figure_data.chart_type
    params = figure_data.parameters.__dict__

    # Map chart type to Plotly function
    if chart_type == ChartTypes.scatter:
        fig = px.scatter(data_frame, **params)
    elif chart_type == ChartTypes.bar:
        fig = px.bar(data_frame, **params)
    elif chart_type == ChartTypes.box:
        fig = px.box(data_frame, **params)
    elif chart_type == ChartTypes.histogram:
        fig = px.histogram(data_frame, **params)
    elif chart_type == ChartTypes.line:
        fig = px.line(data_frame, **params)
    elif chart_type == ChartTypes.pie:
        fig = px.pie(data_frame, **params)
    else:
        return None
    
    return fig