import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict
import sys
from pathlib import Path


""" 
Unit test for whole filter file 
execute by : pytest test_filters.py -v
( make sure you cd into the strategy/filters directory )

"""


# Add the project root to Python path to make imports work
project_root = str(Path(__file__).parent.parent.parent)
sys.path.append(project_root)

from strategy.filters.market_filter import MarketFilter
from strategy.filters.price_filter import PriceFilter
from strategy.filters.volume_filter import VolumeFilter
from data.models import Trade, StockData

# Mock Trade and StockData classes if they don't exist yet
if 'Trade' not in globals():
    class Trade:
        def __init__(self, price: float, volume: float, timestamp: datetime, profit: float):
            self.price = price
            self.volume = volume
            self.timestamp = timestamp
            self.profit = profit

if 'StockData' not in globals():
    class StockData:
        def __init__(self, symbol: str, price: float, volume: float, timestamp: datetime):
            self.symbol = symbol
            self.price = price
            self.volume = volume
            self.timestamp = timestamp

# Fixtures for common test data
@pytest.fixture
def sample_market_data():
    dates = pd.date_range(end=datetime.now(), periods=10)
    return pd.DataFrame({
        'date': dates,
        'close': [100, 102, 101, 103, 105, 104, 106, 108, 107, 110],
        'volume': [1000, 1200, 900, 1500, 2000, 1800, 2200, 2500, 2300, 3000],
        'open': [99, 101, 100, 102, 104, 103, 105, 107, 106, 109]
    })

@pytest.fixture
def sample_trades():
    return [
        Trade(price=100, volume=100, timestamp=datetime.now(), profit=50),
        Trade(price=101, volume=150, timestamp=datetime.now(), profit=-20),
        Trade(price=102, volume=200, timestamp=datetime.now(), profit=70)
    ]

@pytest.fixture
def market_filter_params():
    return {
        'volume_threshold': 2000,
        'min_position_factor': 0.5,
        'max_position_factor': 2.0
    }

@pytest.fixture
def price_filter_params():
    return {
        'price_threshold_percentage': 0.1,
        'momentum_threshold': 0.05,
        'breakdown_threshold': -0.03
    }

@pytest.fixture
def volume_filter_params():
    return {
        'min_volume': 1000,
        'min_amount': 100000,
        'volume_surge_ratio': 1.5
    }

# Market Filter Tests
class TestMarketFilter:
    def test_analyze_market_trend(self, sample_market_data, market_filter_params):
        market_filter = MarketFilter(market_filter_params)
        trend = market_filter.analyze_market_trend(sample_market_data, lookback=5)
        assert trend in ['uptrend', 'downtrend', 'neutral']
        
        # Test with uptrend data
        ascending_data = sample_market_data.copy()
        ascending_data['close'] = range(100, 110)
        trend = market_filter.analyze_market_trend(ascending_data, lookback=5)
        assert trend == 'uptrend'

    def test_check_market_volume(self, sample_market_data, market_filter_params):
        market_filter = MarketFilter(market_filter_params)
        result = market_filter.check_market_volume(sample_market_data)
        assert isinstance(result, bool)
        
        # Test with high volume
        high_volume_data = sample_market_data.copy()
        high_volume_data['volume'] = high_volume_data['volume'] * 2
        assert market_filter.check_market_volume(high_volume_data) == True

    def test_check_previous_day_profit(self, sample_trades, market_filter_params):
        market_filter = MarketFilter(market_filter_params)
        result = market_filter.check_previous_day_profit(sample_trades)
        assert isinstance(result, bool)
        
        # Test with all profitable trades
        profitable_trades = [
            Trade(price=100, volume=100, timestamp=datetime.now(), profit=50),
            Trade(price=101, volume=150, timestamp=datetime.now(), profit=30)
        ]
        assert market_filter.check_previous_day_profit(profitable_trades) == True

    def test_calculate_position_factor(self, market_filter_params):
        market_filter = MarketFilter(market_filter_params)
        factor = market_filter.calculate_position_factor('uptrend', 1000.0)
        assert market_filter_params['min_position_factor'] <= factor <= market_filter_params['max_position_factor']

# Price Filter Tests
class TestPriceFilter:
    def test_check_price_level(self, sample_market_data, price_filter_params):
        price_filter = PriceFilter(price_filter_params)
        result = price_filter.check_price_level(
            price=105.0,
            historical_prices=sample_market_data['close']
        )
        assert isinstance(result, bool)
        
        # Test with price within threshold
        avg_price = sample_market_data['close'].mean()
        assert price_filter.check_price_level(avg_price, sample_market_data['close']) == True

    def test_check_price_momentum(self, sample_market_data, price_filter_params):
        price_filter = PriceFilter(price_filter_params)
        current_data = StockData(
            symbol="TEST",
            price=110.0,
            volume=1000,
            timestamp=datetime.now()
        )
        result = price_filter.check_price_momentum(current_data, sample_market_data)
        assert isinstance(result, bool)

    def test_calculate_support_resistance(self, sample_market_data, price_filter_params):
        price_filter = PriceFilter(price_filter_params)
        support, resistance = price_filter.calculate_support_resistance(sample_market_data)
        assert support < resistance
        assert isinstance(support, float)
        assert isinstance(resistance, float)

# Volume Filter Tests
class TestVolumeFilter:
    def test_calculate_estimated_volume(self, sample_market_data, volume_filter_params):
        volume_filter = VolumeFilter(volume_filter_params)
        estimated_volume = volume_filter.calculate_estimated_volume(
            current_volume=1000.0,
            historical_volume=sample_market_data['volume'],
            remaining_minutes=120
        )
        assert estimated_volume > 1000.0
        assert isinstance(estimated_volume, float)

    def test_calculate_volume_profile(self, sample_market_data, volume_filter_params):
        volume_filter = VolumeFilter(volume_filter_params)
        profile = volume_filter.calculate_volume_profile(sample_market_data)
        assert isinstance(profile, pd.DataFrame)
        assert not profile.empty
        assert 'volume' in profile.columns

    def test_check_volume_surge(self, volume_filter_params):
        volume_filter = VolumeFilter(volume_filter_params)
        # Test normal volume (no surge)
        assert volume_filter.check_volume_surge(1000, 1000) == False
        # Test surge volume
        assert volume_filter.check_volume_surge(2000, 1000) == True

    def test_check_minimum_volume(self, volume_filter_params):
        volume_filter = VolumeFilter(volume_filter_params)
        # Test below minimum
        assert volume_filter.check_minimum_volume(500, 50000) == False
        # Test above minimum
        assert volume_filter.check_minimum_volume(1500, 150000) == True

# Integration Tests
def test_filter_integration(
    sample_market_data,
    sample_trades,
    market_filter_params,
    price_filter_params,
    volume_filter_params
):
    """Test all filters working together"""
    market_filter = MarketFilter(market_filter_params)
    price_filter = PriceFilter(price_filter_params)
    volume_filter = VolumeFilter(volume_filter_params)
    
    # Test market filter
    market_results = market_filter.apply_filter(sample_market_data, sample_trades)
    assert isinstance(market_results, dict)
    
    # Test price filter
    current_data = StockData(
        symbol="TEST",
        price=sample_market_data['close'].iloc[-1],
        volume=sample_market_data['volume'].iloc[-1],
        timestamp=datetime.now()
    )
    price_result = price_filter.apply_filter(current_data, sample_market_data)
    assert isinstance(price_result, bool)
    
    # Test volume filter
    volume_result = volume_filter.apply_filter(current_data, sample_market_data)
    assert isinstance(volume_result, bool)