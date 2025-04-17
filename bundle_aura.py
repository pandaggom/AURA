import zipfile, os
from datetime import datetime

# 압축 대상 파일 (경로 수정 포함)
files = [
    ".env",
    "config/config.yaml",
    "config/strategy.yaml",
    "aura_core/core_runner.py",
    "aura_core/strategy_manager.py",
    "aura_core/market_data.py",
    "aura_core/order_manager.py",
    "aura_core/auth_manager.py",
    "aura_core/logger.py",
    "aura_core/log_analyzer.py",
    "aura_core/auto_runner.py",
    "aura_core/profit_simulator.py"
]

# 압축 결과 저장 폴더
output_dir = "temp_bundle"
os.makedirs(output_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
zipname = f"{output_dir}/aura_bundle_{timestamp}.zip"

with zipfile.ZipFile(zipname, 'w') as zipf:
    for f in files:
        if os.path.exists(f):
            zipf.write(f)
        else:
            print(f"[WARN] 파일 없음: {f}")

print(f"✅ 압축 완료: {zipname}")
