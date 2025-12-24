
import json
import random
import sympy as sp
from pathlib import Path
import time

PARAMS_FILE = "params.json"
start = time.time()
def find_p_q_g():
    # целимся в 256‑битные числа
    q_bits = 256
    print("Ищем q ~ 256 бит и p = k*q + 1 (p простое), затем g порядка q...")
    while True:
        # случайное простое q ≈ 2^255 … 2^256
        q_min = 1 << (q_bits - 1)
        q_max = (1 << q_bits) - 1
        q = sp.randprime(q_min, q_max)
        # подбираем небольшие k, чтобы p = k*q + 1 было простым
        for k in range(2, 50):
            p = k * q + 1
            if not sp.isprime(p):
                continue
            # пробуем найти g такой, что порядок(g) = q
            # g^q ≡ 1 (mod p), и нет меньшего делителя порядка
            print(f"Нашли  p, q с k={k}, ищем g...")
            for g in range(2, 200):
                if pow(g, q, p) != 1:
                    continue
                # проверяем, что порядок ровно q (нет меньших делителей)
                ok = True
                factors = sp.factorint(q).keys()
                for r in factors:
                    if pow(g, q // r, p) == 1:
                        ok = False
                        break
                if ok:
                    return p, q, g
def main():
    start = time.time()
    p, q, g = find_p_q_g()
    

    data = {
        "p": str(p),
        "q": str(q),
        "g": str(g)
    }
    Path(PARAMS_FILE).write_text(json.dumps(data, indent=2), encoding="utf-8")
    print("\nПараметры найдены и сохранены в", PARAMS_FILE)
    print(f"p (бит): {p.bit_length()}, p = {p}")
    print(f"q (бит): {q.bit_length()}, q = {q}")
    print(f"g       : {g}")
if __name__ == "__main__":
    main()
end = time.time()
print(f"\nВремя подбора: {end - start:.4f} с")