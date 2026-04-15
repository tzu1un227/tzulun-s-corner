# 程式 X 的邏輯片段
import secrets
from nacl.signing import SigningKey

# 生成金鑰對（僅需生成一次，私鑰保密，公鑰給程式 Y）
signing_key = SigningKey.generate()
verify_key = signing_key.verify_key
print(verify_key.encode().hex())

# 1. 生成隨機數列
random_numbers = [secrets.randbelow(1000) for _ in range(10)]
data_to_sign = ",".join(map(str, random_numbers)).encode()

# 2. 進行簽署
signature = signing_key.sign(data_to_sign).signature

# 3. 輸出包含簽章的數列（將簽章也轉換為數字方便混合）
output_series = random_numbers + list(signature)
print(output_series)