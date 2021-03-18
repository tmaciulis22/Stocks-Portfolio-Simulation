import util
import calculations
import constants

dfs = [util.load_data(path) for path in constants.data_paths]
returns = [calculations.find_optimized_strategy(df) for df in dfs]

stocks_fig, axes = util.create_subplots()
flattened_axes = axes.flatten()
for index, value in enumerate(returns):
    util.plot_data(
        flattened_axes[index],
        dfs[index][constants.DATE_COLUMN],
        value,
        constants.titles[index],
        y_label=constants.RETURNS_LABEL
    )

portfolio_subplot = util.new_subplot()
portfolio_returns_percentage = calculations.get_portfolio_percentage(returns)
util.plot_data(
    portfolio_subplot,
    dfs[0][constants.DATE_COLUMN],
    portfolio_returns_percentage,
    constants.PORTFOLIO_CHART_TITLE,
    y_label=constants.PERCENT_LABEL
)

util.show_correlation(returns)
