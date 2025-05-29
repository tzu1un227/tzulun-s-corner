import socket

try:
    s = socket.socket()
    s.settimeout(5)  # 最多等 5 秒
    s.connect(("irl-svr.ee.yzu.edu.tw", 80))
    print("✅ 連線成功")
except socket.timeout:
    print("❌ 連線超時（timeout）")
except socket.error as e:
    print(f"❌ 連線失敗：{e}")
finally:
    s.close()
