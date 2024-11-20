from typing import Dict, Optional, Tuple, Any
import pandas as pd
from datetime import datetime
from data.models import StockData


"""
針對叔叔想法，這個檔案需要修改  
"""




class PriceFilter:
    """Price-based filtering"""
    
    def __init__(self, params: Dict[str, Any]):
        self.params = params
        
    def check_price_level(
        self,
        price: float,
        historical_prices: pd.Series
    ) -> bool:
        """
        Check price level condition: 查看現價是否在合理價格範圍內 
        :param price: Current price.
        :param historical_prices: A Series of historical prices.
        :return: True if price level condition is met, otherwise False.
        """
        # TODO:
        # 1. Calculate the average historical price from `historical_prices`.
        # 2. Retrieve the threshold percentage from `self.params`.
        # 3. Check if the `price` is within the acceptable range around the average.
        # 4. Return True if the condition is met, otherwise False.
        pass
    
    def check_price_momentum(
        self,
        current_data: StockData,
        historical_data: pd.DataFrame
    ) -> bool:
        """
        Check price momentum condition.
        :param current_data: The current stock data.
        :param historical_data: A DataFrame of historical stock data.
        :return: True if momentum condition is met, otherwise False.
        """
        # TODO:
        # 1. Calculate the price momentum (e.g., the rate of change in closing prices).
        # 2. Compare the momentum to the threshold defined in `self.params`.
        # 3. Check if the momentum is positive and strong enough to meet the condition.
        # 4. Return True if the condition is met, otherwise False.
        pass
    
    def check_breakdown_condition(
        self,
        price: float,
        open_price: float
    ) -> bool:
        """
        Check price breakdown condition.
        :param price: Current price.
        :param open_price: Opening price.
        :return: True if breakdown condition is met, otherwise False.
        """
        # TODO:
        # 1. Calculate the percentage difference between `price` and `open_price`.
        # 2. Retrieve the breakdown threshold from `self.params`.
        # 3. Check if the price has dropped below the acceptable threshold.
        # 4. Return True if the condition is met, otherwise False.
        pass
    
    def calculate_support_resistance(
        self,
        historical_data: pd.DataFrame
    ) -> Tuple[float, float]:
        """
        功能：計算支撐、阻力線
        Calculate support and resistance levels.
        :param historical_data: A DataFrame of historical stock data.
        :return: A tuple containing the support and resistance levels.
        """
        # TODO:
        # 1. Identify the lowest and highest prices from `historical_data`.
        # 2. Calculate support as a certain percentage above the lowest price.
        # 3. Calculate resistance as a certain percentage below the highest price.
        # 4. Return the calculated support and resistance levels as a tuple.
        pass
    
    def apply_filter(
        self,
        stock_data: StockData,
        historical_data: pd.DataFrame
    ) -> bool:
        """
        Apply all price filters.
        :param stock_data: Current stock data.
        :param historical_data: A DataFrame of historical stock data.
        :return: True if all filters are passed, otherwise False.
        """
        # TODO:
        # 1. Check price level using `check_price_level`.
        # 2. Check price momentum using `check_price_momentum`.
        # 3. Check breakdown condition using `check_breakdown_condition`.
        # 4. Combine the results of all filters and return True if all conditions are met.
        pass
