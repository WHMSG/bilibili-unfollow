# unfollow.py
import requests
import json
import time
import os
import re
from typing import List, Optional
import random

try:
    import config
except ImportError:
    print("错误：找不到 config.py，请先创建配置文件。")
    exit(1)

# ===== 读取配置 =====
COOKIE = config.COOKIE
UNFOLLOW_URL = config.UNFOLLOW_URL
UNFOLLOW_PARAMS = config.UNFOLLOW_PARAMS
UNFOLLOW_INTERVAL = getattr(config, 'UNFOLLOW_INTERVAL', 2)
MID_FILE = config.MID_FILE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": COOKIE
}
# 合并取关专用的请求头
if hasattr(config, 'UNFOLLOW_HEADERS'):
    for k, v in config.UNFOLLOW_HEADERS.items():
        HEADERS[k] = v

def extract_csrf_from_cookie(cookie_str: str) -> Optional[str]:
    match = re.search(r'bili_jct=([a-f0-9]+)', cookie_str)
    return match.group(1) if match else None

def extract_uid_from_cookie(cookie_str: str) -> Optional[str]:
    match = re.search(r'DedeUserID=(\d+)', cookie_str)
    return match.group(1) if match else None

def unfollow(fid: str, csrf_token: str, uid: str) -> bool:
    # 动态设置 Referer
    headers = HEADERS.copy()
    headers["Referer"] = f"https://space.bilibili.com/{uid}/fans/follow"
    
    data = {
        "act": 2,
        "fid": fid,
        "csrf": csrf_token
    }
    try:
        resp = requests.post(UNFOLLOW_URL, params=UNFOLLOW_PARAMS, data=data, headers=headers, timeout=10)
        result = resp.json()
        if result.get('code') == 0:
            print(f"✅ 取关成功：{fid}")
            return True
        else:
            print(f"❌ 取关失败：{fid}，错误码：{result.get('code')}，消息：{result.get('message')}")
            return False
    except Exception as e:
        print(f"❌ 请求异常：{fid}，{e}")
        return False

def main():
    print("=== 批量取关 B站关注 ===")
    
    # 提取 CSRF
    csrf = extract_csrf_from_cookie(COOKIE)
    if not csrf:
        print("错误：无法从 Cookie 中提取 bili_jct，请确认已登录。")
        return
    print(f"CSRF 令牌: {csrf}")
    
    # 提取 UID（用于 Referer）
    uid = extract_uid_from_cookie(COOKIE)
    if not uid:
        print("警告：无法获取 UID，Referer 可能不正确，但取关仍可能成功。")
        uid = ""
    
    # 读取 mid.txt
    if not os.path.exists(MID_FILE):
        print(f"错误：找不到 {MID_FILE}，请先运行 quguan.py 获取关注列表。")
        return
    
    with open(MID_FILE, "r", encoding="utf-8") as f:
        mids = [line.strip() for line in f if line.strip()]
    
    if not mids:
        print("mid.txt 为空，没有需要取关的用户。")
        return
    
    print(f"共读取到 {len(mids)} 个待取关的 mid\n")
    
    success = 0
    fail = 0
    for idx, fid in enumerate(mids, 1):
        print(f"[{idx}/{len(mids)}] 正在取关 {fid} ...")
        if unfollow(fid, csrf, uid):
            success += 1
        else:
            fail += 1
        time.sleep(random.uniform(5, 8))
    
    print(f"\n===== 取关完成 =====")
    print(f"成功：{success}，失败：{fail}，总计：{len(mids)}")

if __name__ == "__main__":
    main()