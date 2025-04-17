import os
import requests
import yaml
from pathlib import Path

# 설정 로드 함수
def load_config():
    config_path = Path(__file__).resolve().parents[1] / "config" / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# KIS 토큰 요청 함수
def get_kis_token():
    config = load_config()
    mode = os.getenv("AURA_MODE", "sim").lower()
    kis_key = 'REAL' if mode == 'real' else 'SIM'

    kis_conf = config['kis']
    app_key = os.getenv(f"{kis_key}_APP_KEY", kis_conf['app_key'])
    app_secret = os.getenv(f"{kis_key}_APP_SECRET", kis_conf['app_secret'])

    token_url = kis_conf['token_url_real'] if mode == 'real' else kis_conf['token_url_sim']
    grant_type = kis_conf.get('grant_type', 'client_credentials')
    content_type = kis_conf.get('content_type', 'application/json')

    headers = {"Content-Type": content_type}
    body = {
        "grant_type": grant_type,
        "appkey": app_key,
        "appsecret": app_secret
    }

    res = requests.post(token_url, headers=headers, json=body)
    return res.json()

if __name__ == "__main__":
    token_info = get_kis_token()
    print(token_info)
