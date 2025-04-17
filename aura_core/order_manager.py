import json
import os
import yaml
from datetime import datetime
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from dotenv import load_dotenv

matplotlib.rcParams['font.family'] = 'Malgun Gothic'

# 환경 변수 로드
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# config.yaml 경로 지정 및 설정 파일 로드
def load_config():
    config_path = Path(__file__).resolve().parents[1] / "config" / "config.yaml"
    with open(config_path, encoding='utf-8') as f:
        raw = yaml.safe_load(f)
    mode = os.getenv("AURA_MODE", "sim").lower()
    kis_key = 'REAL' if mode == "real" else 'SIM'

    return {
        'APP_KEY': os.getenv(f"{kis_key}_APP_KEY", raw['kis']['app_key']),
        'APP_SECRET': os.getenv(f"{kis_key}_APP_SECRET", raw['kis']['app_secret']),
        'ACCOUNT': os.getenv(f"{kis_key}_ACCOUNT", raw['kis']['account'])
    }

config = load_config()

# 로그 파일 경로: logs/YYYYMMDD_aura_log.json
log_dir = Path(__file__).resolve().parents[1] / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"{os.getenv('AURA_LOG_DATE', datetime.now().strftime('%Y%m%d'))}_aura_log.json"

# 로그 로드 함수
def load_logs():
    if not log_file.exists():
        print("[PROFIT SIM] 로그 파일이 없습니다.")
        return pd.DataFrame()

    with open(log_file, "r", encoding="utf-8") as f:
        lines = [json.loads(line) for line in f if line.strip()]
    return pd.DataFrame(lines)

# 수익 시뮬레이션 함수
def simulate_profit(df, quantity=10):
    if df.empty:
        print("[PROFIT SIM] 데이터가 없습니다.")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.drop_duplicates(subset="timestamp", inplace=True)
    df = df.sort_values("timestamp")
    df["profit"] = 0
    df["position_price"] = None
    df["position_time"] = None
    position = None
    buy_time = None
    cumulative_profit = []
    total_profit = 0

    for idx, row in df.iterrows():
        decision = row["decision"]
        price = row["price"]

        if decision == "buy" and position is None:
            position = price
            buy_time = row["timestamp"]
            df.at[idx, "position_price"] = price
            df.at[idx, "position_time"] = buy_time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"[BUY] {buy_time.strftime('%Y-%m-%d %H:%M:%S')}에 {price}원에 매수")

        elif decision == "sell" and position is not None:
            profit = (price - position) * quantity
            total_profit += profit
            print(f"[SELL] {row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}에 {price}원에 매도 → 수익: {profit:,.0f}원")
            position = None
            df.at[idx, "profit"] = profit

        cumulative_profit.append(total_profit)

    if len(cumulative_profit) != len(df):
        print("[WARNING] 누적 수익 배열 길이가 로그 수와 일치하지 않습니다. 자동 보정합니다.")
        while len(cumulative_profit) < len(df):
            cumulative_profit.append(total_profit)
        cumulative_profit = cumulative_profit[:len(df)]

    df["cumulative"] = cumulative_profit
    print(f"\n💰 누적 수익: {total_profit:,.0f}원")

    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["cumulative"], marker='o', linestyle='-')
    plt.title("AURA 전략 누적 수익률 추이")
    plt.xlabel("시간")
    plt.ylabel("누적 수익 (₩)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 메인 함수
def main():
    df = load_logs()
    simulate_profit(df)

if __name__ == "__main__":
    main()
