"""Exhaustive local mutation of real A_sig, structured O packets, and mixed rules."""
import sys
sys.dont_write_bytecode=True
from review import *

def main():
    counts=collections.Counter();hist=collections.defaultdict(collections.Counter);diffs=[]
    def check(kind,raw,pair):
        counts[kind]+=1;a,b=pair;hist[kind][a[0]+' / '+b[0]]+=1
        if a[0]!=b[0]:diffs.append({'kind':kind,'hex':raw.hex(),'B':a[0],'I':b[0]})
        elif a[0]=='OK':
            if kind.startswith('anchor'):assert a[1]==b[1]
            elif kind.startswith('frame'):assert B.jcs(a[1])==I.jcs(b[1])
    layer=json.loads((ROOT/'prototype/e2e/receipts/real-1/bundle.json').read_text())['layers'][0]
    real=base64.b64decode(layer['a_sig'])
    for i in range(len(real)):
        for bit in range(8):
            raw=real[:i]+bytes([real[i]^(1<<bit)])+real[i+1:]
            check('anchor-real-single-bit',raw,anchor(raw))
    for f,_ in B.anchor_decode(real):
        for i in range(len(f)):
            for bit in range(8):
                raw=f[:i]+bytes([f[i]^(1<<bit)])+f[i+1:]
                check('frame-real-single-bit',raw,frame(raw))
    # All proper truncations; all byte values as a one-byte suffix.
    for i in range(len(real)):check('anchor-real-truncation',real[:i],anchor(real[:i]))
    for c in range(256):check('anchor-real-extension',real+bytes([c]),anchor(real+bytes([c])))
    # Isolate 16-bit nested length fields and every MPI bit-count, retaining valid packet boundaries.
    for hlen in (0,1,2,5,191,192,255,256,65535):
        for ulen in (0,1,2,5,191,192,255,256,65535):
            raw=pgp(b'\x04\x00\x13\x08'+hlen.to_bytes(2,'big')+b'\x01\x01'+ulen.to_bytes(2,'big')+b'\x01\x01'+b'\0\0\0\1\1\0\1\1')
            check('signature-nested-length',raw,(outcome(lambda:B.sig_check(raw,B.V1_ALG,0)),outcome(lambda:I.parse_signature(raw))))
    for bits in range(258):
        for value in (0,1,(1<<min(bits,256))-1,1<<max(0,min(bits,256)-1)):
            mpi=bits.to_bytes(2,'big')+value.to_bytes((bits+7)//8,'big') if bits else b'\0\0'
            raw=pgp(b'\x04\x00\x13\x08\0\0\0\0\0\0'+mpi+b'\0\1\1')
            check('signature-mpi-bitcount',raw,(outcome(lambda:B.sig_check(raw,B.V1_ALG,0)),outcome(lambda:I.parse_signature(raw))))
    # Longest O packet: 1024 whole bytes; two-octet old packet lengths.
    for n in (191,192,255,256,1005,1006,1007,1008):
        area=(bytes([n]) if n<192 else bytes([192+((n-192)>>8),(n-192)&255]))+b'x'*n
        raw=tiny_sig(u=area)
        check('signature-packet-length',raw,(outcome(lambda:B.sig_check(raw,B.V1_ALG,0)),outcome(lambda:I.parse_signature(raw))))
    # Common.alg rule chosen independently from each frame, before any receipt conditions.
    obj=B.frame_decode(bytes.fromhex(byid['F-01']['bytes_hex']),'attest')
    for alg0 in (B.V1_ALG,B.HYB_ALG,'CANARY'):
        for alg1 in (B.V1_ALG,B.HYB_ALG,'CANARY'):
            x=copy.deepcopy(obj);y=copy.deepcopy(obj);x['common']['alg']=alg0;y['common']['alg']=alg1
            f0=B.frame_encode('attest',x);f1=B.frame_encode('attest',y)
            s0=b'x'*3309 if alg0==B.HYB_ALG else b'x' if alg0=='CANARY' else tiny_sig()
            s1=b'x' if alg1=='CANARY' else tiny_sig()
            raw=B.anchor_encode(f0,s0,f1,s1);check('anchor-mixed-rules',raw,anchor(raw))
    # Every u8 header length and all byte positions of each known header.
    for g in (byid[x] for x in ('F-01','M-01','A-01','S-01')):
        original=bytes.fromhex(g['bytes_hex']);isanchor=g['kind']=='anchor'
        if g['kind']=='snapshot':continue
        kind='manifest' if g['kind']=='frame-manifest' else 'attest'
        for n in range(256):
            raw=bytes([n])+original[1:]
            check('anchor-tag-length' if isanchor else 'frame-tag-length',raw,anchor(raw) if isanchor else frame(raw,kind))
    result={'counts':dict(counts),'histograms':{k:dict(v) for k,v in hist.items()},'disagreements':diffs}
    (HERE/'exhaustive.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'counts':dict(counts),'disagreements':len(diffs)},indent=2))
    for d in diffs[:12]:print(d)

if __name__=='__main__':main()
