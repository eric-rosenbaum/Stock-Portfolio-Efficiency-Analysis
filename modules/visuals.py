import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import numpy as np



def plot_allocation_donut(portfolio_df):
    fig = px.pie(
        portfolio_df,
        names="Ticker",
        values="Weight",
        hole=0.4,
        title="Portfolio Allocation"
    )
    fig.update_traces(textinfo="percent+label")
    return fig

# Example placeholder for a price chart function
def plot_price_chart(prices_df):
    fig = go.Figure()
    for col in prices_df.columns:
        fig.add_trace(go.Scatter(x=prices_df.index, y=prices_df[col], mode='lines', name=col))
    fig.update_layout(title="Closing Prices Over Time", xaxis_title="Date", yaxis_title="Price")
    return fig



def plot_efficient_frontier_line(efficient_line_df, portfolio_point):
    fig = go.Figure()

    # Efficient frontier line
    fig.add_trace(go.Scatter(
        x=efficient_line_df["volatility"],
        y=efficient_line_df["returns"],
        mode="lines+markers",
        line=dict(color="blue", width=2),
        marker=dict(size=6, color="blue"),
        name="Efficient Frontier",
        customdata=[list(w) if isinstance(w, (list, tuple, np.ndarray)) else [w] for w in efficient_line_df["weights"]],
        hovertemplate="Return: %{y:.2%}<br>Risk: %{x:.2%}<extra></extra>"
    ))

    # User point
    fig.add_trace(go.Scatter(
        x=[portfolio_point[0]],
        y=[portfolio_point[1]],
        mode="markers",
        marker=dict(size=10, color="red", symbol="star"),
        name="Your Portfolio",
        hovertemplate="Your Portfolio<br>Return: %{y:.2%}<br>Risk: %{x:.2%}<extra></extra>"
    ))

    fig.update_layout(
        title="Efficient Frontier",
        xaxis_title="Volatility (Risk)",
        yaxis_title="Expected Return",
        template="plotly_white"
    )

    return fig
