import time
import logging
from math import gcd

from sage.all import GF, crt, inverse_mod, is_prime

logging.basicConfig(level=logging.INFO, format="%(message)s")

# IMPORTANT: Ensure gcd(phi//e, e) == 1 when you want the Shumow fast path.
p = 120419919031709910490722466645725319603709107605346854013154637210716960935486570548446076073162388411530882021302911776751910551596143096440040181574247742010094350794982823076456252495969290735111729828961777365450167447391103381964976322863335088019005955362633260066267661265158139675904388219946491019433
q = 143145136596897792012244927913143321571441800675534861059705469061258992061883995162325862437989937967148966126707021998806898307931462572202651867531561495545853792708828760835643238061807625875894836039823918821156746198833339954739915742541247162094132294567718961747164688457286462756716971084725211371007
e = 268435459

N   = p * q
phi = (p - 1) * (q - 1)

m_bytes = b"ITSEC{tH4Ts_WhY_M4th_iS_Be4UTiFuL_&_iMPoRt4nt!!!}"
m       = int.from_bytes(m_bytes, "big")
c       = pow(m, e, N)

# stop when candidate decodes and starts with ITSEC{
FLAG_PREFIX = b"ITSEC{"

# Demo mode:
#   "until-flag"  → stop when matching the predicate
#   "first-N"     → collect first LIMIT candidates (per attack) for timing comparison
MODE  = "until-flag"   # or "first-N"
LIMIT = 1_000          # used only for MODE="first-N"

def v_e(p_, e_):
    """Return the largest t s.t. e_^t | (p_-1)."""
    t = 0
    while (p_ - 1) % (e_ ** (t + 1)) == 0:
        t += 1
    return t

def int_to_bytes(x: int) -> bytes:
    if x == 0:
        return b"\x00"
    return x.to_bytes((x.bit_length() + 7) // 8, "big")

def looks_like_flag(x: int) -> bool:
    s = int_to_bytes(x)
    return s.startswith(FLAG_PREFIX) and s.endswith(b"}")

def roots_of_unity(Fq, r: int):
    """
    Yield all r-th roots of unity in Fq (r | q-1). Works for prime/prime-power q.
    """
    q = Fq.order()
    assert (q - 1) % r == 0, "r must divide q-1"
    # generator of multiplicative group
    try:
        gen = Fq.multiplicative_generator()
    except AttributeError:
        gen = Fq.primitive_element()
    z = gen ** ((q - 1) // r)  # element of exact order r
    u = Fq(1)
    for _ in range(r):
        yield u
        u *= z

def rth_roots(Fq, delta, r: int):
    """
    AMM (Adleman–Manders–Miller) r-th root extraction in Fq, with r | (q - 1).
    Returns a generator over all r distinct solutions x with x^r = delta.
    """
    delta = Fq(delta)
    q = Fq.order()
    assert (q - 1) % r == 0, "r should divide q - 1"

    # find a non-residue for the r-th power map
    p_elt = Fq(1)
    while p_elt ** ((q - 1) // r) == 1:
        p_elt = Fq.random_element()

    # write q - 1 = r^t * s with r ∤ s
    t = 0
    s = q - 1
    while s % r == 0:
        t += 1
        s //= r

    # find α such that r α ≡ 1 (mod r) via k*s + 1 ≡ 0 (mod r)
    k = 1
    while (k * s + 1) % r != 0:
        k += 1
    alpha = (k * s + 1) // r

    a = p_elt ** (pow(r, t - 1, q - 1) * s)
    b = delta ** (r * alpha - 1)
    c = p_elt ** s
    h = Fq(1)
    for i in range(1, t):
        d = b ** pow(r, t - 1 - i, q - 1)
        j = 0 if d == 1 else -d.log(a)   # discrete log in order-r subgroup
        b *= (c ** r) ** j
        h *= c ** j
        c **= r

    # one root:
    root = delta ** alpha * h
    # all roots are root * ζ with ζ an r-th root of unity
    for zeta in roots_of_unity(Fq, r):
        yield int((root * zeta))


# Shumow special-case attack

def shumow_attack(N_, e_, phi_, c_):
    """
    Shumow Algorithms 1 & 2 (prime e, gcd(phi/e, e)=1).
    Yields *e_* candidates; prefer to use an early-stop consumer.
    """
    assert phi_ % e_ == 0, "Public exponent must divide phi(N)"
    assert gcd(phi_ // e_, e_) == 1, "Require gcd(phi/e, e) = 1"
    assert is_prime(e_), "Shumow fast path assumes prime e"

    phi_red = phi_ // e_

    # Algorithm 1 – find gE of exact order e
    g = 1
    while True:
        g += 1
        gE = pow(g, phi_red, N_)
        if gE != 1 and pow(gE, e_, N_) == 1:   # ensure exact order e (since e is prime)
            break

    # Algorithm 2 – enumerate candidates
    d = inverse_mod(e_, phi_red)     # reduced private exponent
    a = pow(c_, d, N_)
    l = gE
    while True:
        yield (a * l) % N_
        l = (l * gE) % N_


# AMM + CRT (generic)

def amm_crt_attack(N_, e_, p_, q_, c_):
    """
    Generic path: find e-th roots modulo each prime then combine via CRT.
    Yields up to (#roots mod p) * (#roots mod q) RSA roots.
    """
    tp, tq = v_e(p_, e_), v_e(q_, e_)

    # mod p
    cp = c_ % p_
    if tp == 0:
        mps = [pow(cp, inverse_mod(e_, p_ - 1), p_)]
    else:
        mps = list(rth_roots(GF(p_), cp, e_))

    # mod q
    cq = c_ % q_
    if tq == 0:
        mqs = [pow(cq, inverse_mod(e_, q_ - 1), q_)]
    else:
        mqs = list(rth_roots(GF(q_), cq, e_))

    for mp in mps:
        for mq in mqs:
            yield int(crt([int(mp), int(mq)], [p_, q_]))

def time_until_flag(gen_fn, *args):
    t0 = time.perf_counter()
    count = 0
    for x in gen_fn(*args):
        count += 1
        if looks_like_flag(x):
            t1 = time.perf_counter()
            return True, count, (t1 - t0), x
    t1 = time.perf_counter()
    return False, count, (t1 - t0), None

def time_first_n(gen_fn, n, *args):
    t0 = time.perf_counter()
    out = []
    for x in gen_fn(*args):
        out.append(x)
        if len(out) >= n:
            break
    t1 = time.perf_counter()
    return len(out), (t1 - t0), out

if __name__ == "__main__":
    print(f"N bits = {N.bit_length()}, e = {e}, v_e(p-1)={v_e(p, e)}, v_e(q-1)={v_e(q, e)}")
    print(f"gcd(phi/e, e) = {gcd(phi // e, e)}  (0 means Shumow fast path is NOT applicable)")

    if MODE == "until-flag":
        print("\n[+] Shumow (until flag)…")
        ok_s, cnt_s, ts, root_s = time_until_flag(shumow_attack, N, e, phi, c)
        print(f"    stop={ok_s}, steps={cnt_s}, time={ts:.6f}s")
        if ok_s:
            print(f"    candidate (ASCII): {int_to_bytes(root_s)}")

        print("\n[+] AMM+CRT (until flag)…")
        ok_a, cnt_a, ta, root_a = time_until_flag(lambda *_: amm_crt_attack(N, e, p, q, c), None)
        print(f"    stop={ok_a}, steps={cnt_a}, time={ta:.6f}s")
        if ok_a:
            print(f"    candidate (ASCII): {int_to_bytes(root_a)}")

    elif MODE == "first-N":
        print(f"\n[+] Shumow (first {LIMIT}) …")
        n_s, ts, outs_s = time_first_n(shumow_attack, LIMIT, N, e, phi, c)
        print(f"    produced={n_s}, time={ts:.6f}s")

        print(f"\n[+] AMM+CRT (first {LIMIT}) …")
        n_a, ta, outs_a = time_first_n(lambda *_: amm_crt_attack(N, e, p, q, c), LIMIT, None)
        print(f"    produced={n_a}, time={ta:.6f}s")
    else:
        raise SystemExit("MODE must be 'until-flag' or 'first-N'.")

    print("\n[+] Verifying ground truth via decryption check …")
    assert pow(m, e, N) == c
    print("    ok: m^e ≡ c (mod N)")

    if MODE == "until-flag":
        if looks_like_flag(m):
            print("    Expected plaintext looks like a flag; your early-stop condition is sane.")
