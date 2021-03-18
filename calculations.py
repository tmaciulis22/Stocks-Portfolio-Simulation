import constants
import numpy as np


def calculate_bollinger_band(df, period=constants.BOLLINGER_PERIOD, multiplier=constants.BOLLINGER_MULTIPLIER):
    moving_avg = np.round(df[constants.CLOSE_COLUMN].rolling(window=period).mean(), 2)

    std = np.round(df[constants.CLOSE_COLUMN].rolling(window=period).std(), 2)
    multiplied_std = np.multiply(std, multiplier)

    upper_band = np.round(np.add(moving_avg, multiplied_std), 2)
    lower_band = np.round(np.subtract(moving_avg, multiplied_std), 2)

    return upper_band, lower_band


def simulate_strategy(df, upper_band, lower_band, period):
    current_position = 0
    prices = df[constants.CLOSE_COLUMN]
    returns = np.zeros_like(prices)
    positions = np.zeros_like(prices)
    no_of_shares = 0

    for i in range(period, len(prices)):
        returns[i] = (prices[i] - prices[i - 1]) * current_position * no_of_shares
        if prices[i] <= (lower_band[i]) and current_position != 1:
            current_position = 1
            no_of_shares = np.floor(constants.SUM_TO_INVEST / prices[i])
        elif prices[i] >= (upper_band[i]) and current_position != -1:
            current_position = -1
            no_of_shares = np.floor(constants.SUM_TO_INVEST / prices[i])
        positions[i] = current_position

    sharpe_ratio = annualised_sharpe(returns)
    return returns, sharpe_ratio


def find_optimized_strategy(df):
    max_sharpe_ratio = 0
    returns = None

    for period in range(1, 30):
        for multiplier in range(1, 3):
            upper_band, lower_band = calculate_bollinger_band(df, period, multiplier)
            temp_returns, temp_sharpe_ratio = simulate_strategy(df, upper_band, lower_band, period)
            if temp_sharpe_ratio > max_sharpe_ratio:
                max_sharpe_ratio = temp_sharpe_ratio
                returns = temp_returns

    return returns.cumsum()


def annualised_sharpe(returns):
    multiplication = np.multiply(np.sqrt(returns.size), returns.mean())
    std = returns.std()

    if multiplication == 0 or std == 0:
        return 0

    return np.divide(multiplication, std)


def get_portfolio_percentage(returns):
    summed_returns = np.array(returns).sum(axis=0)
    pct_change = np.divide(np.multiply(summed_returns, 100), constants.SUM_TO_INVEST * len(constants.data_paths))
    return pct_change
