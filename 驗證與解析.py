# 程式 Y 的邏輯片段
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

# 內嵌程式 X 提供的公鑰
PUBLIC_KEY_HEX = "400910475e3df32a3dd1abaf484df8197384528e22bb9dc1b593ee91d416b3a3" 
verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY_HEX))

def verify_data(input_series):
    # 假設前 10 個是數字，後面是 Ed25519 的 64 位元組簽章
    random_part = input_series[:10]
    signature_part = bytes(input_series[10:])
    
    data_to_verify = ",".join(map(str, random_part)).encode()
    
    try:
        verify_key.verify(data_to_verify, signature_part)
        return True
    except BadSignatureError:
        return False

print(verify_data([167, 266, 408, 304, 872, 761, 950, 277, 91, 691, 12, 164, 8, 68, 119, 131, 5, 114, 234, 34, 210, 37, 50, 12, 121, 71, 163, 227, 229, 144, 220, 160, 188, 200, 61, 197, 120, 67, 58, 193, 148, 18, 106, 198, 176, 132, 172, 93, 146, 91, 13, 248, 236, 71, 42, 234, 19, 219, 197, 236, 240, 161, 139, 16, 83, 218, 73, 106, 224, 185, 192, 137, 196, 14]))