import secrets
import struct
import base64
from nacl.signing import SigningKey
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

def generate_key_pair():
    """
    產生基於 Ed25519 演算法的簽名金鑰對。
    
    :return: 包含 (私鑰 hex 字串, 公鑰 hex 字串) 的 Tuple 型態
    """
    signing_key = SigningKey.generate()
    # 同時產生並回傳私鑰與公鑰 (打包為 Tuple)
    return signing_key.encode().hex(), signing_key.verify_key.encode().hex()

def generate_signed_numbers(private_key_hex):
    """
    產生 10 個隨機數字 (各 2 bytes)，並使用給定的私鑰對其進行數位簽名以防偽造。
    將本文 (20 bytes) 與簽章 (64 bytes) 合併後進行 Base64 編碼，以縮小 QR Code 尺寸。
    
    :param private_key_hex: 16 進位格式的字串私鑰
    :return: Base64 編碼的字串 (約 112 bytes)
    """
    signing_key = SigningKey(bytes.fromhex(private_key_hex))
    
    # 產生 10 個 2 bytes 的隨機數字 (0~65535)
    random_numbers = [secrets.randbelow(65536) for _ in range(10)]
    
    # 將數字打包為 20 bytes 的二進位資料 (Little-endian, unsigned short)
    data_to_sign = struct.pack('<10H', *random_numbers)
    
    # 進行簽名
    signed_message = signing_key.sign(data_to_sign)
    signature_bytes = signed_message.signature
    
    # 組合本文與簽章，共 84 bytes
    payload = data_to_sign + signature_bytes
    
    # 採用 Base64 編碼成 ASCII 字串
    return base64.b64encode(payload).decode('ascii')

def verify_data(payload_b64, public_key_hex):
    """
    使用給定的公鑰，驗證接收到的 Base64 簽章資料是否正確，以確認資料未遭竄改。
    
    :param payload_b64: 以 Base64 編碼的字串，包含 20 bytes 本文與 64 bytes 簽章
    :param public_key_hex: 16 進位格式的字串公鑰
    :return: bool，若簽章驗證成功回傳 True，簽章不符或發生例外則回傳 False
    """
    verify_key = VerifyKey(bytes.fromhex(public_key_hex))
    
    try:
        # 解碼 Base64 資料
        payload = base64.b64decode(payload_b64)
        
        # 驗證長度是否為 84 bytes (20 bytes 本文 + 64 bytes 簽章)
        if len(payload) != 84:
            return False
            
        # 前 20 bytes 是數字的二進位資料，後面是 Ed25519 的 64 位元組簽章
        data_to_verify = payload[:20]
        signature_part = payload[20:]
        
        verify_key.verify(data_to_verify, signature_part)
        return True
    except BadSignatureError:
        return False
    except Exception:
        return False


# === 主程式測試 ===
if __name__ == "__main__":
    # 1. 產生金鑰對
    print("--- 1. 產生金鑰對 ---")
    private_key, public_key = generate_key_pair()
    print(f"私鑰 (Private Key): {private_key}")
    print(f"公鑰 (Public Key):  {public_key}")
    print("="*50)

    # 2. 產生帶有簽名的資料
    print("--- 2. 產生帶有簽名的資料 ---")
    payload_b64 = generate_signed_numbers(private_key)
    
    print(f"Base64 簽名資料 (Payload): {payload_b64}")
    print(f"資料長度: {len(payload_b64)} bytes")
    
    # 轉換回 bytes 查看內容
    payload_bytes = base64.b64decode(payload_b64)
    numbers = struct.unpack('<10H', payload_bytes[:20])
    print(f"還原的前 10 個數字: {list(numbers)}")
    print("="*50)

    # 3. 進行驗證測試
    print("--- 3. 進行驗證測試 ---")
    
    # 測試正確的資料
    is_valid = verify_data(payload_b64, public_key)
    print(f"✓ 正確資料驗證結果: {'成功' if is_valid else '失敗'}")
    
    # 測試竄改過的資料 (修改其中一個數字)
    malicious_b64 = payload_b64[:-5] + "AAAAA"  # 替換最後幾個字元
    is_valid_malicious = verify_data(malicious_b64, public_key)
    print(f"✗ 竄改資料驗證結果: {'成功' if is_valid_malicious else '失敗 (預期)'}")
    
    # 測試錯誤的公鑰
    wrong_public_key = "0000000000000000000000000000000000000000000000000000000000000000"
    is_valid_wrong_key = verify_data(payload_b64, wrong_public_key)
    print(f"✗ 錯誤公鑰驗證結果: {'成功' if is_valid_wrong_key else '失敗 (預期)'}")