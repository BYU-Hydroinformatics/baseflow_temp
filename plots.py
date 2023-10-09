import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime, timedelta
from urllib import request, parse
import os
import plotly.graph_objs as go
import math


def plot_hydrograph_recession(data):
    """
        Generate a hydrograph recession chart based on streamflow data.

        Parameters:
            data_path (str): Path to the CSV file containing streamflow data.

        Returns:
            None. Displays the hydrograph recession chart.
    """
    # Calculate recession index (logarithm of discharge)
    data["recession_index"] = data["Discharge"].apply(lambda q: np.log10(q))

    # Sort data based on recession index
    data = data.sort_values("recession_index")

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.scatter(data["recession_index"], data["Discharge"], color='blue', marker='o')
    plt.xlabel("Recession Index (log10(Q))")
    plt.ylabel("Streamflow Discharge")
    plt.title("Hydrograph Recession Chart")
    plt.grid(True)

    # Show the plot
    plt.show()


def plot_discharge_and_models(df, model_columns):
    """
        Plot Discharge and multiple models over time.

        Parameters:
        df (pandas.DataFrame): The DataFrame containing the data to be plotted.
        model_columns (list of str): A list of column names representing the models to be plotted.

        Returns:
        None

        This function takes a DataFrame with columns including 'Date', 'Discharge', and model columns,
        and creates a line plot to visualize the Discharge and multiple models over time.
        It is designed to be flexible and can handle any number of models by specifying their column names
        in the 'model_columns' parameter.

        Example Usage:
        model_columns = ['Lyne_Hollick', 'Chapman', 'New_Model']
        plot_discharge_and_models(df, model_columns)
    """
        
    # Extract Date and Discharge columns
    date = df['Date']
    discharge = df['Discharge']
    
    # Create a plot for Discharge
    plt.figure(figsize=(14, 6))
    plt.plot(date, discharge, label='Discharge', color='blue', linewidth=2)

    # Plot additional models
    for model_column in model_columns:
        plt.plot(date, df[model_column], label=model_column, linestyle='--')

    # Customize the plot
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Discharge and Models Over Time')
    plt.legend(loc='upper right')
    plt.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()

