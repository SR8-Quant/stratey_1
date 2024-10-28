import pandas as pd
import numpy as np
from pathlib import Path
import pandas_market_calendars as mcal
from datetime import datetime

import sr8_performance as sr8

def execute_strategy_on_single(
        ts_np: np.array,
        open_np: np.array,
        close_np: np.array,
        initial_cap: int = 1e5,
        stop_loss_pct: float = 0.005,
        earliest_entry_time: str = '09:06',
    ) -> pd.Series:

    idx_len = len(ts_np)
    
    earliest_entry_idx = np.searchsorted(ts_np, earliest_entry_time, side='left')
    partial_exit_idx_1 = np.searchsorted(ts_np, '11:00', side='left')
    partial_exit_idx_2 = np.searchsorted(ts_np, '13:00', side='left')
    partial_exit_idx_3 = np.searchsorted(ts_np, '13:30', side='left')

    equity = np.full(idx_len, np.nan, dtype=float)
    
    entry_price = open_np[earliest_entry_idx]
    initial_position = np.floor(initial_cap * 1000 / (entry_price * 1.000399)) / 1000
    partial_close_position = np.floor(initial_position / 3)
    position = initial_position
    cap = initial_cap - position * entry_price
    
    equity[0 : earliest_entry_idx] = initial_cap
    equity[earliest_entry_idx] = cap + position * (2 * entry_price - close_np[earliest_entry_idx] * 1.003399)
    
    earliest_entry_idx += 1
    trailing_price = entry_price
    for i in range(earliest_entry_idx, idx_len):
        if position > 0:
            exit_price = open_np[i]
            if i >= partial_exit_idx_3:
                cap += position * (2 * entry_price - exit_price * 1.003399)
                position = 0
            elif close_np[i-1] > trailing_price * (1 + stop_loss_pct):
                trailing_price = exit_price
                cap += position * (2 * entry_price - exit_price * 1.003399)
                position -= position
            elif i == partial_exit_idx_1 or i == partial_exit_idx_2:
                cap += partial_close_position * (2 * entry_price - exit_price * 1.003399)
                position -= partial_close_position
        equity[i] = cap + position * (2 * entry_price - close_np[i] * 1.003399)
        if position <= 0:
            break

    if i < idx_len - 1:
        equity[i+1:] = equity[i]
    
    equity_series = pd.Series(equity, index=ts_np, name='Equity')
    
    return equity_series

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
            
            ret = equity.iloc[-1] - equity.iloc[0]
            
            ret_list.append((day, ret))
    
    index_series, ret_series = zip(*ret_list)
    ret_series = pd.Series(data=ret_series, index=index_series)
    
    # ret_series 以日期為 index
    ret_series.index = pd.to_datetime(ret_series.index)
    return ret_series


#%%
if __name__ == "__main__":
    filtered_stocks_list_path = Path('***') # exist path of 'filtered_stocks_list.parquet'
    filtered_stocks_data_path = Path('***') # exist path of 'filtered_stocks_data.parquet'
    
    filtered_stocks_list = pd.read_parquet(filtered_stocks_list_path)
    filtered_stocks_data = pd.read_parquet(filtered_stocks_data_path)

    start_date = '2023-09-01'
    end_date = '2024-10-14'
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
    
    investment_each_trade = 1e5
    
    ret_per_trade = backtest(
        filtered_stocks_list, 
        filtered_stocks_data, 
        start_date_dt, 
        end_date_dt
    )
    total_investment = len(ret_per_trade) * investment_each_trade
    ret_per_day = ret_per_trade.groupby(ret_per_trade.index).sum()
    ror_per_trade = ret_per_trade/investment_each_trade
    ror_per_day = ret_per_trade.groupby(ret_per_trade.index).mean()/investment_each_trade
    
    # ret_per_week = ret_per_day.resample('W-SAT').sum()
    
    ret_per_month = ret_per_day.resample('ME').sum()
    
    equity_series = ret_per_day.cumsum() + total_investment
    
    tradely_metrics = sr8.calculate_single_metrics(ror_per_trade)
    
    daily_metrics = sr8.calculate_single_metrics(ror_per_day)
    
    equity_metrics = sr8.calculate_equity_metrics(total_investment, equity_series)
    
    #%%
    sr8.plot_monthly_heatplot(ret_per_month, 'Monthly Return')
    sr8.plot_equity(equity_series)
    sr8.plot_ret_distribution(ror_per_day, 'Returns (daily)')
    sr8.plot_ret_distribution(ror_per_trade, 'Returns (tradely)')
    sr8.print_dict(daily_metrics, 'Performance (daily)')
    sr8.print_dict(equity_metrics, 'Equity Performance (daily)')
    sr8.print_dict(tradely_metrics, 'Performance (tradely)')
    
    
