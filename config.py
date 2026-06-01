# config.py
# 用户只需要填写 Cookie 即可，其他参数保持默认

# ========== 必填 ==========
# 从浏览器复制的完整 Cookie 字符串（必须包含 DedeUserID 和 bili_jct）
COOKIE = ""

# ========== 可选 ==========
# 你的 B站 UID，如果不填会自动从 Cookie 中的 DedeUserID 提取
VMID = ""

# 请求间隔（秒），避免风控
REQUEST_INTERVAL = 1
UNFOLLOW_INTERVAL = 2

# 以下参数一般不需要修改
# 关注列表接口
FOLLOWINGS_URL = "https://api.bilibili.com/x/relation/followings"
FOLLOWINGS_PARAMS = {
    "order": "desc",
    "order_type": "",
    "ps": 24,               # 每页数量，最大50
    "gaia_source": "main_web",
    "web_location": "333.1387"
}

# 取关接口
UNFOLLOW_URL = "https://api.bilibili.com/x/relation/modify"
UNFOLLOW_PARAMS = {
    "statistics": '{"appId":100,"platform":5}',
    "x-bili-device-req-json": '{"platform":"web","device":"pc","spmid":"333.1387"}'
}
UNFOLLOW_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "https://space.bilibili.com/"  # 后面会动态拼接 UID
}

# 输出文件
MID_FILE = "mid.txt"