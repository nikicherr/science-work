# keygen.py
import secrets
import json
import time
from pathlib import Path
start = time.time()
PARAMS_FILE = "params.json"
KEY_FILE = "key.json"

def main():
    # читаем p, q, g из params.json
    params = json.loads(Path(PARAMS_FILE).read_text(encoding="utf-8"))
    p = int(params["p"])
    q = int(params["q"])
    g = int(params["g"])

    print("=== Генерация ключей (Схема Шнорра) ===")
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"g = {g}")
    # закрытый ключ x: 1 < x < q
    x = secrets.randbelow(q - 2) + 2
    # открытый ключ y = g^x mod p
    y = pow(g, x, p)

    Path(KEY_FILE).write_text(json.dumps({
        "x": str(x),
        "y": str(y)
    }, indent=2), encoding="utf-8")
    print(f"Ключи сохранены в {KEY_FILE}")
    print(f"x (секретный) = {x}")
    print(f"y (открытый)  = {y}")
if __name__ == "__main__":
    main()
end = time.time()
print(f"Время выполнения: {end - start:.4f} с")