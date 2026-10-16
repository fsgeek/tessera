"""Differential fuzz: implementation A (gen.py) against implementation B (check.py).

60,000 seeded cases in three stages of 20,000:
  1. random JSON texts and byte mutations of content vectors, through ingestion;
  2. byte mutations of the golden attestation frames, through the frame decoder;
  3. (2026-10-12) mutations of the composite receipt anchor A_sig (A-01 with real signatures, A-02 canary):
     byte edits biased to the signature slots and length prefixes, and structural edits that substitute,
     duplicate, truncate, re-frame or swap signature and frame slots, with and without consistent prefixes.
Every case must get the same verdict and reason code from both; accepted texts the same canonical bytes;
accepted anchors the same ordered (frame, signature) tuples. Stages 1 and 2 are unchanged from 2026-10-09
(same seed, same order), so their cases are the same as before.
Hybrid supplement (2026-10-14): stages 4-6 below, own seed, read hybrid-golden.json / hybrid-reject.json.
Run: uv run --no-project --with rfc8785==0.1.4 python formal/p8/vectors/fuzz.py
"""
import os, sys, random, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.setrecursionlimit(5000)
import gen as A, check as B
rnd = random.Random(8)
G = json.load(open(os.path.join(HERE, 'golden.json')))['vectors']; R = json.load(open(os.path.join(HERE, 'reject.json')))['vectors']
def va(fn):
    try: fn(); return 'OK'
    except A.Reject as e: return e.code
def vb(fn):
    try: fn(); return 'OK'
    except B.Bad as e: return e.code
dis = 0; n = 0; codes = {}
frames = [bytes.fromhex(g['bytes_hex']) for g in G if g['kind']=='frame-attest']
texts = [bytes.fromhex(g['input']['text_hex']) for g in G if g['kind']=='content'] + [bytes.fromhex(r['input']['text_hex']) for r in R if r['entry']=='content']
alphabet = list(b'{}[]",:0123456789-+.eE \\u\nabtrfnl') + [0xc3,0xa9,0xff,0xed]
toks = ['0','-0','1e400','9.8','9.80','1E2','0.1','1e-7','123456789012345680000','9007199254740993','"\\ud800"','"\\u00e9"','"e\\u0301"','true','null','[]','{}','"\\uffff"','1.5e300','5e-324','4.9e-324','2.4703282292062328e-324','1e21','1e+21','0.000001','-1.5','1.7976931348623158e308','1.7976931348623157e308']
def rand_json(d=0):
    r = rnd.random()
    if d>3 or r<0.4: return rnd.choice(toks)
    if r<0.7: return '['+','.join(rand_json(d+1) for _ in range(rnd.randint(0,3)))+']'
    ks = [rnd.choice(['"a"','"b"','"\\u0061"','"\\ue000"','"\\ud83d\\ude00"','"é"']) for _ in range(rnd.randint(0,3))]
    return '{'+','.join(k+':'+rand_json(d+1) for k in ks)+'}'
for _ in range(20000):
    t = rand_json().encode() if rnd.random()<0.6 else bytearray(rnd.choice(texts))
    if isinstance(t, bytearray) and t:
        for _ in range(rnd.randint(1,3)):
            p = rnd.randrange(len(t)+1); op = rnd.random()
            if op<0.4 and p<len(t): t[p]=rnd.choice(alphabet)
            elif op<0.7: t.insert(p, rnd.choice(alphabet))
            elif p<len(t): del t[p]
    t = bytes(t)
    a, b = va(lambda: A.ingest(t)), vb(lambda: B.ingest(t))
    n += 1
    if a=='OK' and b=='OK':
        if A.jcs(A.ingest(t)) != B.jcs(B.ingest(t)): dis+=1; print('JCS DIFF', t)
    elif a!=b: dis+=1; print('VERDICT DIFF', t, a, b) if dis<15 else None
    codes[a]=codes.get(a,0)+1
for _ in range(20000):
    f = bytearray(rnd.choice(frames))
    for _ in range(rnd.randint(1,2)):
        p = rnd.randrange(len(f)); op=rnd.random()
        if op<0.5: f[p]=rnd.randrange(256)
        elif op<0.75: f.insert(p, rnd.randrange(256))
        else: del f[p]
    f = bytes(f); n += 1
    a, b = va(lambda: A.decode_frame(f, A.T_ATTEST)), vb(lambda: B.frame_decode(f, 'attest'))
    if a!=b: dis+=1; print('FRAME DIFF', a, b) if dis<15 else None
    codes[a]=codes.get(a,0)+1
# ---- stage 3: composite anchor A_sig ----
import struct
anchors = [g for g in G if g['kind'] == 'anchor']
def parts(g): return [bytes.fromhex(g['input'][k]) for k in ('f0_hex', 's0_hex', 'f1_hex', 's1_hex')]
sig_pool = [p[1] for p in map(parts, anchors)] + [p[3] for p in map(parts, anchors)]
sig_pool += [bytes.fromhex(r['input']['s0_hex']) for r in R if r['entry'] == 'receipt' and 'control' in r]
def regions(g):
    f0, s0, f1, s1 = parts(g); hl = 1 + 29 + 1; out = []; at = hl
    for x in (f0, s0, f1, s1):
        out.append((at, 4)); out.append((at + 4, len(x))); at += 4 + len(x)
    return out
def P4(x): return struct.pack('>I', len(x)) + x
ah = bytes([29]) + b'tessera-v1/receipt-anchor-sig'
codes3 = {}
for _ in range(20000):
    g = rnd.choice(anchors); f0, s0, f1, s1 = parts(g); op = rnd.random()
    if op < 0.45:                       # byte edits, mostly in prefixes and signatures
        b = bytearray(bytes.fromhex(g['bytes_hex'])); regs = regions(g)
        for _ in range(rnd.randint(1, 3)):
            if rnd.random() < 0.8:
                at, ln = rnd.choice([regs[i] for i in (0, 2, 3, 4, 6, 7)])
                p = at + rnd.randrange(max(ln, 1))
            else:
                p = rnd.randrange(len(b))
            p = min(p, len(b) - 1); k = rnd.random()
            if k < 0.6: b[p] = rnd.randrange(256)
            elif k < 0.8: b.insert(p, rnd.randrange(256))
            else: del b[p]
        a_bytes = bytes(b)
    else:                               # structural edits
        sl = [f0, s0, f1, s1]; k = rnd.randrange(9); i = rnd.choice((1, 3))
        if k == 0: sl[i] = rnd.choice(sig_pool)
        elif k == 1: sl[i] = sl[i] + rnd.choice(sig_pool)
        elif k == 2: sl[i] = sl[i][:rnd.randrange(len(sl[i]) + 1)]
        elif k == 3: sl[i] = bytes([rnd.choice((0x88, 0x89, 0xc2, 0x90, 0xa8))]) + sl[i][1:]
        elif k == 4: sl[1], sl[3] = sl[3], sl[1]
        elif k == 5: sl[i - 1], sl[i] = sl[i], sl[i - 1]
        elif k == 6: sl[i] = b''
        elif k == 7: sl[i] = bytes(rnd.randrange(256) for _ in range(rnd.choice((1, 64, 1024, 1025, 3309))))
        else:
            sb = bytearray(sl[i]); p = rnd.randrange(len(sb)); sb[p] = rnd.randrange(256); sl[i] = bytes(sb)
        body = b''.join(P4(x) for x in sl)
        if rnd.random() < 0.15:          # inconsistent prefix
            bb = bytearray(body); p = rnd.choice([0, 4 + len(sl[0])]); d = rnd.choice((-1, 1, 5))
            bb[p:p + 4] = struct.pack('>I', max(0, int.from_bytes(bb[p:p + 4], 'big') + d)); body = bytes(bb)
        a_bytes = ah + bytes([rnd.choice((2, 2, 2, 2, 1, 3))]) + body + (b'\x00' if rnd.random() < 0.05 else b'')
    n += 1
    ra_, rb_ = [None], [None]
    def da(): ra_[0] = A.decode_anchor(a_bytes)
    def db(): rb_[0] = B.anchor_decode(a_bytes)
    a, b = va(da), vb(db)
    if a != b: dis += 1; print('ANCHOR DIFF', a, b) if dis < 15 else None
    elif a == 'OK' and ra_[0] != rb_[0]: dis += 1; print('ANCHOR TUPLE DIFF')
    codes3[a] = codes3.get(a, 0) + 1
print('cases', n, 'disagreements', dis); print(sorted(codes.items(), key=lambda x:-x[1]))
print('stage 3 (anchor) verdicts:', sorted(codes3.items(), key=lambda x:-x[1]))
# ==== hybrid supplement stages (2026-10-14), own seed: stages 1-3 above are unchanged ====
# 4. 20,000 mutations of the hybrid anchors A-H1/A-H2 (rule R in kms, rule O in gpg), as stage 3, with
#    rule-R-specific lengths (3308, 3309, 3310, 2420, 4627) and cross-rule substitutions.
# 5. 10,000 mutations of the ML-DSA-65 SPKI through both key codecs (KEY_FORMAT / KEY_MISMATCH / OK).
# 6. 400 mutated (frame, signature) pairs through both ML-DSA-65 verifiers (A: butterfly NTT; B: direct
#    evaluation), biased to the c~, z and hint regions; verdicts must agree.
rnd = random.Random(1014)
HG = json.load(open(os.path.join(HERE, 'hybrid-golden.json')))['vectors']
HR = json.load(open(os.path.join(HERE, 'hybrid-reject.json')))['vectors']
hanchors = [g for g in HG if g['kind'] == 'anchor']
hsig_pool = [p[1] for p in map(parts, hanchors)] + [p[3] for p in map(parts, hanchors)] + sig_pool
hsig_pool += [bytes.fromhex(r['input']['s0_hex']) for r in HR if r['entry'] == 'receipt']
hframes = frames + [bytes.fromhex(g['bytes_hex']) for g in HG if g['kind'] == 'frame-attest']
dis4 = 0; codes4 = {}
for _ in range(20000):
    g = rnd.choice(hanchors); f0, s0, f1, s1 = parts(g); op = rnd.random()
    if op < 0.4:
        b = bytearray(bytes.fromhex(g['bytes_hex'])); regs = regions(g)
        for _ in range(rnd.randint(1, 3)):
            if rnd.random() < 0.8:
                at, ln = rnd.choice([regs[i] for i in (0, 2, 3, 4, 6, 7)]); p = at + rnd.randrange(max(ln, 1))
            else:
                p = rnd.randrange(len(b))
            p = min(p, len(b) - 1); k = rnd.random()
            if k < 0.6: b[p] = rnd.randrange(256)
            elif k < 0.8: b.insert(p, rnd.randrange(256))
            else: del b[p]
        a_bytes = bytes(b)
    else:
        sl = [f0, s0, f1, s1]; k = rnd.randrange(10); i = rnd.choice((1, 3))
        if k == 0: sl[i] = rnd.choice(hsig_pool)
        elif k == 1: sl[i] = sl[i] + rnd.choice(hsig_pool)
        elif k == 2: sl[i] = sl[i][:rnd.randrange(len(sl[i]) + 1)]
        elif k == 3: sl[i] = bytes(rnd.randrange(256) for _ in range(rnd.choice((1, 119, 1024, 1025, 2420, 3308, 3309, 3310, 4627))))
        elif k == 4: sl[1], sl[3] = sl[3], sl[1]
        elif k == 5: sl[i - 1], sl[i] = sl[i], sl[i - 1]
        elif k == 6: sl[i] = b''
        elif k == 7: sl[i - 1] = rnd.choice(hframes)          # cross-id frame substitution (classical, canary, hybrid)
        elif k == 8: sl[i] = sl[i][:-1] + bytes([rnd.randrange(256)]) * rnd.choice((0, 1, 2))
        else:
            sb = bytearray(sl[i]); p = rnd.randrange(len(sb)); sb[p] = rnd.randrange(256); sl[i] = bytes(sb)
        body = b''.join(P4(x) for x in sl)
        if rnd.random() < 0.15:
            bb = bytearray(body); p = rnd.choice([0, 4 + len(sl[0])]); d = rnd.choice((-1, 1, 5))
            bb[p:p + 4] = struct.pack('>I', max(0, int.from_bytes(bb[p:p + 4], 'big') + d)); body = bytes(bb)
        a_bytes = ah + bytes([rnd.choice((2, 2, 2, 2, 1, 3))]) + body + (b'\x00' if rnd.random() < 0.05 else b'')
    n += 1
    ra_, rb_ = [None], [None]
    def da(): ra_[0] = A.decode_anchor(a_bytes)
    def db(): rb_[0] = B.anchor_decode(a_bytes)
    a, b = va(da), vb(db)
    if a != b: dis4 += 1; print('HYBRID ANCHOR DIFF', a, b) if dis4 < 15 else None
    elif a == 'OK' and ra_[0] != rb_[0]: dis4 += 1; print('HYBRID ANCHOR TUPLE DIFF')
    codes4[a] = codes4.get(a, 0) + 1
spkis = [bytes.fromhex(g['spki_der_hex']) for g in HG if g['kind'] == 'fingerprint-kms-spki']
spkis += [bytes.fromhex(r['input']['spki_der_hex']) for r in HR if r['entry'] == 'key-kms']
fp_h = [g['key_fp'] for g in HG if g['id'] == 'K-H1'][0]
dis5 = 0; codes5 = {}
for _ in range(10000):
    k = bytearray(rnd.choice(spkis))
    for _ in range(rnd.randint(1, 2)):
        p = rnd.randrange(min(len(k), 40)) if rnd.random() < 0.8 else rnd.randrange(len(k))
        op = rnd.random()
        if op < 0.6: k[p] = rnd.choice((0x00, 0x01, 0x03, 0x05, 0x06, 0x07, 0x0b, 0x11, 0x12, 0x13, 0x30, 0x80, 0x81, 0x82, 0x83, rnd.randrange(256)))
        elif op < 0.8: k.insert(p, rnd.randrange(256))
        else: del k[p]
    k = bytes(k); n += 1
    a, b = va(lambda: A.check_key_kms(k, fp_h)), vb(lambda: B.key_kms(k, fp_h))
    if a != b: dis5 += 1; print('SPKI DIFF', a, b, k[:30].hex()) if dis5 < 15 else None
    codes5[a] = codes5.get(a, 0) + 1
sigv = [(bytes.fromhex(g['input']['spki_der_hex']), bytes.fromhex(g['input']['message_hex']), bytes.fromhex(g['bytes_hex']))
        for g in HG if g['kind'] == 'signature-mldsa65']
dis6 = 0; codes6 = {}
for _ in range(400):
    spk, msg, sg = rnd.choice(sigv); sg = bytearray(sg); msg = bytearray(msg); r_ = rnd.random()
    if r_ < 0.25: p = rnd.randrange(48); sg[p] ^= 1 << rnd.randrange(8)                         # c~
    elif r_ < 0.5: p = 48 + rnd.randrange(3200); sg[p] = rnd.randrange(256)                    # z
    elif r_ < 0.8: p = 3248 + rnd.randrange(61); sg[p] = rnd.choice((0, 1, 54, 55, 56, 255, rnd.randrange(256)))   # hints
    elif r_ < 0.9: p = rnd.randrange(len(msg)); msg[p] ^= 1                                    # message
    # else: unchanged (must verify)
    sg, msg = bytes(sg), bytes(msg); n += 1
    a, b = A.mldsa65_verify(spk[22:], msg, sg), B.mldsa65_ok(B.mldsa_spki(spk), msg, sg)
    if a != b: dis6 += 1; print('MLDSA VERIFY DIFF', a, b)
    codes6[a] = codes6.get(a, 0) + 1
print('hybrid stage 4 (anchor) verdicts:', sorted(codes4.items(), key=lambda x: -x[1]))
print('hybrid stage 5 (kms SPKI) verdicts:', sorted(codes5.items(), key=lambda x: -x[1]))
print('hybrid stage 6 (ML-DSA-65 verify) verdicts:', sorted(codes6.items(), key=lambda x: -x[1]))
print('hybrid disagreements', dis4 + dis5 + dis6, 'total cases', n)
sys.exit(1 if dis or dis4 or dis5 or dis6 else 0)
