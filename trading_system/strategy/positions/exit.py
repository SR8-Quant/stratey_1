from typing import Dict, Optional, List, Any
from datetime import datetime
from data.models import Position, Trade, StockData
from strategy.risk_management.stop_loss import StopLossManager

class ExitStrategy:
    """Exit strategy implementation"""
    
    def __init__(self, params: Dict[str, Any], stop_loss_manager: StopLossManager):
        self.params = params
        self.stop_loss_manager = stop_loss_manager
        
    def check_exit_time(
        self,
        current_time: datetime,
        position: Position
    ) -> bool:
        """
        Check if current time is valid for exit. ( 後5min不進場 )
        :param current_time: The current timestamp.
        :param position: The position being evaluated for exit.
        :return: True if the current time allows an exit, otherwise False.
        """
        # TODO:
        # 1. Retrieve allowed exit time range from `self.params`.
        # 2. Check if `current_time` falls within the allowed range.
        # 3. Consider position-specific or market-specific timing rules.
        # 4. Return True if conditions are met, otherwise False.
        pass
    
    
    def check_stop_loss(
        self,
        position: Position,
        current_price: float
    ) -> bool:
        """
        Check if stop loss is triggered using StopLossManager.
        :param position: The position being evaluated.
        :param current_price: The current price of the stock.
        :return: True if the stop loss is triggered, otherwise False.
        """
        # TODO:
        # 1. Use `self.stop_loss_manager.check_stop_triggered` to evaluate stop-loss conditions.
        # 2. Pass the current `position` and `current_price` to the manager.
        # 3. Return True if the stop loss is triggered, otherwise False.
        pass
    
    
    def calculate_exit_price(
        self,
        position: Position,
        stock_data: StockData
    ) -> float:
        """
        計算預期出場價格--> 用於掛限價單
        Calculate exit price using StopLossManager.
        :param position: The position being evaluated.
        :param stock_data: Stock data containing historical and current prices.
        :return: The calculated exit price.
        """
        # TODO:
        # 1. For stop-loss exits, use `self.stop_loss_manager.calculate_trailing_stop`.
        # 2. Adjust the exit price based on stock volatility or market conditions.
        # 3. Return the calculated exit price.
        pass
    
    def generate_exit_signals(
        self,
        positions: Dict[str, Position],
        stock_data: Dict[str, StockData]
    ) -> List[Trade]:
        """
        Generate exit signals for all positions.
        :param positions: A dictionary of active positions, keyed by stock symbol.
        :param stock_data: A dictionary of stock data, keyed by stock symbol.
        :return: A list of Trade objects representing exit signals.
        """
        # TODO:
        # 1. Iterate through all `positions` and retrieve corresponding `stock_data`.
        # 2. Check each position for stop loss conditions.
        # 3. Use `calculate_exit_price` to determine the best exit price.
        # 4. Create and append Trade objects for positions requiring an exit.
        # 5. Return a list of Trade objects.
        pass
