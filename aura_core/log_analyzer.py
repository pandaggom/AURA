import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
from dotenv import load_dotenv

# 한글 폰트 설정
matplotlib.rcParams['font.family'] = 'Malgun Gothic'

# 환경변수 로드
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# 날짜 기반 로그 파일 설정
log_dir = Path(__file__).resolve().parents[1] / "logs"
log_file = log_dir / f"{os.getenv('AURA_LOG_DATE', '')}_aura_log.json"

# 로그 로드 함수
def load_logs():
    if not log_file.exists():
        print("[LOG VIEWER] 로그 파일이 없습니다.")
        return pd.DataFrame()

    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        entries = [json.loads(line) for line in lines if line.strip()]
    return pd.DataFrame(entries)

# 가격 시각화 함수
def plot_price_trend(df):
    if df.empty:
        return
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")
    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["price"], marker='o', linestyle='-')
    plt.title("AURA 전략 실행 시점별 현재가")
    plt.xlabel("시간")
    plt.ylabel("현재가")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 판단 통계 출력 함수
def count_decisions(df):
    if df.empty:
        return
    counts = df["decision"].value_counts()
    print("\n\ud83d\udcca 전략 판단 통계:")
    for decision, count in counts.items():
        print(f"- {decision}: {count}회")

# 메인 함수
def main():
    df = load_logs()
    count_decisions(df)
    plot_price_trend(df)

if __name__ == "__main__":
    main()
