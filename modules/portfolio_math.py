# portfolio_math.py
import numpy as np
import pandas as pd

def calculate_user_efficient_frontier(price_df, num_portfolios=5000, risk_free_rate=0.02, user_weights=None):
    price_df = price_df.head(252)
    daily_returns = price_df.pct_change().dropna()
    mean_returns = daily_returns.mean()
    cov_matrix = daily_returns.cov()
    tickers = price_df.columns

    results = {
        "returns": [],
        "volatility": [],
        "sharpe": [],
        "weights": []
    }

    for _ in range(num_portfolios):
        weights = np.random.random(len(tickers))
        weights /= np.sum(weights)

        port_return = np.dot(weights, mean_returns) * 252
        port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 252, weights)))
        sharpe = (port_return - risk_free_rate) / port_volatility

        results["returns"].append(port_return)
        results["volatility"].append(port_volatility)
        results["sharpe"].append(sharpe)
        results["weights"].append(weights)

    df = pd.DataFrame(results)

    # Efficient frontier line (upper edge)
    df_sorted = df.sort_values(by="volatility")
    efficient_points = []
    max_return = -np.inf

    for _, row in df_sorted.iterrows():
        if row["returns"] > max_return:
            efficient_points.append(row)
            max_return = row["returns"]

    efficient_line_df = pd.DataFrame(efficient_points)

    # User portfolio
    user_point = None
    if user_weights is not None:
        user_return = np.dot(user_weights, mean_returns) * 252
        user_volatility = np.sqrt(np.dot(user_weights.T, np.dot(cov_matrix * 252, user_weights)))
        user_point = (user_volatility, user_return)

    return df, user_point, efficient_line_df
