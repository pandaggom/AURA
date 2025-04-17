import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# 상대경로로 모듈 인식
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from aura_core.market_data import get_market_price
from aura_core.strategy_manager import should_sell_with_context
from aura_core.order_manager import place_order
from aura_core import logger

def run_once():
    stock_code = os.getenv("AURA_STOCK_CODE", "005930")
    buy_price = int(os.getenv("AURA_BUY_PRICE", 53500))
    quantity = int(os.getenv("AURA_QUANTITY", 10))

    indicators = {
        "체결강도": "강함",
        "외국인수급": "매수우세",
        "뉴스": "긍정",
        "공매도": "감소",
        "거래량": "폭증"
    }

    try:
        response = get_market_price(stock_code)
        current_price = int(response["output"]["stck_prpr"])
    except Exception as e:
        print(f"[ERROR] 시세 조회 실패: {e}")
        return None

    decision = should_sell_with_context(current_price, buy_price, indicators)

    if decision == "sell":
        result = place_order("sell", stock_code, quantity, current_price)
    elif decision == "buy":
        result = place_order("buy", stock_code, quantity, current_price)
    else:
        result = {"status": "보유 유지", "current_price": current_price}

    print("\n📌 판단 결과:", decision)
    print("📝 주문 처리 결과:", result)

    return {
        "decision": decision,
        "price": current_price,
        "result": result
    }

if __name__ == "__main__":
    result = run_once()
    if result:
        logger.log_result(result)
