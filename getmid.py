# quguan.py
import requests
import json
import time
import os
import re
from typing import List, Optional

try:
    import config
except ImportError:
    print("错误：找不到 config.py，请先创建配置文件。")
    exit(1)

# ===== 读取配置 =====
COOKIE = config.COOKIE
VMID = getattr(config, 'VMID', '')
REQUEST_INTERVAL = getattr(config, 'REQUEST_INTERVAL', 1)
FOLLOWINGS_URL = config.FOLLOWINGS_URL
FOLLOWINGS_PARAMS = config.FOLLOWINGS_PARAMS.copy()
MID_FILE = config.MID_FILE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com/",
    "Cookie": COOKIE
}

def extract_uid_from_cookie(cookie_str: str) -> Optional[str]:
    match = re.search(r'DedeUserID=(\d+)', cookie_str)
    return match.group(1) if match else None

def fetch_followings(params: dict, headers: dict) -> Optional[dict]:
    try:
        print(f"正在请求：第 {params.get('pn', 1)} 页，每页 {params.get('ps', 24)} 条...")
        response = requests.get(FOLLOWINGS_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('code') != 0:
            print(f"API 返回错误: code={data.get('code')}, message={data.get('message')}")
            return None
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def extract_mids_from_data(data: dict) -> List[int]:
    mids = []
    if data and 'data' in data and 'list' in data['data']:
        for item in data['data']['list']:
            if 'mid' in item:
                mids.append(item['mid'])
    return mids

def save_mids_to_file(mids: List[int], filename: str):
    with open(filename, 'a', encoding='utf-8') as f:
        for mid in mids:
            f.write(str(mid) + '\n')

def main():
    print("=== 获取B站关注列表 mid ===")
    
    # 确定 UID
    uid = VMID if VMID else extract_uid_from_cookie(COOKIE)
    if not uid:
        print("错误：无法获取 UID，请检查 Cookie 中是否包含 DedeUserID，或在 config.py 中手动填写 VMID")
        return
    print(f"用户 ID: {uid}")
    FOLLOWINGS_PARAMS['vmid'] = uid
    
    # 清空输出文件
    if os.path.exists(MID_FILE):
        os.remove(MID_FILE)
    
    all_mids = []
    current_page = 1
    
    while True:
        FOLLOWINGS_PARAMS['pn'] = current_page
        data = fetch_followings(FOLLOWINGS_PARAMS, HEADERS)
        if data is None:
            break
        
        mids = extract_mids_from_data(data)
        if not mids:
            break
        
        save_mids_to_file(mids, MID_FILE)
        all_mids.extend(mids)
        print(f"第 {current_page} 页提取到 {len(mids)} 个 mid")
        
        if len(mids) < FOLLOWINGS_PARAMS.get('ps', 24):
            break
        
        time.sleep(REQUEST_INTERVAL)
        current_page += 1
    
    print(f"\n总计提取到 {len(all_mids)} 个 mid，已保存到 {MID_FILE}")

if __name__ == "__main__":
    main()