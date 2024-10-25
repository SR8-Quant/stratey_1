import pandas as pd
import numpy as np
from pathlib import Path
import pandas_market_calendars as mcal
from datetime import datetime

import seaborn as sns
import matplotlib.pyplot as plt

def execute_strategy_on_single(
        ts_np: np.array,
        open_np: np.array,
        close_np: np.array,
        initial_cap: int = 1e5,
        stop_loss_pct: float = 0.01,
        earliest_entry_time: str = '09:06',
    ) -> np.array:

    idx_len = len(ts_np)
    open_np *= 1000
    close_np *= 1000
    
    earliest_entry_idx = np.searchsorted(ts_np, earliest_entry_time, side='left')
    partial_exit_idx_1 = np.searchsorted(ts_np, '11:00', side='left')
    partial_exit_idx_2 = np.searchsorted(ts_np, '13:00', side='left')
    partial_exit_idx_3 = np.searchsorted(ts_np, '13:30', side='left')
    
    equity = np.full(idx_len, np.nan, dtype=float)
    
    entry_price = open_np[earliest_entry_idx]
    initial_position = np.floor(initial_cap / (entry_price * 1.000399))
    to_close_position = np.floor(initial_position / 3)
    position = initial_position
    cap = initial_cap - position * entry_price
    
    earliest_entry_idx += 1
    equity[0 : earliest_entry_idx] = initial_cap

    for i in range(earliest_entry_idx, idx_len):
        if position > 0:
            exit_price = open_np[i]
            if close_np[i-1] > entry_price * (1 + stop_loss_pct) or i >= partial_exit_idx_3:
                cap += position * (2 * entry_price - exit_price * 1.003399)
                position = 0
            elif i == partial_exit_idx_1 or i == partial_exit_idx_2:
                cap += to_close_position * (2 * entry_price - exit_price * 1.003399)
                position -= to_close_position
        equity[i] = cap + position * (2 * entry_price - close_np[i] * 1.003399)
        if position <= 0:
            break

    if i < idx_len - 1:
        equity[i+1:] = equity[i]

    return equity

#%%
def backtest(
        filtered_stocks_list: pd.DataFrame,
        filtered_stocks_data: pd.DataFrame,
        start_date: datetime,
        end_date: datetime,
    ) -> pd.Series:
    
    trading_days = mcal.get_calendar('XTAI').schedule(
        start_date = start_date, 
        end_date = end_date
    ).index.strftime('%Y-%m-%d')
    
    # (day, ret)
    ret_list = []
    for day in trading_days:
        if day not in filtered_stocks_list.index:
            continue
        stock_list = filtered_stocks_list.loc[day, 'stock_list']
        if len(stock_list) == 0:
            continue
        for stock_code in stock_list:
            day_data = filtered_stocks_data.loc[day, stock_code].dropna()
            
            ts_np = day_data.index.strftime('%H:%M').to_numpy()
            open_np = day_data['Open'].to_numpy()
            close_np = day_data['Close'].to_numpy()
            
            equity = execute_strategy_on_single(ts_np, open_np, close_np)
            ret = equity[-1]/equity[0] - 1
            ret_list.append((day, ret))
    index_series, ret_series = zip(*ret_list)
    ret_series = pd.Series(data=ret_series, index=index_series)
    
    # ret_series 以日期為 index
    ret_series.index = pd.to_datetime(ret_series.index)
    return ret_series

#%%
def plot_ret_distribution(ret_series: pd.Series, start_date: str, end_date: str, title_str: str):
    mean_ret = np.mean(ret_series)
    q1 = np.percentile(ret_series, 25)
    median = np.percentile(ret_series, 50)
    q3 = np.percentile(ret_series, 75)
    
    win_rate = sum(ret_series > 0)/len(ret_series)
    
    profit_trades = ret_series[ret_series > 0]
    loss_trades = -ret_series[ret_series < 0]
    mean_profit = np.mean(profit_trades) if len(profit_trades) > 0 else 0
    mean_loss = np.mean(loss_trades) if len(loss_trades) > 0 else 0
    pl_ratio = mean_profit / mean_loss if mean_loss > 0 else np.inf
    
    plt.figure(figsize=(12, 7))
    plt.hist(ret_series, bins=70, edgecolor='k', alpha=0.7)
    
    # plt.axvline(0, color='black', linestyle='-')
    plt.axvline(mean_ret, color='r', linestyle='-', label=f'Mean: {mean_ret * 100:.2f}%')
    plt.axvline(q1, color='blue', linestyle='-', label=f'Q1: {q1 * 100:.2f}%')
    plt.axvline(median, color='blue', linestyle='-', label=f'Q2: {median * 100:.2f}%')
    plt.axvline(q3, color='blue', linestyle='-', label=f'Q3: {q3 * 100:.2f}%')
    
    win_rate_label = f'WR: {sum(ret_series > 0)}/{len(ret_series)} = {win_rate * 100:.2f}%'
    pl_ratio_label = f'PL: {mean_profit*100:.2f}%/{mean_loss*100:.2f}% = {pl_ratio:.2f}'
    
    plt.title(f'{title_str}\n{win_rate_label}, {pl_ratio_label}')
    plt.xlabel(f'Returns (from {start_date} to {end_date})')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_monthly_heatplot(series_per_month: pd.Series, title_str: str):
    series_per_month.index = pd.to_datetime(series_per_month.index)
    
    # 使用 pivot_table 重新排列數據為以年和月為結構的 DataFrame
    ret_per_month_df = series_per_month.groupby(
        [series_per_month.index.year, series_per_month.index.month]
        ).sum().unstack()

    # 畫熱力圖
    plt.figure(figsize=(10, 6))
    sns.heatmap(ret_per_month_df, annot=False, fmt=".2f", cmap="coolwarm", linewidths=0.5)
    
    # 設置標題和軸標籤
    plt.title(f'{title_str}')
    plt.xlabel('Month')
    plt.ylabel('Year')
    plt.show()

def calculate_daily_metrics(ret_series: pd.Series) -> dict:
    """
    Calculates portfolio-level performance metrics across all traded stocks for the day.
        
    Returns:
        dict: Portfolio-level performance metrics.
    """
    if ret_series.empty:
        return {}
    
    mean_per_trade = np.mean(ret_series)
    q1_per_trade = np.percentile(ret_series, 25)
    q2_per_trade = np.percentile(ret_series, 50)
    q3_per_trade = np.percentile(ret_series, 75)
    win_rate_per_trade = sum(ret_series > 0)/len(ret_series)
    
    profit_trades = ret_series[ret_series > 0]
    loss_trades = -ret_series[ret_series < 0]
    mean_profit_trades = np.mean(profit_trades) if len(profit_trades) > 0 else 0
    mean_loss_trades = np.mean(loss_trades) if len(loss_trades) > 0 else 0
    pl_ratio_per_trade = mean_profit_trades / mean_loss_trades if mean_loss_trades > 0 else np.inf
    
    trade_count = len(ret_series)


    #%%
    ret_per_day = ret_per_trade.groupby(ret_per_trade.index).sum()
    
    mean_per_day = np.mean(ret_per_day)
    q1_per_day = np.percentile(ret_per_day, 25)
    q2_per_day = np.percentile(ret_per_day, 50)
    q3_per_day = np.percentile(ret_per_day, 75)
    win_rate_per_day = sum(ret_per_day > 0)/len(ret_per_day)
    
    profit_days = ret_per_day[ret_per_day > 0]
    loss_days = -ret_per_day[ret_per_day < 0]
    mean_profit_days = np.mean(profit_days) if len(profit_days) > 0 else 0
    mean_loss_days = np.mean(loss_days) if len(loss_days) > 0 else 0
    pl_ratio_per_day = mean_profit_days / mean_loss_days if mean_loss_days > 0 else np.inf
    
    std_per_day = ret_per_day.std()
    sharpe_ratio = mean_per_day / std_per_day * np.sqrt(len(ret_per_day)) if std_per_day != 0 else 0
    
    equity = ret_per_day.cumsum()
    equity_cummax = equity.cummax()
    equity_DDs = (equity_cummax - equity) / equity_cummax
    equity_MDD = equity_DDs.max()
    
    total_ret = equity.iloc[-1] / equity.iloc[0] - 1
    calmar_ratio = total_ret / equity_MDD if equity_MDD != 0 else 0
    
    # Sortino ratio (using only negative returns for denominator)
    loss_days_std = loss_days.std()
    sortino_ratio = total_ret / loss_days_std if loss_days_std != 0 else 0
    
    return {
        'Total return': total_ret,
        'Mean per trade': mean_per_trade,
        # 'Q1 per trade': q1_per_trade,
        'Mode per trade': q2_per_trade,
        # 'Q3 per trade': q3_per_trade,
        'WR per trade': win_rate_per_trade,
        'PL ratio per trade': pl_ratio_per_trade,
        'Trade times': trade_count,
        'Mean per day': mean_per_day,
        # 'Q1 per day': q1_per_day,
        'Mode per day': q2_per_day,
        # 'Q3 per day': q3_per_day,
        'WR per day': win_rate_per_day,
        'PL ratio per day':pl_ratio_per_day,
        'Sharpe ratio': sharpe_ratio,
        'Daily Volatility': std_per_day,
        'MDD': equity_MDD,
        'Calmar ratio': calmar_ratio,
        'Sortino ratio': sortino_ratio,
    }

#%%
def plot_daily_equity(equity: pd.Series):
    # Calculate drawdown
    equity_cummax = equity.cummax()
    DDs = (equity_cummax - equity) / equity_cummax

    # Identify new high points
    new_highs = (equity == equity_cummax)

    # Find drawdown periods
    DD_periods = DDs > 0
    
    # Find drawdown start and end indices
    DD_starts = np.where((~DD_periods[:-1]) & (DD_periods[1:]))[0] + 1
    DD_ends = np.where((DD_periods[:-1]) & (~DD_periods[1:]))[0] + 1

    # If drawdown starts at the beginning
    if DD_periods.iloc[0]:
        DD_starts = np.insert(DD_starts, 0, 0)

    # If drawdown ends after the last data point
    if DD_periods.iloc[-1]:
        DD_ends = np.append(DD_ends, len(DDs) - 1)
    
    open_time = equity.index
    # Calculate maximum drawdowns and durations
    mdds = []
    for start, end in zip(DD_starts, DD_ends):
        MDD = np.max(DDs[start:end+1])
        duration = (open_time[end] - open_time[start]).astype('timedelta64[m]').astype(int)
        mdds.append({'start': start, 'end': end, 'mdd': MDD, 'duration': duration})

    # Sort by duration (longest first)
    MDDs_sorted = sorted(mdds, key=lambda x: x['duration'], reverse=True)
    top_MDDs = MDDs_sorted[:5]

    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True,
                                   gridspec_kw={'height_ratios': [3, 1]})
    ax1.plot(equity, label='Equity Curve', linewidth=1)

    # Corrected scatter to use index values for the new highs
    ax1.scatter(equity.index[new_highs], equity[new_highs], color='green', marker='^', label='New Highs')

    # Highlight top five longest drawdown areas
    for MDD_info in top_MDDs:
        start_idx = MDD_info['start']
        end_idx = MDD_info['end']
        ax1.axvspan(open_time[start_idx], open_time[end_idx], color='red', alpha=0.2)

    ax1.set_title('Equity Curve vs Buy&Hold')
    ax1.set_ylabel('Normalized Return')
    ax1.legend()
    ax1.grid(True)

    # Underwater plot, corrected fill_between
    ax2.fill_between(equity.index, 0, -DDs, color='blue', alpha=0.5)
    ax2.set_title('Underwater Plot (Drawdown)')
    ax2.set_ylabel('Drawdown')
    ax2.set_xlabel('Time')
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

#%%
if __name__ == "__main__":
    filtered_stocks_list_path = Path('***') # exist path of 'filtered_stocks_list.parquet' 
    filtered_stocks_data_path = Path('***') # exist path of 'filtered_stocks_data.parquet'
    
    filtered_stocks_list = pd.read_parquet(filtered_stocks_list_path)
    filtered_stocks_data = pd.read_parquet(filtered_stocks_data_path)

    start_date = '2022-01-01'
    end_date = '2024-10-14'
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')

    ret_per_trade = backtest(filtered_stocks_list, filtered_stocks_data, start_date_dt, end_date_dt)
    ret_per_day = ret_per_trade.groupby(ret_per_trade.index).sum()
    
    # ret_per_week = ret_per_day.resample('W-SAT').sum()
    
    ret_per_month = ret_per_day.resample('ME').sum()
    
    plot_ret_distribution(ret_per_trade, start_date, end_date,
                      'Distribution of Returns / trade')
    plot_ret_distribution(ret_per_day, start_date, end_date,
                      'Distribution of Returns / day')                    
    plot_monthly_heatplot(ret_per_month, 'Monthly Return Heatmap')
    
    #%%
    daily_metrics = calculate_daily_metrics(ret_per_trade)
    # 設定 key 和 value 的對齊寬度
    key_width = max(len(str(key)) for key in daily_metrics.keys()) + 2
    value_width = 10  # 可以根據需要調整寬度
    # 列印標題
    print(f"{'Key':<{key_width}} {'Value':<{value_width}}")
    # 列印分隔線
    print("-" * (key_width + value_width))
    # 列印每個 key 和 value，value 限制到小數點後兩位
    for key, value in daily_metrics.items():
        if isinstance(value, float):
            # 若 value 是 float，格式化到小數點後兩位
            print(f"{key:<{key_width}} {value:<{value_width}.2f}")
        else:
            # 若 value 是其他類型，直接輸出
            print(f"{key:<{key_width}} {value:<{value_width}}")
    
    #%%
    equity = ret_per_day.cumsum()
    plot_daily_equity(equity)
    
