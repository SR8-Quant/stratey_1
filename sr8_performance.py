import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def plot_ret_distribution(ret_series: pd.Series, title_str: str):
    # Ensure 0 is a bin edge and bins have equal width
    min_ret = ret_series.min()
    max_ret = ret_series.max()

    # Set the number of bins (adjust as needed)
    num_bins = 60
    bin_width = (max_ret - min_ret) / num_bins

    # Generate bin edges that include 0 and have equal width
    # Find the smallest bin edge that contains 0
    start_edge = min_ret - (min_ret % bin_width)
    end_edge = max_ret + (bin_width - (max_ret % bin_width))
    bin_edges = np.arange(start_edge, end_edge + bin_width, bin_width)

    # Insert 0 into bin edges if it's not already present
    if 0 not in bin_edges:
        bin_edges = np.insert(bin_edges, np.searchsorted(bin_edges, 0), 0)

    # Create figure and axes
    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True,
                                   gridspec_kw={'height_ratios': [4, 1]},
                                   figsize=(12, 8))

    # Plot histogram with different colors for positive and negative values
    ax1.hist([ret_series[ret_series < 0], ret_series[ret_series > 0]], bins=bin_edges,
             stacked=True, color=['red', 'green'], alpha=0.7, edgecolor='k')

    ax1.set_title(title_str, fontsize=16)
    ax1.set_ylabel('Frequency')
    ax1.grid(True, linestyle='--', linewidth=0.5)

    # Calculate statistics
    mean_value = ret_series.mean()
    median_value = ret_series.median()
    q1 = ret_series.quantile(0.01)
    q99 = ret_series.quantile(0.99)
    trimmed_ret_series = ret_series[(ret_series >= q1) & (ret_series <= q99)]
    trimmed_mean = trimmed_ret_series.mean()

    # Create text for the legend
    stats_text = (f"{'Mean:':<15}{mean_value *100:>10.4f}%\n"
                  f"{'Trimmed Mean:':<15}{trimmed_mean *100:>10.4f}%\n"
                  f"{'Median:':<15}{median_value *100:>10.4f}%")
    
    # Add the text box
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax1.text(0.95, 0.95, stats_text, transform=ax1.transAxes, fontsize=12,
             verticalalignment='top', horizontalalignment='right', bbox=props)

    # Boxplot
    ax2.boxplot(ret_series, vert=False, whis=[1, 99], showmeans=True, meanline=True, 
                meanprops={'color': 'blue'},
                medianprops={'color': 'black'}, 
                widths=0.5)
    ax2.set_xlabel('Value')
    ax2.set_yticks([])
    ax2.grid(True, linestyle='--', linewidth=0.5)

    # Adjust layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    plt.show()

def plot_monthly_heatplot(series_per_month: pd.Series, title_str: str):
    series_per_month.index = pd.to_datetime(series_per_month.index)
    
    # Use pivot_table to rearrange data into a DataFrame structured by year and month
    ret_per_month_df = series_per_month.groupby(
        [series_per_month.index.year, series_per_month.index.month]
        ).sum().unstack()

    # Plot heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(ret_per_month_df, annot=False, fmt=".2f", cmap="coolwarm", linewidths=0.5)
    
    # Set title and axis labels
    plt.title(f'{title_str}')
    plt.xlabel('Month')
    plt.ylabel('Year')
    plt.show()

def calculate_single_metrics(ret_series: pd.Series) -> dict:
    """
    Calculates portfolio-level performance metrics across all traded stocks for the day.
        
    Returns:
        dict: Portfolio-level performance metrics.
    """
    if ret_series.empty:
        return {}
    
    ret_mean = np.mean(ret_series)
    
    q1 = ret_series.quantile(0.01)
    q99 = ret_series.quantile(0.99)
    trimmed_ret_series = ret_series[(ret_series >= q1) & (ret_series <= q99)]
    ret_trimmed_mean = trimmed_ret_series.mean()
    
    ret_median = np.percentile(ret_series, 50)
    ret_win_rate = sum(ret_series > 0)/len(ret_series)
    
    profit_trades = ret_series[ret_series > 0]
    loss_trades = -ret_series[ret_series < 0]
    mean_profit_trades = np.mean(profit_trades) if len(profit_trades) > 0 else 0
    mean_loss_trades = np.mean(loss_trades) if len(loss_trades) > 0 else 0
    ret_pl_ratio = mean_profit_trades / mean_loss_trades if mean_loss_trades > 0 else np.inf
    
    trade_times = len(ret_series)
    
    return {
        'Mean': ret_mean,
        'Trimmed mean': ret_trimmed_mean,
        'Median': ret_median,
        'WR': ret_win_rate,
        'PL ratio': ret_pl_ratio,
        'Trade times': trade_times
    }

def calculate_equity_metrics(total_investment: int, equity_series: pd.Series) -> dict:
    # Calculate daily returns
    rets = equity_series.pct_change()
    rets.iloc[0] = equity_series.iloc[0]/total_investment - 1
    
    rets_mean = rets.mean()
    rets_std = rets.std()
    
    # Sharpe ratio
    sharpe_ratio = rets_mean / rets_std if rets_std != 0 else 0
    
    # Max Drawdown (MDD)
    equity_cummax = equity_series.cummax()
    equity_DDs = (equity_series - equity_cummax) / equity_cummax
    equity_MDD = -equity_DDs.min()
    
    # Total Return
    total_ror = equity_series.iloc[-1]/total_investment - 1
    
    # Calmar ratio
    calmar_ratio = total_ror / equity_MDD if equity_MDD != 0 else 0
    
    # Sortino ratio
    # Downside deviation
    negative_rets = rets[rets < 0]
    loss_std = negative_rets.std()
    sortino_ratio = rets_mean / loss_std if loss_std != 0 else 0

    return {
        'Total investment': int(total_investment),
        'Total RoR': total_ror,
        'RoR mean': rets_mean,
        'RoR volatility': rets_std,
        'MDD': equity_MDD,
        'Sharpe ratio': sharpe_ratio,
        'Sortino ratio': sortino_ratio,
        'Calmar ratio': calmar_ratio,
    }

def plot_equity(equity: pd.Series):
    # Calculate cumulative maximum and drawdowns
    equity_cummax = equity.cummax()
    DDs = equity - equity_cummax

    # Find positions of new highs
    new_highs = (equity == equity_cummax)

    # Calculate drawdown periods
    drawdowns = []
    in_drawdown = False
    drawdown_start = None

    for t in equity.index:
        if equity[t] == equity_cummax[t]:  # New high
            if in_drawdown:
                drawdown_end = t
                # Calculate duration as the number of periods
                duration = equity.index.get_loc(drawdown_end) - equity.index.get_loc(drawdown_start)
                drawdowns.append({'start': drawdown_start, 'end': drawdown_end, 'duration': duration})
                in_drawdown = False
        else:
            if not in_drawdown:
                drawdown_start = t
                in_drawdown = True

    # If still in drawdown at the end
    if in_drawdown:
        drawdown_end = equity.index[-1]
        # Calculate duration as the number of periods
        duration = equity.index.get_loc(drawdown_end) - equity.index.get_loc(drawdown_start)
        drawdowns.append({'start': drawdown_start, 'end': drawdown_end, 'duration': duration})

    # Find the top five longest drawdown periods
    top_five_drawdowns = sorted(drawdowns, key=lambda x: x['duration'], reverse=True)[:5]

    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True,
                                   gridspec_kw={'height_ratios': [3, 1]})

    # Plot Equity Curve
    ax1.plot(equity, label='Equity Curve', linewidth=1)
    ax1.scatter(equity.index[new_highs], equity[new_highs], color='green', marker='.', label='New Highs')

    # Mark the top five longest drawdown periods
    for period in top_five_drawdowns:
        if 'Top 5 Longest DD' not in ax2.get_legend_handles_labels()[1]:
            label = 'Top 5 Longest DD'
        else:
            label = None
        ax1.axvspan(period['start'], period['end'], color='red', alpha=0.3, label=label)
        ax2.axvspan(period['start'], period['end'], color='red', alpha=0.3, label=label)

    ax1.set_title('Equity Curve')
    ax1.set_ylabel('Return')
    ax1.grid(True)
    ax1.legend()

    # Plot Underwater Plot
    ax2.fill_between(equity.index, DDs, color='blue', alpha=0.5, label='Drawdown')
    ax2.set_title('Underwater Plot (Drawdown)')
    ax2.set_ylabel('Drawdown')
    ax2.set_xlabel('Time')
    ax2.grid(True)
    # ax2.legend()

    plt.tight_layout()
    plt.show()


def print_dict(to_print_dict: dict, key_str: str):
    key_width = max(len(str(key)) for key in to_print_dict.keys())
    key_width = max(key_width, len(key_str)) + 2
    
    value_width = 10
    
    print("-" * (key_width + value_width + 1))
    print(f"{key_str:<{key_width}} {'Value':>{value_width}}")
    print("-" * (key_width + value_width + 1))
    
    for key, value in to_print_dict.items():
        if isinstance(value, float):
            # 使用科學記號格式顯示接近 0 的浮點數
            if abs(value) < 1e-2:
                print(f"{key:<{key_width}} {value:>{value_width}.2e}")
            else:
                print(f"{key:<{key_width}} {value:>{value_width}.2f}")
        elif isinstance(value, int):
            print(f"{key:<{key_width}} {value:>{value_width}d}")
