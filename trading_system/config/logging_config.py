import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class LoggerConfig:
    """Logging configuration"""
    
    @staticmethod
    def setup_logging(log_dir: Path) -> None:
        """Setup logging configuration"""
        # 確保日誌目錄存在
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # 設置日誌文件名(使用日期)
        log_file = log_dir / f"trading_{datetime.now().strftime('%Y%m%d')}.log"
        
        # 設置日誌格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # 設置文件處理器
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        
        # 設置控制台處理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # 配置根日誌記錄器
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get logger instance"""
        logger = logging.getLogger(name)
        if not logger.handlers:  # 如果logger還沒有被配置
            logger.setLevel(logging.INFO)
        return logger
    
    @staticmethod
    def log_trade(logger: logging.Logger, trade_info: Dict[str, Any]) -> None:
        """Log trade information"""
        try:
            # 格式化交易信息
            trade_msg = (
                f"Trade executed: "
                f"Type={trade_info.get('type', 'N/A')} | "
                f"Symbol={trade_info.get('symbol', 'N/A')} | "
                f"Price={trade_info.get('price', 0.0)} | "
                f"Quantity={trade_info.get('quantity', 0.0)} | "
                f"Total={trade_info.get('price', 0.0) * trade_info.get('quantity', 0.0):.2f}"
            )
            logger.info(trade_msg)
            
            # 可以添加更詳細的DEBUG級別日誌
            logger.debug(f"Complete trade info: {trade_info}")
            
        except Exception as e:
            logger.error(f"Error logging trade: {str(e)}")
            
            
# if __name__ == "__main__":
#     try:
#         # 1. 測試基本配置
#         log_dir = Path("test_logs")
#         LoggerConfig.setup_logging(log_dir)
#         print(f"Log directory created at: {log_dir.absolute()}")
        
#         # 2. 測試獲取logger
#         test_logger = LoggerConfig.get_logger("test_trading")
#         print("Logger created successfully")
        
#         # 3. 測試記錄不同類型的交易
#         # 測試買入交易
#         buy_trade = {
#             "type": "BUY",
#             "symbol": "BTC/USDT",
#             "price": 50000.0,
#             "quantity": 0.1,
#             "timestamp": datetime.now().isoformat()
#         }
#         LoggerConfig.log_trade(test_logger, buy_trade)
        
#         # 測試賣出交易
#         sell_trade = {
#             "type": "SELL",
#             "symbol": "ETH/USDT",
#             "price": 3000.0,
#             "quantity": 1.5,
#             "timestamp": datetime.now().isoformat()
#         }
#         LoggerConfig.log_trade(test_logger, sell_trade)
        
#         # 4. 測試錯誤情況
#         invalid_trade = {
#             "type": "INVALID",
#             # 缺少必要欄位
#         }
#         LoggerConfig.log_trade(test_logger, invalid_trade)
        
#         print("All tests completed successfully!")
        
#         # 5. 顯示日誌文件內容
#         log_files = list(log_dir.glob("*.log"))
#         if log_files:
#             latest_log = max(log_files, key=lambda x: x.stat().st_mtime)
#             print(f"\nContent of the latest log file ({latest_log.name}):")
#             print("-" * 50)
#             with open(latest_log, 'r') as f:
#                 print(f.read())
        
#     except Exception as e:
#         print(f"Error during testing: {str(e)}")
#     finally:
#         # 清理測試文件（可選）
#         # import shutil
#         # shutil.rmtree(log_dir, ignore_errors=True)
#         pass