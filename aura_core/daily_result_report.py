import datetime
import logging
import os  # 이 줄이 누락됐었음

def export_daily_summary():
    today = datetime.date.today().isoformat()
    log_path = f"logs/{today}.log"
    
    print("📄 매매 결과 정리 시작")

    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(f"logs/{today}_summary.txt", 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("✅ 매매 요약 저장 완료")
    else:
        print("❌ 로그 파일이 존재하지 않습니다.")

if __name__ == "__main__":
    export_daily_summary()
