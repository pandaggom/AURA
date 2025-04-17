import datetime
import time
import subprocess
import os

TARGET_SCRIPT = "python aura_core/auto_runner.py"
RESULT_SCRIPT = "python aura_core/daily_result_report.py"

START_TIME = datetime.time(hour=9, minute=0)
END_TIME = datetime.time(hour=15, minute=40)
RESULT_TIME = datetime.time(hour=15, minute=33)

has_executed = False
has_reported = False

def now():
    return datetime.datetime.now()

def run_script(cmd, tag="실행"):
    print(f"🚀 {tag} 시작: {cmd}")
    subprocess.call(cmd, shell=True)
    print(f"✅ {tag} 완료.")

def main():
    global has_executed, has_reported  # ⬅️ 반드시 함수 처음에 선언해줘야 오류 안남
    print("⏰ AURA 자동 스케줄러 시작")
    while True:
        current = now().time()

        if START_TIME <= current <= END_TIME and not has_executed:
            run_script(TARGET_SCRIPT, tag="모의매매")
            has_executed = True

        if current >= RESULT_TIME and not has_reported:
            run_script(RESULT_SCRIPT, tag="매매결과 리포트")
            has_reported = True

        if current >= END_TIME:
            print("🛑 시장 종료. 스케줄러 종료.")
            break

        time.sleep(30)

if __name__ == "__main__":
    main()
