# main.py
import threading
import time
import subprocess
import sys
import os

def start_worker():
    """
    启动你现有的程序逻辑
    """
    try:
        # 示例：如果你是 Go 二进制
        binary_path = os.path.join(os.path.dirname(__file__), "ech-wk")
        if os.path.exists(binary_path):
            subprocess.Popen([binary_path])
        else:
            print("Worker binary not found:", binary_path)
    except Exception as e:
        print("Worker start failed:", e)

if __name__ == "__main__":
    t = threading.Thread(target=start_worker, daemon=True)
    t.start()

    # 防止 Python 进程立刻退出
    while True:
        time.sleep(60)
