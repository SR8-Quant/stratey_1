# database.py 

from typing import Optional, Any, List, Tuple
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import DictCursor
from datetime import datetime
from config.settings import TradingConfig

class DatabaseConnection:
    """Database connection management"""
    
    def __init__(self):
        self._pool: Optional[SimpleConnectionPool] = None
        
    def initialize_pool(self, min_conn: int = 1, max_conn: int = 10) -> None:
        if self._pool is None:
            self._pool = SimpleConnectionPool(
                min_conn,
                max_conn,
                host=TradingConfig.DATABASE["host"],
                port=TradingConfig.DATABASE["port"],
                database=TradingConfig.DATABASE["dbname"],
                user=TradingConfig.DATABASE["user"],
                password=TradingConfig.DATABASE["password"],
                cursor_factory=DictCursor  # 返回 dict 格式的 cursor
            )

    
    def get_connection(self):
        if self._pool:
            return self._pool.getconn()
        else:
            raise ConnectionError("Connection pool is not initialized")

    
    def return_connection(self, conn: Any) -> None:
        if self._pool:
            self._pool.putconn(conn)

    
    def execute_query(
    self,
    query: str,
    params: tuple = None,
    fetch: bool = True
) -> Optional[List[tuple]]:
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
        finally:
            self.return_connection(conn)
            

    def execute_many(
    self,
    query: str,
    params: List[tuple]
) -> None:
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.executemany(query, params)
                conn.commit()
        finally:
            self.return_connection(conn)

    
    def close_all(self) -> None:
        if self._pool:
            self._pool.closeall()




class QueryBuilder:
    """SQL query builder"""
    
    @staticmethod
    def build_stock_query(
        stock_code: str,
        start_date: datetime,
        end_date: datetime
    ) -> Tuple[str, tuple]:
        """Build stock data query"""
        pass
    
    @staticmethod
    def build_market_query(
        start_date: datetime,
        end_date: datetime
    ) -> Tuple[str, tuple]:
        """Build market data query"""
        pass
    
    @staticmethod
    def build_volume_query(
        stock_code: str,
        date: datetime,
        lookback: int
    ) -> Tuple[str, tuple]:
        """Build volume data query"""
        pass
    
    
    
    
    if __name__ == "__main__":
        db = DatabaseConnection()
        db.initialize_pool(min_conn=1, max_conn=10)  # 初始化連接池

        query = "SELECT * FROM some_table WHERE column_name = %s;"
        params = ("some_value",)

        try:
            results = db.execute_query(query, params)
            print("Query Results:", results)
        finally:
            db.close_all()  # 關閉所有連接
