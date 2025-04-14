from pydantic import BaseModel, Field
from typing import Optional, Union
from enum import Enum

class ChartTypes(Enum):
    bar = "bar"
    scatter = "scatter"
    box = "box"
    histogram = "histogram"
    line = "line"
    pie = "pie"

# Parameters for a bar chart
class BarChartParameters(BaseModel):
    x: str = Field(..., description="Column name for the x-axis data.")
    y: str = Field(..., description="Column name for the y-axis data.")
    barmode: str = Field(..., description="Arrangement of bars. Options: group, stack, overlay.")

# Parameters for a scatter plot
class ScatterChartParameters(BaseModel):
    x: str = Field(..., description="Column name for the x-axis data.")
    y: str = Field(..., description="Column name for the y-axis data.")
    color: Optional[str] = Field(None, description="Column name for grouping (color).")
    symbol: Optional[str] = Field(None, description="Column name to define marker symbol.")

# Parameters for a box plot
class BoxChartParameters(BaseModel):
    x: Optional[str] = Field(None, description="Optional column name for grouping data.")
    y: str = Field(..., description="Numeric column name to visualize as a box plot.")
    
# Parameters for a histogram
class HistogramParameters(BaseModel):
    x: str = Field(..., description="Column name for the histogram data.")
    nbins: int = Field(..., description="Number of bins for the histogram.")
    
# Parameters for a line chart
class LineChartParameters(BaseModel):
    x: str = Field(..., description="Column name for the x-axis data.")
    y: str = Field(..., description="Column name for the y-axis data.")
    color: Optional[str] = Field(None, description="Column name to differentiate multiple lines.")
    line_shape: str = Field(..., description="Shape of the line. Options: linear, spline, etc.")

# Parameters for a pie chart
class PieChartParameters(BaseModel):
    names: str = Field(..., description="Column name for the pie chart's categorical labels.")
    values: str = Field(..., description="Column name for the pie chart's numerical values.")
    
# Union of all chart parameter types
PlotlyParametersUnion = Union[
    BarChartParameters,
    ScatterChartParameters,
    BoxChartParameters,
    HistogramParameters,
    LineChartParameters,
    PieChartParameters,
]

# Composite class linking chart type with its corresponding parameters
class PlotlyFigureParameters(BaseModel):
    chart_type: ChartTypes = Field(..., description="Chart type that best explains the data provided.")
    parameters: PlotlyParametersUnion = Field(
        ..., description="The specific parameters required by the Plotly Python package."
    )
