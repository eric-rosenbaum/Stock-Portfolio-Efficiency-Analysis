import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules.visuals import plot_allocation_donut, plot_efficient_frontier_line
from modules.portfolio_math import calculate_user_efficient_frontier
from modules.data_fetcher import get_ticker_prices, fetch_data
from streamlit_plotly_events import plotly_events
import plotly.io as pio

current_theme = st.get_option("theme.base")  # 'light' or 'dark'

if current_theme == "dark":
    plotly_template = "plotly_dark"
else:
    plotly_template = "plotly_white"

# Page config and background color
st.set_page_config(layout="wide", page_title="Portfolio Optimizer", initial_sidebar_state="auto")



# Title and instructions
st.title("Portfolio Efficiency Analysis")
st.subheader("Enter Your Portfolio (note: weights must add up to 1)")

# Default editable portfolio input
default_data = pd.DataFrame({
    "Ticker": ["AAPL", "MSFT", "GOOGL"],
    "Weight": [0.33, 0.33, 0.34]
})

portfolio_df = st.data_editor(
    default_data,
    num_rows="dynamic",
    use_container_width=True,
    key="portfolio_input"
)

# When user submits the portfolio
if st.button("Submit Portfolio"):
    with st.spinner("Retrieving data..."):
        portfolio_df["Ticker"] = portfolio_df["Ticker"].str.upper()
        portfolio_df = portfolio_df.dropna()
        total_weight = portfolio_df["Weight"].sum()

        if abs(total_weight - 1.0) > 0.01:
            st.warning("Weights don't sum to 1. Adjusting automatically.")
            portfolio_df["Weight"] = portfolio_df["Weight"] / total_weight

        # Fetch price data
        one_year_ago = datetime.now().date() - timedelta(days=365)
        price_data = []



        for ticker in portfolio_df["Ticker"]:
            prices = get_ticker_prices(ticker)
            if not prices:
                fetch_data(ticker)
                prices = get_ticker_prices(ticker)

            filtered = [p for p in prices if p["date"] >= one_year_ago]
            df = pd.DataFrame(filtered).set_index("date").sort_index()
            df.rename(columns={"close": ticker}, inplace=True)
            price_data.append(df[[ticker]])

        if price_data:
            combined_df = pd.concat(price_data, axis=1)

            # Calculate frontier and user portfolio
            user_weights = portfolio_df["Weight"].values
            frontier_df, user_point, efficient_line_df = calculate_user_efficient_frontier(
                combined_df,
                user_weights=user_weights
            )
            efficient_line_df = efficient_line_df.drop_duplicates(subset="volatility")
            efficient_line_df = efficient_line_df.sort_values(by="volatility")


            # Two-column layout
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Allocation Breakdown")
                donut_fig = plot_allocation_donut(portfolio_df)
                st.plotly_chart(donut_fig, use_container_width=True)

            with col2:
                # Efficient Frontier with hover tooltip


                with st.container():
                    st.subheader("Efficient Frontier")
                    st.caption("The efficient frontier is created from points, each representing a different " \
                    "weighting of the stocks present in your portolfio. The breakdowns that have the best level of return " \
                    "for a given level of risk make up this line.")


                frontier_fig = plot_efficient_frontier_line(efficient_line_df, user_point)
                selected_points = plotly_events(frontier_fig, click_event=True, key="frontier_click")

                if selected_points:
                    point_index = selected_points[0]["pointIndex"]
                    selected_weights = efficient_line_df.iloc[point_index]["weights"]
                    tickers = combined_df.columns.tolist()

                    selected_portfolio_df = pd.DataFrame({
                        "Ticker": tickers,
                        "Weight": selected_weights
                    })

                    st.subheader("Clicked Portfolio Allocation")
                    st.plotly_chart(plot_allocation_donut(selected_portfolio_df), use_container_width=True)
