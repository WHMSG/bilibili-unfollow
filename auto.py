# auto_unfollow.py
import subprocess
import sys
import os

def run_script(script_name):
    print(f"\n>>> 正在运行 {script_name} ...")
    result = subprocess.run([sys.executable, script_name], capture_output=False)
    if result.returncode != 0:
        print(f"错误：{script_name} 执行失败，退出码 {result.returncode}")
        sys.exit(1)
    print(f"<<< {script_name} 完成")

if __name__ == "__main__":
    print("=== B站一键取关工具 ===")
    # 1. 获取关注列表
    run_script("getmid.py")
    # 2. 批量取关
    run_script("quguan.py")
    print("\n全部完成！")