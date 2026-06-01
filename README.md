# bilibili-unfollow
用于b站批量取关，快速清空关注列表

# B站关注列表获取 & 批量取关工具


一个自动化工具，用于**获取B站关注列表中的所有用户id**，并支持**批量取消关注**。配置简单，一键运行，全程自动。

## 功能特性

**自动登录识别**：仅需提供 Cookie，自动提取 UID 和 CSRF 令牌。
**获取关注列表**：分页抓取所有关注用户的 `mid`，保存到 `mid.txt`。
**批量取关**：读取 `mid.txt`，逐个发送取关请求，支持自定义间隔。
**一键执行**：运行 `auto_unfollow.py` 即可自动完成“获取列表 → 批量取关”。也可独立执行各脚本
**模块化设计**：配置、获取、取关脚本分离，便于维护和二次开发。
**详细日志**：控制台实时输出进度，成功/失败一目了然。

文件结构
bili_auto_unfollow/
│
├── config.py # 统一配置文件（用户只需填写 Cookie）
├── quguan.py # 获取关注列表脚本（生成 mid.txt）
├── unfollow.py # 批量取关脚本（读取 mid.txt）
├── auto_unfollow.py # 一键入口脚本（顺序执行上述两个脚本）
├── mid.txt # 自动生成的关注列表（每行一个 mid）
└── README.md


## 🛠️ 使用前准备

1. **安装 Python 3.8+**（[下载地址](https://www.python.org/downloads/)），安装时勾选 “Add Python to PATH”。
2. **安装依赖库**（只需 `requests`）：
   ```
   pip install requests

配置步骤
获取 B站 Cookie：

使用 Chrome/Edge 浏览器登录 B站。

按 F12 打开开发者工具 → 切换到 Network 标签。

刷新页面，找到任意一个 api.bilibili.com 的请求。

在 Request Headers 中找到 Cookie 字段，复制完整的 Cookie 字符串。

填写配置文件：

用文本编辑器打开 config.py。

将复制的 Cookie 粘贴到 COOKIE = "这里填写你的Cookie" 中。

（可选）如需自定义请求间隔、输出文件等，可修改对应的参数。

运行方法
方式一：一键运行（推荐）
在命令行中进入项目目录，执行：

python auto_unfollow.py
脚本将自动完成：

获取所有关注用户的 id → 保存到 mid.txt

逐个取消关注（每个请求间隔 UNFOLLOW_INTERVAL 秒）

方式二：分步运行
仅获取关注列表：
```

python quguan.py
```

仅执行取关（需已有 mid.txt）：
```

python unfollow.py
```

 注意事项
Cookie 有效期：Cookie 会过期，如果脚本报错（如 -101），请重新复制最新的 Cookie。

风控风险：批量取关可能触发 B站 的风控机制（错误码 -352）。建议：

设置 time.sleep(random.uniform(5, 8))   为 5~8 秒或更长。

分批运行，不要一次性取关数百个用户。

引入随机延迟（可在 unfollow.py 中修改）。

账号安全：本脚本仅在你本地运行，不会上传任何数据。但请不要将包含真实 Cookie 的 config.py 分享或上传到公开仓库。

仅用于学习：请合理使用，遵守 B站 用户协议。
