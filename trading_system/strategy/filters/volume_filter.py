from typing import Dict, Any
import pandas as pd
from datetime import datetime
from data.models import StockData

class VolumeFilter:
    """Volume-based filtering"""
    
    def __init__(self, params: Dict[str, Any]):
        self.min_volume = params['min_volume']
        self.min_amount = params['min_amount']
        self.volume_surge_ratio = params['volume_surge_ratio']
        
    def calculate_estimated_volume(
        self,
        current_volume: float,
        historical_volume: pd.Series,
        remaining_minutes: int
    ) -> float:
        """
        實踐估計量 : 目前可以先用XQ估計量 
        XQ估計量 = 開盤迄今實際總量+ 預估單量*離收盤時間
        預估單量= 近期均值(260天均值,收盤時間分割為1分鐘為單位。)

        :param current_volume: Current volume so far.
        :param historical_volume: Historical volume data as a Series.
        :param remaining_minutes: Number of minutes left in the trading session.
        :return: Estimated total volume by end-of-day.
        """
        # TODO:
        # 1. Calculate the average volume per minute from `historical_volume`.
        # 2. Multiply the average volume by `remaining_minutes`.
        # 3. Add the `current_volume` to the projected volume for the remaining minutes.
        # 4. Return the estimated total end-of-day volume.
        pass
    
    def calculate_volume_profile(
        self,
        historical_data: pd.DataFrame
    ) -> pd.DataFrame:
        """
        計算交易量分佈(Volume Profile), 顯示在不同價格區間的交易活躍程度。
        :param historical_data: Historical stock data as a DataFrame.
        :return: A DataFrame with volume profile information.
        """
        # TODO:
        # 1. Group `historical_data` by price levels or intervals.
        # 2. Sum up  total volume traded at each price level.
        # 3. Normalize the volume data if required for better visualization ( optinonal )
        # 4. Return a DataFrame containing the volume profile.
        pass
    
    def check_volume_surge(
        self,
        current_volume: float,
        avg_volume: float
    ) -> bool:
        """
        Check volume surge condition.
        :param current_volume: Current trading volume.
        :param avg_volume: Average historical trading volume.
        :return: True if a volume surge condition is met, otherwise False.
        """
        # TODO:
        # 1. Calculate the ratio of `current_volume` to `avg_volume`.
        # 2. Compare the ratio with `self.volume_surge_ratio`.
        # 3. Return True if the ratio exceeds the surge threshold, otherwise False.
        pass
    
    def check_minimum_volume(
        self,
        volume: float,
        amount: float
    ) -> bool:
        """
        篩掉流動性不足的股票 
        :param volume: Current trading volume.
        :param amount: Current trading amount.
        :return: True if both volume and amount meet the minimum thresholds, otherwise False.
        """
        # TODO:
        # 1. Compare `volume` with `self.min_volume`.
        # 2. Compare `amount` with `self.min_amount`.
        # 3. Return True if both conditions are satisfied, otherwise False.
        pass
    
    def apply_filter(
        self,
        stock_data: StockData,
        historical_data: pd.DataFrame
    ) -> bool:
        """
        Apply all volume filters.
        :param stock_data: Current stock data.
        :param historical_data: Historical stock data.
        :return: True if all volume conditions are satisfied, otherwise False.
        """
        # TODO:
        # 1. Estimate the end-of-day volume using `calculate_estimated_volume`.
        # 2. Check the volume surge condition using `check_volume_surge`.
        # 3. Check the minimum volume condition using `check_minimum_volume`.
        # 4. Combine the results of all filters and return True if all conditions are met.
        pass
