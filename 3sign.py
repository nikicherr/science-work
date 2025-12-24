# sign.py
import json
import secrets
import hashlib
import time
from pathlib import Path

PARAMS_FILE = "params.json"
KEY_FILE = "key.json"
SIGN_FILE = "signature.json"
MESSAGE_FILE = "2/testik.txt"# Указать путь к файлу для подписи:
start = time.time()
def H(data: bytes) -> int:
    """Хеш SHA-256 -> число"""
    h = hashlib.sha256(data).digest()
    return int.from_bytes(h, "big")
def main():
    print("=== Создание подписи (Схема Шнорра) ===")

    if not Path(MESSAGE_FILE).exists():
        print(f"Файл {MESSAGE_FILE} не найден.")
        return
    m_bytes = Path(MESSAGE_FILE).read_bytes()
    print(f"Сообщение: {MESSAGE_FILE}, размер {len(m_bytes)} байт.")

    params = json.loads(Path(PARAMS_FILE).read_text(encoding="utf-8"))
    p = int(params["p"])
    q = int(params["q"])
    g = int(params["g"])
    key = json.loads(Path(KEY_FILE).read_text(encoding="utf-8"))
    x = int(key["x"])  # секретный ключ
    # 1. H(m) — можно не использовать отдельно, главное H(m||r)
    # 2. k: 1 < k < q
    k = secrets.randbelow(q - 2) + 2
    # 3. r = g^k mod p
    r = pow(g, k, p)
    # 4. e = H(m || r) mod q
    r_bytes = r.to_bytes((r.bit_length() + 7) // 8, "big")
    e = H(m_bytes + r_bytes) % q
    # 5. s = k - x*e mod q
    s = (k - x * e) % q
    sig = {
        "file": MESSAGE_FILE,
        "e": str(e),
        "s": str(s)
    }
    Path(SIGN_FILE).write_text(json.dumps(sig, indent=2), encoding="utf-8")
    print(f"Подпись сохранена в {SIGN_FILE}")
    print(f"e = {e}")
    print(f"s = {s}")
if __name__ == "__main__":
    main()
end = time.time()
print(f"Время выполнения : {end - start:.4f} секунд")