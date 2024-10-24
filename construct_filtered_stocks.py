import pandas as pd
from pathlib import Path
from typing import List
import pandas_market_calendars as mcal
from concurrent.futures import ThreadPoolExecutor

def filter_stocks_by_list(
        stocks_df: pd.DataFrame,
        stocks_list: List[str]
    ) -> pd.DataFrame:
    """Filter stocks_df to retain only rows where the 'StockCode' in the MultiIndex is in the stocks_list."""
    filtered_stocks_df = stocks_df[stocks_df.index.get_level_values(0).isin(stocks_list)]
    return filtered_stocks_df

def filter_stocks_by_trading_days(
        stocks_df: pd.DataFrame,
        start_date_str: str,
        end_date_str: str
        ) -> pd.DataFrame:
    """Filter all_stocks_df by keeping only rows within the business days range."""
    start_date = pd.to_datetime(start_date_str)
    end_date = pd.to_datetime(end_date_str)
    trading_days = mcal.get_calendar('XTAI').schedule(
        start_date=start_date, 
        end_date=end_date
        ).index.strftime('%Y-%m-%d')
    reindexed_stocks = []
    for stock_code in stocks_df.index.get_level_values(0).unique():
        stock_data = stocks_df.xs(stock_code, level=0)
        stock_data = stock_data.reindex(trading_days)
        stock_data.columns = pd.MultiIndex.from_product([[stock_code], stock_data.columns])
        reindexed_stocks.append(stock_data)

    combined_df = pd.concat(reindexed_stocks, axis=1)
    
    return combined_df

def create_top_ret(
        stocks_df: pd.DataFrame,
        offset_days: int = 3,
        top_n: int = 100
        ) -> pd.DataFrame:
    close_df = stocks_df.xs('Close', axis=1, level=1)
    
    ret_df = close_df.pct_change(periods=offset_days, fill_method=None).shift(1)
    
    criteria_df = pd.DataFrame(False, index=ret_df.index, columns=ret_df.columns)
    
    # Iterate over each trading day to identify top N stocks
    for date, row in ret_df.iterrows():
        if row.isna().all():
            continue  # Skip if all returns are NaN for the date
        # Drop NaN values to exclude stocks with undefined returns
        row_cleaned = row.dropna()
        # Get the top N stocks based on return
        top_stocks = row_cleaned.nlargest(top_n).index.tolist()
        # Mark the top N stocks as True in the criteria DataFrame
        criteria_df.loc[date, top_stocks] = True
    
    return criteria_df

def create_new_high(
        stocks_df: pd.DataFrame,
        offset_days: int = 3
        ) -> pd.DataFrame:
    # Extract 'Close' and 'High' columns from the multi-index DataFrame
    close_df = stocks_df.xs('Close', axis=1, level=1)
    high_df = stocks_df.xs('High', axis=1, level=1)
    
    # Criteria: The previous day's Close is higher than the maximum High over the past offset_days
    criteria = close_df.shift(1) > high_df.shift(2).rolling(window=offset_days).max()
    
    return criteria

def create_filtered_by_vol_and_amount(
        stocks_df: pd.DataFrame,
        offset_days: int = 3
        ) -> pd.DataFrame:
    """
    Create a criteria DataFrame based on Volume and Amount thresholds.
    
    Parameters:
    - stocks_df: pd.DataFrame, Multi-index columns with 'Volume' and 'Amount'
    - offset_days: int, number of days for rolling average in volume criteria
    
    Returns:
    - pd.DataFrame: A boolean DataFrame where True indicates the stock meets the volume and amount criteria
    """
    # Extract 'Volume' and 'Amount' columns
    volume_df = stocks_df.xs('Volume', axis=1, level=1)
    amount_df = stocks_df.xs('Amount', axis=1, level=1)
    
    # Criterion 1: Volume on the previous day is greater than 3 times the average volume over the past offset_days
    criteria_1 = volume_df.shift(1) > 3 * volume_df.shift(2).rolling(window=offset_days).mean()
    
    # Criterion 2: Volume on the previous day is greater than 1000
    criteria_2 = volume_df.shift(1) > 2000
    
    # Criterion 3: Amount on the previous day is greater than 1 billion
    criteria_3 = amount_df.shift(1) > 1e8
    
    # Combine all criteria: A stock must satisfy all three criteria to be selected
    combined_criteria = criteria_1 & criteria_2 & criteria_3
    
    return combined_criteria


def criterion_to_list(
        stocks_df: pd.DataFrame,
        *criteria: pd.DataFrame
        ) -> pd.DataFrame:

    combined_criteria = criteria[0]
    for crit in criteria[1:]:
        combined_criteria &= crit
    for col in stocks_df.columns.get_level_values(1).unique():
        combined_criteria &= ~stocks_df.xs(col, axis=1, level=1).isna()
    
    stock_list = []
    
    for date, row in combined_criteria.iterrows():
        filtered_stocks = row[row].index.tolist()
        stock_list.append([date, filtered_stocks])
    
    # Convert the list to a DataFrame
    result_df = pd.DataFrame(stock_list, columns=['Date', 'stock_list']).set_index('Date')
    
    return result_df

def process_stock_data_for_day(day, stock_code, all_stocks):
    stock_data = all_stocks.loc[stock_code, day].copy()
    stock_data = stock_data.reset_index()
    stock_data['day'] = day
    stock_data['stock_code'] = stock_code
    return stock_data

def process_filtered_stocks(filtered_stocks_list, all_stocks):
    filtered_stocks_data = []
    for day in filtered_stocks_list.index:
        print(f"Processing day: {day}")
        for stock_code in filtered_stocks_list.loc[day, 'stock_list']:
            stock_data = all_stocks.loc[stock_code, day].copy()
            stock_data = stock_data.reset_index()
            stock_data['day'] = day
            stock_data['stock_code'] = stock_code
            filtered_stocks_data.append(stock_data)
    filtered_stocks_data = pd.concat(filtered_stocks_data, ignore_index=True)
    
    # #######
    # # 定義要處理的任務
    # tasks = []
    # for day in filtered_stocks_list.index:
    #     print(f"Preparing tasks for day: {day}")
    #     for stock_code in filtered_stocks_list.loc[day, 'stock_list']:
    #         tasks.append((day, stock_code))
    
    # # 使用多線程並行處理
    # with ThreadPoolExecutor() as executor:
    #     # 提交任務並收集結果
    #     results = list(executor.map(
    #         lambda task: process_stock_data_for_day(task[0], task[1], all_stocks), tasks
    #         ))
    
    # # 將結果合併
    # filtered_stocks_data = pd.concat(results, ignore_index=True)
    # #######
    
    
    filtered_stocks_data.set_index(['day', 'stock_code', 'ts'], inplace=True)
    filtered_stocks_data = filtered_stocks_data.sort_index()
    return filtered_stocks_data

if __name__ == "__main__":
    # Define file paths
    mid_stocks_list_path = Path('***') # path of 'mid_stocks_list.feather'
    all_stocks_daily_path = Path('***') # path of 'all_stocks_daily.parquet'
    filtered_stocks_list_path = Path('***') # path of 'filtered_stocks_list.parquet'
    
    # Define parameters
    start_date, end_date = '2023-10-01', '2024-10-14'
    top_n = 100
    offset_days = 3
    offset_days_2 = 3
    offset_days_3 = 3
    
    # Load stock lists and data
    mid_stocks_list = pd.read_feather(mid_stocks_list_path)['stock_code'].astype(str).tolist()
    all_stocks_daily = pd.read_parquet(all_stocks_daily_path)
    
    filtered_stocks_df = filter_stocks_by_list(all_stocks_daily, mid_stocks_list)
    
    filtered_stocks_df = filter_stocks_by_trading_days(filtered_stocks_df, start_date, end_date)
    
    # Generate criteria DataFrames
    top_ret_criteria = create_top_ret(filtered_stocks_df, offset_days, top_n)
    new_high_criteria = create_new_high(filtered_stocks_df, offset_days_2)
    vol_amount_criteria = create_filtered_by_vol_and_amount(filtered_stocks_df, offset_days_3)

    # Combine all criteria to find common stocks
    filtered_stocks_list = criterion_to_list(
        filtered_stocks_df,
        top_ret_criteria,
        new_high_criteria,
        vol_amount_criteria
    )
    filtered_stocks_list.to_parquet(filtered_stocks_list_path)
    
    #%%
    filtered_stocks_data_path = Path('/Users/jack/Documents/Quant/Code/TW_stocks/filtered_stocks_data.parquet')
    all_stocks_path = Path('/Users/jack/Documents/Quant/Code/TW_stocks/all_stocks.parquet')
    all_stocks = pd.read_parquet(all_stocks_path)
    filtered_stocks_data = process_filtered_stocks(filtered_stocks_list, all_stocks)
    
    print(filtered_stocks_data)
    filtered_stocks_data.to_parquet(filtered_stocks_data_path)
    
    
    
