# 程式 Y 的邏輯片段
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

# 內嵌程式 X 提供的公鑰
PUBLIC_KEY_HEX = "..." 
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