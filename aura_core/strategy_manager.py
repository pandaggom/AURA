import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# 환경 로딩
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# 전략 설정 불러오기
def load_strategy_config():
    path = Path(__file__).resolve().parents[1] / "config" / "strategy.yaml"
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)["strategy"]

strategy_conf = load_strategy_config()

# 단순 매수 전략
def should_buy(current_price, ma5, ma20):
    return current_price > ma5 and current_price > ma20

# 단순 매도 전략
def should_sell(current_price, buy_price):
    profit_threshold = strategy_conf["profit_threshold"]
    loss_threshold = strategy_conf["loss_threshold"]
    profit = (current_price - buy_price) / buy_price
    return profit >= profit_threshold or profit <= -loss_threshold

# 문맥 기반 매도 판단
def should_sell_with_context(current_price, buy_price, indicators):
    profit = (current_price - buy_price) / buy_price
    hold_conditions = strategy_conf["hold_conditions"]

    if profit >= strategy_conf["profit_threshold"]:
        for k, v in hold_conditions["take_profit_hold"].items():
            if indicators.get(k) == v:
                return "hold"
        return "sell"

    elif profit <= -strategy_conf["loss_threshold"]:
        for k, v in hold_conditions["stop_loss_hold"].items():
            if indicators.get(k) == v:
                return "hold"
        return "sell"

    return "hold"

# 보유 유지 판단 (확장 예정)
def should_hold(current_price, conditions):
    return False
