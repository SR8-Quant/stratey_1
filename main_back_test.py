import pandas as pd
import numpy as np
from pathlib import Path
import pandas_market_calendars as mcal
from datetime import datetime

import matplotlib.pyplot as plt

def execute_strategy_on_single(
        ts_np: np.array,
        open_np: np.array,
        close_np: np.array,
        initial_cap: int = 1e6, 
        stop_loss_pct: float = 0.01,
        earliest_entry_time: str = '09:06',
        ):
    idx_len = len(ts_np)
    open_np *= 1000
    close_np *= 1000
    
    earliest_entry_idx = np.searchsorted(ts_np, earliest_entry_time)
    partial_exit_idx_1 = np.searchsorted(ts_np, '11:00')
    partial_exit_idx_2 = np.searchsorted(ts_np, '13:00')
    partial_exit_idx_3 = np.searchsorted(ts_np, '13:30')
    
    equity = np.full(idx_len, np.nan, dtype=float)
    
    entry_price = open_np[earliest_entry_idx - 1]
    initial_position = np.floor(initial_cap / (entry_price * 1.000399))
    to_close_position = np.floor(initial_position / 3)
    position = initial_position
    cap = initial_cap - position * entry_price
    equity[0 : earliest_entry_idx] = initial_cap

    for i in range(earliest_entry_idx, idx_len):
        exit_price = open_np[i]
        if position > 0:
            if close_np[i] > entry_price * (1 + stop_loss_pct) or i >= partial_exit_idx_3:
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

def back_test(
        filtered_stocks_list: pd.DataFrame,
        filtered_stocks_data: pd.DataFrame,
        start_date: datetime,
        end_date: datetime,
        ):
    
    trading_days = mcal.get_calendar('XTAI').schedule(
        start_date = start_date, 
        end_date = end_date
        ).index.strftime('%Y-%m-%d')
    
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
            ret_list.append(ret)
    return np.array(ret_list)

def plot_distribution(lst: np.array, start_date: str, end_date: str):
    mean_ret = np.mean(lst)
    q1 = np.percentile(lst, 25)
    median = np.percentile(lst, 50)
    q3 = np.percentile(lst, 75)
    win_rate = sum(lst > 0)/len(ret_list)
    
    profit_trades = ret_list[ret_list > 0]
    loss_trades = -ret_list[ret_list < 0]
    mean_profit = np.mean(profit_trades) if len(profit_trades) > 0 else 0
    mean_loss = np.mean(loss_trades) if len(loss_trades) > 0 else 0
    pl_ratio = mean_profit / mean_loss if mean_loss > 0 else np.inf
    
    plt.figure(figsize=(12, 7))
    plt.hist(lst, bins=50, edgecolor='k', alpha=0.7)
    
    plt.axvline(mean_ret, color='r', linestyle='-', label=f'Mean: {mean_ret * 1000:.2f}\u2030')
    plt.axvline(q1, color='gray', linestyle='-', label=f'Q1: {q1 * 1000:.2f}\u2030')
    plt.axvline(median, color='gray', linestyle='-', label=f'Q2: {median * 1000:.2f}\u2030')
    plt.axvline(q3, color='gray', linestyle='-', label=f'Q3: {q3 * 1000:.2f}\u2030')
    
    win_rate_label = f'WR: {win_rate * 100:.2f}%'
    pl_ratio_label = f'P/L: {pl_ratio:.2f}'
    
    plt.title(f'Distribution of Returns: each trade from {start_date} to {end_date}')
    plt.xlabel(f'Return ({win_rate_label}, {pl_ratio_label})')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    plt.show()
    
if __name__ == "__main__":
    filtered_stocks_list_path = Path('***') # path of 'iltered_stocks_list.parquet'
    filtered_stocks_data_path = Path('***') # path of 'filtered_stocks_data.parquet'
    
    filtered_stocks_list = pd.read_parquet(filtered_stocks_list_path)
    filtered_stocks_data = pd.read_parquet(filtered_stocks_data_path)

    start_date = '2022-10-01'
    end_date = '2023-10-01'
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')

    ret_list = back_test(filtered_stocks_list, filtered_stocks_data, start_date_dt, end_date_dt)
    plot_distribution(ret_list, start_date, end_date)
                                    
    