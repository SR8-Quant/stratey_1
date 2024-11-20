# config/__init__.py

import os
from pathlib import Path
from .settings import TradingConfig
from .logging_config import LoggerConfig

class ConfigurationManager:
    """配置管理器"""
    
    def __init__(self):
        # 獲取環境設定
        self.env = os.getenv('TRADING_ENV', 'development')
        
        # 設定路徑
        self.root_dir = Path(__file__).parent.parent
        self.log_dir = self.root_dir / "logs" / self.env
        
        # 確保日誌目錄存在
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化日誌
        LoggerConfig.setup_logging(self.log_dir)
        self.logger = LoggerConfig.get_logger("trading_system")
        
        # 初始化配置
        self.config = TradingConfig()
        
        # 記錄初始化信息
        self._log_startup_info()
    
    def _log_startup_info(self):
        """記錄啟動信息"""
        self.logger.info(f"Trading system initializing in {self.env} environment")
        self.logger.info(f"Root directory: {self.root_dir}")
        self.logger.info(f"Log directory: {self.log_dir}")
        
    @property
    def version(self):
        return '1.0.0'

# 創建全局配置管理器實例
config_manager = ConfigurationManager()

# 導出常用對象和屬性
config = config_manager.config
logger = config_manager.logger
root_dir = config_manager.root_dir
log_dir = config_manager.log_dir

__all__ = [
    'ConfigurationManager',  # 添加 ConfigurationManager 到導出列表
    'TradingConfig',
    'LoggerConfig',
    'config',
    'logger',
    'root_dir',
    'log_dir',
    'config_manager'
]

__version__ = config_manager.version