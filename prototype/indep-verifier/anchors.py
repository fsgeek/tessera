"""Closed OTS grammar and pinned Bitcoin evidence; no network or PoW policy."""
from dataclasses import dataclass
from codec import Cursor, Fault, demand, sha

MAGIC=bytes.fromhex('004f70656e54696d657374616d7073000050726f6f6600bf89e2e884e89294')
BTC=bytes.fromhex('0588960d73d71901')
PENDING=bytes.fromhex('83dfe30d2ef90c8e')

def sha256d(raw): return sha(sha(raw))
class Reader(Cursor):
    def __init__(self,data): super().__init__(data,'OTS_FORMAT')
    def varuint(self):
        value=0
        for i in range(5):
            b=self.uint(1); value|=(b&127)<<(7*i)
            if not b&128:
                demand(value<=0xffffffff and (i==0 or b!=0),'OTS_FORMAT'); return value
        raise Fault('OTS_FORMAT')
    def varbytes(self,limit):
        n=self.varuint(); demand(n<=limit,'OTS_FORMAT'); return self.take(n)

@dataclass
class Attestation:
    height: int
    message: bytes
    path: tuple
    order: int
@dataclass
class Proof:
    digest: bytes
    bitcoin: list
    pending: list

def parse_ots(raw):
    demand(len(raw)<=2**20,'OTS_FORMAT'); c=Reader(raw)
    demand(c.take(len(MAGIC))==MAGIC and c.varuint()==1 and c.uint(1)==8,'OTS_FORMAT')
    digest=c.take(32); bitcoin=[]; pending=[]; ops=0; attestations=0
    # Explicit stack: a depth-256 proof is safe under any Python recursion setting.
    tasks=[(digest,(),0)]
    while tasks:
        message,path,depth=tasks.pop(); demand(depth<=256,'OTS_FORMAT')
        sibling=c.data[c.pos:c.pos+1]==b'\xff'
        if sibling: c.take(1); tasks.append((message,path,depth))
        opcode=c.uint(1)
        if opcode==0:
            attestations+=1; demand(attestations<=4096,'OTS_FORMAT')
            tag=c.take(8); payload=Reader(c.varbytes(8192))
            if tag==BTC:
                h=payload.varuint(); payload.end('OTS_FORMAT'); demand(len(message)==32,'OTS_FORMAT')
                bitcoin.append(Attestation(h,message,path,len(bitcoin)))
            elif tag==PENDING:
                uri=payload.varbytes(1000); payload.end('OTS_FORMAT'); pending.append(uri)
            else: raise Fault('OTS_FORMAT')
        else:
            ops+=1; demand(ops<=65536 and opcode in (8,0xf0,0xf1),'OTS_FORMAT')
            arg=b'' if opcode==8 else c.varbytes(4096)
            demand(opcode==8 or len(arg)>0,'OTS_FORMAT')
            result=sha(message) if opcode==8 else message+arg if opcode==0xf0 else arg+message
            demand(len(message)<=4096 and len(result)<=4096,'OTS_FORMAT')
            tasks.append((result,path+((opcode,arg,message),),depth+1))
    c.end('OTS_FORMAT'); return Proof(digest,bitcoin,pending)

class TxReader(Cursor):
    def __init__(self,raw): super().__init__(raw,'OTS_TX_SHAPE')
    def compact(self):
        first=self.uint(1)
        if first<253: return first
        width={253:2,254:4,255:8}[first]; n=int.from_bytes(self.take(width),'little')
        demand(n>={253:253,254:65536,255:4294967296}[first],'OTS_TX_SHAPE'); return n

def transaction(raw):
    c=TxReader(raw); c.take(4); n=c.compact(); demand(1<=n<=len(raw)//41,'OTS_TX_SHAPE')
    for _ in range(n): c.take(36); c.take(c.compact()); c.take(4)
    n=c.compact(); demand(1<=n<=len(raw)//9,'OTS_TX_SHAPE'); scripts=[]
    for _ in range(n): c.take(8); scripts.append(c.take(c.compact()))
    c.take(4); c.end('OTS_TX_SHAPE'); return scripts

def tx_path(att,txid=None):
    path=att.path
    for i in range(len(path)-1):
        if path[i][0]==path[i+1][0]==8:
            # The definition chooses the FIRST consecutive SHA256 pair.
            p=path[i][2]; j=i
            while j>0 and path[j-1][0] in (0xf0,0xf1): j-=1
            m=path[j][2]
            try: scripts=transaction(p)
            except Fault: return False
            if len(m)!=32 or b'\x6a\x20'+m not in scripts: return False
            if txid is not None and sha256d(p)[::-1].hex()!=txid: return False
            suffix=path[i+2:]
            if len(suffix)%3: return False
            for k in range(0,len(suffix),3):
                a,b,c=suffix[k:k+3]
                if a[0] not in (0xf0,0xf1) or len(a[1])!=32 or b[0]!=8 or c[0]!=8: return False
            return True
    return False

@dataclass
class Selected:
    height: int
    time: int
    confirmed: int
    paths: list

def select(proof,headers,pins):
    contradicted=[]; qualifying=[]
    for att in proof.bitcoin:
        h=att.height
        if h in headers and h in pins and sha256d(headers[h])[::-1].hex()==pins[h] and headers[h][36:68]!=att.message:
            contradicted.append(att)
        if any(i not in headers or i not in pins or sha256d(headers[i])[::-1].hex()!=pins[i] for i in range(h,h+6)): continue
        if any(headers[i][4:36]!=sha256d(headers[i-1]) for i in range(h+1,h+6)): continue
        if headers[h][36:68]==att.message: qualifying.append(att)
    if not qualifying: return None,bool(contradicted)
    height=min(a.height for a in qualifying)
    return Selected(height,int.from_bytes(headers[height][68:72],'little'),
                    int.from_bytes(headers[height+5][68:72],'little'),[a for a in qualifying if a.height==height]),bool(contradicted)
