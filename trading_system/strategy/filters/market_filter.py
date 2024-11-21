from typing import Dict, Optional, Any, List
import pandas as pd
from datetime import datetime
from data.models import Trade

class MarketFilter:
    """Market condition filtering"""
    
    def __init__(self, params: Dict[str, Any]):
        self.params = params
        
    def analyze_market_trend(
        self,
        market_data: pd.DataFrame,
        lookback: int = 5
    ) -> str:
        """
        主要功能: for 後面func
        Analyze market trend.  # 分析市場近期趨勢 （例：創三天新高）
        :param market_data: A DataFrame containing market data.
        :param lookback: The number of days to look back for trend analysis.
        :return: A string indicating the trend (e.g., 'uptrend', 'downtrend', 'neutral').
        """
        # TODO:
        # 1. Extract the closing prices from the `market_data` DataFrame.
        # 2. Calculate the average closing price over the last `lookback` days.
        # 3. Compare this average to the previous period's average.
        # 4. Return 'uptrend', 'downtrend', or 'neutral' based on the comparison.
        pass
    
    def check_market_volume(
        self,
        market_data: pd.DataFrame
    ) -> bool:     
        """
        Check market volume condition.  # 看是否爆大量 
        :param market_data: A DataFrame containing market data.
        :return: True if the volume condition is met, otherwise False.
        """
        # TODO:
        # 1. Extract the volume data from the `market_data` DataFrame.
        # 2. Retrieve the volume threshold from `self.params`.
        # 3. Compare the current volume to the threshold.
        # 4. Return True if the current volume meets or exceeds the threshold.
        pass
    
    def check_previous_day_profit(
        self,
        trades: List[Trade]
    ) -> bool:
        """
        (OPTIONAL)
        Check previous day's trading profit.     
        :param trades: A list of Trade objects from the previous day.
        :return: True if the previous day was profitable, otherwise False.
        # 需要修改
        """
        # TODO:
        # 1. Iterate through the list of `trades` to calculate total profit.
        # 2. Subtract all costs (e.g., commissions, slippage) from the total profit.
        # 3. Check if the resulting profit is greater than 0.
        # 4. Return True if profitable, otherwise False.
        pass
    
    def calculate_position_factor(
        self,
        market_condition: str,
        previous_profit: float
    ) -> float:
        """
        Calculate position size factor.
        :param market_condition: The current market condition (e.g., 'uptrend', 'downtrend').
        :param previous_profit: The profit from the previous day.
        :return: A factor for adjusting position size.
        """
        # TODO:
        # 1. Use the `market_condition` to determine a base factor (e.g., 1.0 for neutral, 1.2 for uptrend).
        # 2. Adjust the factor based on the `previous_profit` (e.g., scale up if profit is high).
        # 3. Ensure the factor stays within a defined range (e.g., min and max values from `self.params`).
        # 4. Return the calculated position size factor.
        pass
    
    def apply_filter(
        self,
        market_data: pd.DataFrame,
        trades: List[Trade]
    ) -> Dict[str, Any]:
        """
        Apply all market filters.
        :param market_data: A DataFrame containing market data.
        :param trades: A list of Trade objects.
        :return: A dictionary summarizing the results of all applied filters.
        """
        # TODO:
        # 1. Analyze the market trend using `analyze_market_trend`.
        # 2. Check the market volume condition using `check_market_volume`.
        # 3. Evaluate the previous day's profit using `check_previous_day_profit`.
        # 4. Calculate the position factor using `calculate_position_factor`.
        # 5. Combine all the results into a dictionary and return it.
        pass
