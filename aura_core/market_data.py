import os
import requests
import yaml
from pathlib import Path
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# 설정 파일 로드
def load_config():
    config_path = Path(__file__).resolve().parents[1] / "config" / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# 토큰 발급 함수
def get_token(kis_conf, mode):
    url = kis_conf['token_url_sim'] if mode == 'sim' else kis_conf['token_url_real']
    headers = {"Content-Type": kis_conf.get("content_type", "application/json")}
    body = {
        "grant_type": kis_conf.get("grant_type", "client_credentials"),
        "appkey": kis_conf['app_key'],
        "appsecret": kis_conf['app_secret']
    }
    res = requests.post(url, headers=headers, json=body)
    return res.json().get("access_token")

# 실시간 시세 조회 함수
def get_market_price(stock_code):
    config = load_config()
    kis_conf = config['kis']
    mode = os.getenv("AURA_MODE", "sim").lower()

    base_url = kis_conf['api_url_sim'] if mode == 'sim' else kis_conf['api_url_real']
    endpoint = "/uapi/domestic-stock/v1/quotations/inquire-price"
    token = get_token(kis_conf, mode)

    headers = {
        "Content-Type": kis_conf.get("content_type", "application/json"),
        "authorization": f"Bearer {token}",
        "appKey": kis_conf['app_key'],
        "appSecret": kis_conf['app_secret'],
        "tr_id": "FHKST01010100" if mode == 'sim' else "HHKST01010100"
    }
    params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": stock_code
    }
    res = requests.get(base_url + endpoint, headers=headers, params=params)
    return res.json()

# 테스트 실행
if __name__ == "__main__":
    result = get_market_price("005930")
    print(result)