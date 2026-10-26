"""Git's closed V1 subset. SHA-1 hashing alone does not supply SHA-1DC."""
import base64
import hashlib
import re
from .codec import Fault, demand, b64, parse_signature, sig_policy

LHEX=re.compile(rb'[0-9a-f]{40}\Z')

def object_id(kind,body):
    return hashlib.sha1(kind.encode()+b' '+str(len(body)).encode()+b'\x00'+body).hexdigest()

def parse_commit(raw):
    try:
        end=raw.index(b'\n\n'); lines=raw[:end].split(b'\n'); i=0
        demand(lines[0].startswith(b'tree ') and LHEX.fullmatch(lines[0][5:]),'GIT_COMMIT_FORMAT')
        tree=lines[0][5:].decode(); i=1; parents=[]
        while i<len(lines) and lines[i].startswith(b'parent '):
            parent=lines[i][7:]; demand(LHEX.fullmatch(parent) and parent not in parents,'GIT_COMMIT_FORMAT'); parents.append(parent); i+=1
        demand(i+2<len(lines) and lines[i].startswith(b'author ') and lines[i+1].startswith(b'committer '),'GIT_COMMIT_FORMAT')
        # Author and committer bytes uninterpreted, but each required header has a value.
        demand(len(lines[i])>7 and len(lines[i+1])>10,'GIT_COMMIT_FORMAT'); i+=2; begin=i
        demand(lines[i].startswith(b'gpgsig '),'GIT_COMMIT_FORMAT'); armor=[lines[i][7:]]; i+=1
        while i<len(lines) and lines[i].startswith(b' '): armor.append(lines[i][1:]); i+=1
        demand(i==len(lines),'GIT_COMMIT_FORMAT')
        payload=b'\n'.join(lines[:begin])+b'\n\n'+raw[end+2:]
        return tree,payload,b'\n'.join(armor)
    except (ValueError,IndexError): raise Fault('GIT_COMMIT_FORMAT') from None

def crc24(raw):
    crc=0xb704ce
    for octet in raw:
        crc^=octet<<16
        for _ in range(8):
            crc<<=1
            if crc&0x1000000: crc^=0x1864cfb
    return (crc&0xffffff).to_bytes(3,'big')

def dearmor(raw):
    try:
        lines=raw.split(b'\n')
        demand(len(lines)>=4 and lines[:2]==[b'-----BEGIN PGP SIGNATURE-----',b''] and lines[-1]==b'-----END PGP SIGNATURE-----','GIT_SIG_FORMAT')
        body=lines[2:-1]; crc=None
        if body and body[-1].startswith(b'='):
            demand(re.fullmatch(rb'=[A-Za-z0-9+/]{4}',body[-1]),'GIT_SIG_FORMAT'); crc=base64.b64decode(body.pop()[1:])
        demand(bool(body) and all(re.fullmatch(rb'[A-Za-z0-9+/=]{1,76}',line) for line in body),'GIT_SIG_FORMAT')
        demand(all(b'=' not in line for line in body[:-1]),'GIT_SIG_FORMAT')
        data=b64(b''.join(body).decode('ascii'))
        demand(crc is None or crc==crc24(data),'GIT_SIG_FORMAT')
        sig=parse_signature(data); sig_policy(sig); return sig
    except (Fault,ValueError,UnicodeError): raise Fault('GIT_SIG_FORMAT') from None

def parse_tree(raw):
    pos=0; out={}; last=None
    while pos<len(raw):
        try:
            sp=raw.index(b' ',pos); nul=raw.index(b'\x00',sp+1); mode=raw[pos:sp]; name=raw[sp+1:nul]
            demand(mode in (b'40000',b'100644',b'100755',b'120000',b'160000') and name and b'/' not in name and name not in (b'.',b'..'),'GIT_TREE_FORMAT')
            demand(len(raw)-nul-1>=20 and name not in out,'GIT_TREE_FORMAT'); key=name+(b'/' if mode==b'40000' else b'')
            demand(last is None or key>last,'GIT_TREE_FORMAT'); last=key
            out[name]=(mode,raw[nul+1:nul+21].hex()); pos=nul+21
        except ValueError: raise Fault('GIT_TREE_FORMAT') from None
    return out

def verify_path(commit_tree,trees,blob):
    root,sub=trees
    demand(commit_tree==object_id('tree',root),'GIT_PATH')
    root_entries=parse_tree(root); sub_entries=parse_tree(sub)
    demand(root_entries.get(b'tessera-v1')==(b'40000',object_id('tree',sub)),'GIT_PATH')
    demand(sub_entries.get(b'key-assertion')==(b'100644',object_id('blob',blob)),'GIT_PATH')
