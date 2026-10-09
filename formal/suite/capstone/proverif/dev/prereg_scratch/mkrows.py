import re
B={}
for l in open('slice_blobs.txt'):
    f,b,_=l.split(None,2); B[f[:-3]]=b[:12]
rows=[l.split() for l in open('rows.txt')]
meta={ # (src,q): (member, pred line, seam, pilot)
('cap_cc02_d','cq3a'):('C-Q3 `ReattributedA`',':1771','D1','rl:22 red 98 s; rl:5 cone red 29 s (rerun `codex/reruns.jsonl:1`)'),
('cap_cc02_d','cq3b'):('C-Q3 `ReattributedB`',':1771','D1','rl:28 red 98 s; rl:4 cone red'),
('cap_cc02_d','link5'):('link 5, frame-to-key half (T)',':1771','D1','rl:29 red 95 s; rl:8 cone red (`codex2/reruns.jsonl:1`)'),
('cap_cc03_d','cq5'):('C-Q5 `SetAltered`',':1772','D10','rl:48 cone red 2 s (`codex2/reruns.jsonl:3`); depth0 unpiloted'),
('cap_cc03_d','cq9'):('C-Q9 `PossessionUnbound`',':1772','D10','rl:49 cone red; depth0 unpiloted'),
('cap_cc03_d','link3'):('link 3',':1772','D10','rl:50 cone red; depth0 unpiloted'),
('cap_cc04_d','cq4r'):('C-Q4 `Rescoped`',':1773','D2','rl:53 depth1.cone red 50 s; depth1 unpiloted'),
('cap_cc04_d','cq4s'):('C-Q4 `InnerSigTransplanted`',':1773','D2','rl:54 depth1.cone red 48 s; depth1 unpiloted'),
('cap_cc04_d','cq3a'):('C-Q3 `ReattributedA`',':1773','D2','rl:51 depth0.cone red 30 s; depth1 unpiloted'),
('cap_cc04_d','cq3b'):('C-Q3 `ReattributedB`',':1773','D2','none (by symmetry with row 9 and C-C2 rl:4)'),
('cap_cc04_d','link6b'):('link 6b',':1773','D2','rl:55 depth1.cone red 50 s; depth1 unpiloted'),
('cap_cc04_d','link5'):('link 5, frame-to-key half (T, L)',':1773','D2','rl:52 depth0.cone red 11 s; depth1 unpiloted'),
('cap_cc05_d','cq4s'):('C-Q4 `InnerSigTransplanted`',':1774','D5','rl:58 depth1.cone red 55 s (`codex/reruns.jsonl:2`); depth1 unpiloted'),
('cap_cc05_d','cq8'):('C-Q8 (L)',':1774','D5','rl:56 depth0.cone red 33 s; depth1 unpiloted'),
('cap_cc05_d','link4'):('link 4 (L)',':1774','D5','rl:57 depth0.cone red 33 s; depth1 unpiloted'),
('cap_cc06_d','cq7'):('C-Q7 `SigTransplanted`',':1775','D5 producer, D6','rl:59 cone red 89 s; depth0 unpiloted'),
('cap_cc06_d','cq4s'):('C-Q4 `InnerSigTransplanted`',':1775','D5','rl:62 depth1.cone red 476 s / 1.2 GB; depth1 unpiloted'),
('cap_cc06_d','cq8'):('C-Q8 (registered "predicted also")',':1775','D6','rl:60 cone red 89 s; depth0 unpiloted'),
('cap_cc06_d','link4'):('link 4 (registered "predicted also")',':1775','D6','rl:61 cone red 88 s; depth0 unpiloted'),
('cap_cc07i_d','cq8'):('C-Q8',':1776','D6','rl:64 cone red 2 s; depth0 unpiloted'),
('cap_cc07i_d','link4'):('link 4',':1776','D6','rl:65 cone red 2 s; depth0 unpiloted'),
('cap_cc07i_d','auhk'):('`AcceptedUnderHonestKey ⟹ IssuerSigned`',':1776','D6','rl:90 depth0 red 5 s (`codex2/reruns.jsonl:2`); rl:63 cone GREEN (too tight); depth1 unpiloted'),
('cap_cc07ii_d','cq8'):('C-Q8',':1776','D6','rl:66 cone red 35 s; depth0 unpiloted'),
('cap_cc07ii_d','link4'):('link 4',':1776','D6','rl:67 cone red 35 s; depth0 unpiloted'),
('cap_cc07ii_d','cq7'):('C-Q7 `SigTransplanted` (composed)',':1776','D6','none; the cone would delete `Wrapper` (`codex2/REVIEW.md:124`)'),
('cap_cc07ii_d','auhk'):('`AcceptedUnderHonestKey ⟹ IssuerSigned` (composed)',':1776','D6','none; as row 25'),
('cap_cc08_d','cq9'):('C-Q9 `PossessionUnbound`',':1777','D10','rl:69 cone red 2 s; depth0 unpiloted'),
('cap_cc08_d','cq5'):('C-Q5 `SetAltered`',':1777','D10','rl:68 cone red 2 s; depth0 unpiloted'),
('cap_cc08_d','link3'):('link 3',':1777','D10','rl:70 cone red 2 s; depth0 unpiloted'),
('cap_cc08_d','link5'):('link 5, `mh` half (H)',':1777','D10','rl:71 cone red 1 s; depth0 unpiloted'),
('cap_cc08ii_d','cq9'):('C-Q9 (registered red by construction) (I)',':2547','none (D10 isolation)','rl:72 cone red 2 s; depth0 unpiloted'),
('cap_cc17_d','link2a'):('link 2a',':2666','D7 membership','rl:73 cone red 3 s; depth0 unpiloted'),
('cap_cc17_d','sf'):('`SignerForged`',':2666','D7 membership','rl:91 depth0 red 10 s (`codex/reruns.jsonl:3`); rl:74 cone GREEN (too tight); depth1 unpiloted'),
}
for i,(src,q,p,f) in enumerate(rows,1):
    m,pl,seam,pil=meta[(src,q)]
    short=src.replace('cap_','').replace('_d','')
    print(f"| {i} | `{short}` | {m} `{q}` | red, `PREDICTIONS.md{pl}` | {seam} | `{p}` `{B[src+'__'+p+'__'+q]}` | `{f}` `{B[src+'__'+f+'__'+q]}` | {pil} |")
print()
ctl={}
for k,b in B.items():
    if k.startswith('capstone_d__'):
        _,sl,q=k.split('__'); ctl.setdefault(sl,[]).append(f"{q} `{b}`")
for sl in ['depth0','depth0.cone','depth1','depth1.cone']:
    print(f"| `{sl}` | {len(ctl[sl])} | "+', '.join(sorted(ctl[sl]))+" |")
