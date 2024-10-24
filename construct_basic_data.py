from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from pathlib import Path
from typing import Tuple
import pandas_market_calendars as mcal

def load_stock_data(
        stock_code: str, 
        file_path: Path, 
        ) -> pd.DataFrame:
    """Read and resample stock data from CSV."""
    stock_df = pd.read_csv(
        file_path,
        parse_dates=['ts'],
        dtype={
            'Open': 'float64',
            'High': 'float64',
            'Low': 'float64',
            'Close': 'float64',
            'Volume': 'int64',
            'Amount': 'float64'
        }
    )
    stock_df.set_index('ts', inplace=True)
    return stock_df
def resample_to_daily(
        stock_code: str,
        stock_df: pd.DataFrame,
        start_date: str, 
        end_date: str
        ) -> pd.DataFrame:
    # Resample to daily frequency and aggregate
    stock_df = stock_df.resample('D').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum',
        'Amount': 'sum'
    })
    
    # Fill missing dates between start_date and end_date with NaN
    trading_days = mcal.get_calendar('XTAI').schedule(
        start_date=start_date, 
        end_date=end_date
        ).index.strftime('%Y-%m-%d')
    stock_df = stock_df.reindex(trading_days)
    stock_df = stock_df.where(stock_df.notna().all(axis=1))
    # Add stock_code as a level in the column index
    stock_df['stock_code'] = stock_code
    stock_df.set_index('stock_code', append=True, inplace=True)
    stock_df = stock_df.reorder_levels(['stock_code', stock_df.index.names[0]])
    return stock_df

def combine_stock_data(
        data_folder: Path, start_date: str, end_date: str
        ) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Combine multiple stock data CSVs into a single DataFrame with MultiIndex columns."""

    all_stocks_daily = []
    all_stocks = []
    
    for csv_file in data_folder.glob('*.csv'):
        stock_code = csv_file.stem  # Use file stem as the stock code
        stock_df = load_stock_data(stock_code, csv_file)
        stock_df_daily = resample_to_daily(stock_code, stock_df, start_date, end_date)
        stock_df['stock_code'] = stock_code
        stock_df.set_index('stock_code', append=True, inplace=True)
        stock_df = stock_df.reorder_levels(['stock_code', stock_df.index.names[0]])
        all_stocks.append(stock_df)
        all_stocks_daily.append(stock_df_daily)
        print(f"Processing stock_code: {stock_code}")
    
    # #############
    # def process_stock(csv_file):
    #     stock_code = csv_file.stem  # Use file stem as the stock code
    #     stock_df = load_stock_data(stock_code, csv_file)
    #     stock_df_daily = resample_to_daily(stock_code, stock_df, start_date, end_date)
    #     stock_df['stock_code'] = stock_code
    #     stock_df.set_index('stock_code', append=True, inplace=True)
    #     stock_df = stock_df.reorder_levels(['stock_code', stock_df.index.names[0]])
    #     return stock_df, stock_df_daily
    
    # # 使用 ThreadPoolExecutor 進行並行處理
    # with ThreadPoolExecutor() as executor:
    #     results = list(executor.map(process_stock, data_folder.glob('*.csv')))
    
    # for stock_df, stock_df_daily in results:
    #     all_stocks.append(stock_df)
    #     all_stocks_daily.append(stock_df_daily)
    # #############

    all_stocks = pd.concat(all_stocks, axis=0)
    all_stocks_daily = pd.concat(all_stocks_daily, axis=0)
    
    return all_stocks.sort_index(), all_stocks_daily.sort_index()

if __name__ == "__main__":
    data_folder = Path('***') # path of 'k_data/永豐'
    all_stocks_path = Path('***') # path of 'all_stocks.parquet'
    all_stocks_daily_path = Path('***') # path of 'all_stocks_daily.parquet'
    start_date, end_date = '2021-01-01', '2024-10-14'

    # Combine all stock data into one DataFrame
    all_stocks, all_stocks_daily = combine_stock_data(data_folder, start_date, end_date)
    print(all_stocks)
    print(all_stocks_daily)
    # Optionally, save the combined DataFrame to a Parquet file
    all_stocks.to_parquet(all_stocks_path)
    all_stocks_daily.to_parquet(all_stocks_daily_path)
