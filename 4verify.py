# verify.py
import json
import hashlib
import time
from pathlib import Path
PARAMS_FILE = "params.json"
KEY_FILE = "key.json"
SIGN_FILE = "signature.json"
# ДОЛЖЕН СОВПАДАТЬ с тем, что в sign.py:
MESSAGE_FILE = "2/testik.txt"
start = time.time()
def H(data: bytes) -> int:
    h = hashlib.sha256(data).digest()
    return int.from_bytes(h, "big")
def main():
    print("=== Проверка подписи (Схема Шнорра) ===")
    if not Path(MESSAGE_FILE).exists():
        print(f"Файл {MESSAGE_FILE} не найден.")
        return
    if not Path(SIGN_FILE).exists():
        print(f"Файл {SIGN_FILE} не найден.")
        return
    m_bytes = Path(MESSAGE_FILE).read_bytes()
    print(f"Сообщение: {MESSAGE_FILE}, размер {len(m_bytes)} байт.")
    params = json.loads(Path(PARAMS_FILE).read_text(encoding="utf-8"))
    p = int(params["p"])
    q = int(params["q"])
    g = int(params["g"])
    key = json.loads(Path(KEY_FILE).read_text(encoding="utf-8"))
    y = int(key["y"])  # открытый ключ
    sig = json.loads(Path(SIGN_FILE).read_text(encoding="utf-8"))
    e = int(sig["e"])
    s = int(sig["s"])
    # 1. r' = g^s * y^e mod p
    gs = pow(g, s, p)
    ye = pow(y, e, p)
    r_prime = (gs * ye) % p
    # 2. e' = H(m || r') mod q
    r_prime_bytes = r_prime.to_bytes((r_prime.bit_length() + 7) // 8, "big")
    e_prime = H(m_bytes + r_prime_bytes) % q
    print(f"e  (из подписи) = {e}")
    print(f"e' (вычисленное) = {e_prime}")
    if e_prime == e:
        print(" Подпись ДЕЙСТВИТЕЛЬНА.")
    else:
        print(" Подпись НЕДЕЙСТВИТЕЛЬНА.")
if __name__ == "__main__":
    main()
end = time.time()
print(f"Время выполнения : {end - start:.4f} секунд")