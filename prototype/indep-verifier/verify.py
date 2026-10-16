#!/usr/bin/env python3.14
"""Independent V1 differential instrument. Emits only the stable six on stdout."""
import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from codec import (ALG,PROFILE,Fault,Literal,b64,demand,frame,isotime,jcs,parse_json,
                   parse_signature,public_key,read_anchor,read_frame,registered_codecs,shahex,
                   signature_verifies,sig_policy,utc)
from anchors import parse_ots,select,sha256d,tx_path
from dnssec import interval,parse_snapshot,txt_value,validate_snapshot
from git_channel import dearmor,object_id,parse_commit,parse_tree,verify_path
from policy import parse_catalog,parse_trust
import release_constants as release
import sha1dc

SLOTS=('kms','gpg')
ROWS=['1.1','1.2','1.3','1.4','2.1','2.2','2.3','2.4','3.1','4.1','4.2','5.1','5.2','6.1','6.2','6.3','7.1',
      '8.1','8.2','8.3','8.4','8.5','9.1','9.2','9.3','9.4','9.5','10.1','10.2','10.3',
      '11.1','11.2','11.3','11.4','11.5','12.1','12.2','12.3',
      '13.1','13.2','13.3','13.4','13.5','13.6','13.7',
      '14.1','14.2','14.3','14.4','14.5','14.6','14.7','14.8',
      '15.1','15.2','16.1','17.1','17.2','17.3','17.4']
@dataclass
class Check:
    row:str
    status:str
    reason:str|None=None
    tie:tuple=()

class Ledger:
    def __init__(self): self.checks=[]
    def add(self,row,condition,code,tie=(),unknown=False):
        self.checks.append(Check(row,'pass' if condition else 'unknown' if unknown else 'invalid',None if condition else code,tie))
        return bool(condition)
    def fault(self,row,code,tie=(),unknown=False): return self.add(row,False,code,tie,unknown)
    def run(self,row,fn,*args,tie=()):
        try: value=fn(*args); self.checks.append(Check(row,'pass',tie=tie)); return value
        except Fault as e: self.fault(row,e.code,tie); return None
    def report(self,t):
        rank={r:i for i,r in enumerate(ROWS)}
        for kind,verdict in [('invalid','INVALID'),('unknown','UNVERIFIABLE')]:
            candidates=[c for c in self.checks if c.status==kind and c.reason]
            if candidates:
                winner=min(candidates,key=lambda c:(rank[c.row],c.tie))
                return stable(verdict,winner.reason,t)
        return stable('VALID_STRICT','OK',t)
    def diagnostics(self):
        result=[]
        for row in ROWS:
            seen=[c for c in self.checks if c.row==row]
            result.extend(seen or [Check(row,'blocked')])
        return result

def stable(verdict,reason,t=None):
    return {'historical_security':'NOT_EVALUATED','reason':reason,'revocation':'NOT_EVALUATED',
            'standing':'ABSENT/NOT_ISSUED_IN_PROFILE','T':isotime(t) if t is not None else None,'verdict':verdict}

BINARY={'a_sig','manifest','spec','vectors','preamble','dependency_manifest'}
NESTED={'possession':{'kms','gpg'},'keys':{'kms','gpg'},'receipt_anchor':{'ots','txid'},
        'dns':{'ots','snapshot_body'},'git':{'blob','commit','object_format','ots','trees'},
        'issuer_record':{'observed_anchor_delay_s','policy_version'}}
REQUIRED=BINARY|set(NESTED)-{'issuer_record'}|{'headers'}
DEC=re.compile(r'(?:0|[1-9][0-9]*)\Z')

def decimal_string(v): return isinstance(v,str) and not isinstance(v,Literal) and len(v)<=10 and DEC.fullmatch(v) and int(v)<=4294967295

def container_schema(obj,ledger):
    raw={}; layer=obj['layers'][0]
    if set(obj)!={'profile','layers'}: ledger.fault('2.4','CONTAINER_SCHEMA',('top',))
    if not isinstance(layer,dict): ledger.fault('2.4','CONTAINER_SCHEMA',('layer',)); return raw
    def missing(path): ledger.fault('2.2','GIT_OBJECT_FORMAT_MISSING' if path=='git.object_format' else 'MEMBER_MISSING:'+path,(path.encode('utf-16be'),),True)
    def bad(path): ledger.fault('2.4','CONTAINER_SCHEMA',(path.encode('utf-16be'),))
    def binary(value,path):
        try: raw[path]=b64(value)
        except Fault: bad(path)
    for k in sorted(REQUIRED):
        if k not in layer: missing(k)
    for k,value in layer.items():
        if k in BINARY: binary(value,k)
        elif k in NESTED:
            if not isinstance(value,dict): bad(k); continue
            for f in sorted(NESTED[k]):
                path=k+'.'+f
                if f not in value:
                    if k=='issuer_record': bad(path)
                    else: missing(path)
                    continue
                v=value[f]
                if path=='git.object_format':
                    if not isinstance(v,str) or isinstance(v,Literal): bad(path)
                    else: raw[path]=v; ledger.add('2.3',v=='sha1','GIT_OBJECT_FORMAT',unknown=True)
                elif path=='receipt_anchor.txid':
                    if isinstance(v,str) and not isinstance(v,Literal) and re.fullmatch(r'[0-9a-f]{64}',v): raw[path]=v
                    else: bad(path)
                elif path=='git.trees':
                    if not isinstance(v,list): bad(path)
                    else:
                        if len(v)!=2: bad(path)
                        for i,x in enumerate(v[:2]): binary(x,f'{path}.{i}')
                        for i in range(len(v),2): missing(f'{path}.{i}')
                elif path=='issuer_record.observed_anchor_delay_s':
                    if not decimal_string(v): bad(path)
                elif path=='issuer_record.policy_version':
                    if not isinstance(v,str) or isinstance(v,Literal) or not re.fullmatch(r'tessera-v1-issue-policy/(?:0|[1-9][0-9]*)',v): bad(path)
                else: binary(v,path)
            for f in set(value)-NESTED[k]: bad(k+'.'+f)
        elif k=='headers':
            if not isinstance(value,dict) or not value: bad(k); continue
            for h,v in value.items():
                if not decimal_string(h) or not isinstance(v,str) or isinstance(v,Literal) or not re.fullmatch(r'[0-9a-f]{160}',v): bad('headers.'+h)
                else: raw['headers.'+h]=bytes.fromhex(v)
        else: bad(k)
    for row in ('2.2','2.4'):
        if not any(c.row==row for c in ledger.checks): ledger.add(row,True,'')
    return raw

@dataclass
class AnchorResult:
    selected:object|None
    usable:bool

def anchor_checks(ledger,row,data,expected,headers,pins,kind,txid=None):
    # All branches are evaluated even when an independent stage has failed.
    if data is None: return AnchorResult(None,False)
    receipt=kind=='receipt'; codes={'receipt':'RECEIPT_ANCHOR_MISMATCH','snapshot':'SNAPSHOT_STAMP_MISMATCH','git':'GIT_STAMP_MISMATCH'}
    sub=lambda i: f'11.{i}' if receipt else row
    proof=ledger.run(sub(1),parse_ots,data,tie=(0,))
    if proof is None: return AnchorResult(None,False)
    digest_ok=False
    if expected is not None: digest_ok=ledger.add(sub(2),proof.digest.hex()==shahex(expected),codes[kind],(1,))
    selected,contradicted=select(proof,headers,pins)
    ledger.add(sub(3),not contradicted,'OTS_MERKLE_MISMATCH',(2,))
    no_anchor=('HEADERS_MISSING' if proof.bitcoin else 'ANCHOR_PENDING_ONLY') if receipt else 'SNAPSHOT_NOT_ANCHORED' if kind=='snapshot' else 'GIT_NOT_ANCHORED'
    ledger.add(sub(4),selected is not None,no_anchor,(3,),True)
    if selected:
        if not receipt or txid is not None:
            ledger.add(sub(5),any(tx_path(a,txid if receipt else None) for a in selected.paths),
                       'ANCHOR_TXID_MISMATCH' if receipt else 'OTS_TX_SHAPE',(4,))
    # T requires grammar, digest, no contradiction, qualifying; NOT tx shape.
    return AnchorResult(selected,digest_ok and not contradicted and selected is not None)

def verify_bundle(bundle,config,catalog,request='strict',diagnostics=False):
    if len(bundle)>2**27: return stable('UNVERIFIABLE','OUT_OF_PROFILE')
    try: obj=parse_json(bundle,numbers=False)
    except Fault: return stable('UNVERIFIABLE','OUT_OF_PROFILE')
    if not isinstance(obj,dict) or obj.get('profile')!=PROFILE: return stable('UNVERIFIABLE','OUT_OF_PROFILE')
    if not isinstance(obj.get('layers'),list) or len(obj['layers'])!=1 or request!='strict': return stable('UNVERIFIABLE','OUT_OF_PROFILE')
    ledger=Ledger()
    for row in ('1.1','1.2','1.3','1.4'): ledger.add(row,True,'')
    try: ledger.add('2.1',jcs(obj)==bundle,'JSON_NONCANONICAL')
    except Fault: ledger.fault('2.1','JSON_NONCANONICAL')
    raw=container_schema(obj,ledger)
    headers={int(p.split('.')[1]):data for p,data in raw.items() if p.startswith('headers.')}; pins=config['_pins']
    # Installation input, never inferred from a bundle or its spec lookup.
    catalog_alg=next(iter(catalog.values()))['alg'] if catalog else None
    registry=registered_codecs(catalog_alg)
    anchor=ledger.run('3.1',read_anchor,raw['a_sig'],registry) if 'a_sig' in raw else None
    manifest=ledger.run('4.1',read_frame,raw['manifest'],'tessera-v1/manifest') if 'manifest' in raw else None
    frames=anchor if anchor else []
    commons=[f[1]['common'] for f in frames]
    fps=[manifest['key_fp'],manifest['sset'][0]] if manifest else []
    if manifest:
        for i,co in enumerate(commons): ledger.add('4.2',co['manifest_sha256']==shahex(raw['manifest']),'RECEIPT_MANIFEST_MISMATCH',(i,))
    # Codecs use each frame's own alg within the installed registry (r2-F01).
    supported={i:co['alg']==catalog_alg and co['alg'] in registry for i,co in enumerate(commons)}
    keys={}; bound={}
    for i,slot in enumerate(SLOTS):
        keybytes=raw.get('keys.'+slot)
        if keybytes is not None and supported.get(i):
            # EA-31: installed-spec key rules require catalog-supported alg.
            key=ledger.run('5.1',public_key,keybytes,slot,catalog_alg,tie=(i,)); keys[slot]=key
            if key is not None and manifest:
                bound[slot]=ledger.add('5.2',shahex(keybytes)==fps[i].split(':')[1],'KEY_MISMATCH',(i,))
    if anchor:
        if manifest:
            for i,f in enumerate(frames): ledger.add('6.1',f[1]['signer']['key_fp']==fps[i],'RECEIPT_SLOT',(i,))
        ledger.add('6.2',jcs(commons[0])==jcs(commons[1]),'RECEIPT_COMMON_MISMATCH')
        if manifest:
            for fieldno,field in enumerate(('issuer','alg')):
                for i,co in enumerate(commons): ledger.add('6.3',co[field]==manifest[field],'RECEIPT_MANIFEST_MISMATCH',(fieldno,i))
    entries=[]
    for i,co in enumerate(commons):
        entry=catalog.get(co['spec']['sha256']); entries.append(entry)
        ledger.add('7.1',supported[i],'ALG_UNKNOWN',(i,),True)
        ledger.add('8.1',co['issuer']=='wamason.com'==config['issuer_domain'],'ISSUER_NOT_PINNED',(i,))
        ledger.add('8.2',co['spec']['id']=='tessera-v1-strict/verification-spec/1','SPEC_ID',(i,))
        ledger.add('8.3',entry is not None,'SPEC_UNKNOWN',(i,),True)
        if entry:
            for j,field in enumerate(('vectors_sha256','preamble_sha256')):
                ledger.add('8.4',co[field]==entry[field],'SPEC_OBJECT_MISMATCH',(j,i))
        if co['binding_forms']==['STMT_DIRECT']: ledger.add('8.5',True,'',tie=(0,i))
        for j,f in enumerate(co['binding_forms']):
            if f!='STMT_DIRECT': ledger.fault('8.5','BINDING_FORM_UNSUPPORTED' if f=='STMT_DIGEST' else 'BINDING_FORM_UNKNOWN',(j,i),True)
    for i,slot in enumerate(SLOTS):
        co=commons[i] if i<len(commons) else None
        if anchor and supported.get(i):
            sig=frames[i][3]; policy=ledger.run('9.1',sig_policy,sig,tie=(i,))
            # run returns None for both successful policy and failure: consult checks.
            policy_ok=ledger.checks[-1].status=='pass'
            if policy_ok and keys.get(slot) is not None and bound.get(slot):
                ledger.add('9.2',signature_verifies(frames[i][0],sig,keys[slot]),'SIG_INVALID',(i,))
        possession=raw.get('possession.'+slot)
        if possession is not None:
            alg=co['alg'] if co else (manifest['alg'] if manifest else None)
            if alg is not None:
                parsed=ledger.run('9.3',parse_signature,possession,alg,slot,registry,tie=(i,))
                codec_ok=ledger.checks[-1].status=='pass'
                if codec_ok and supported.get(i):
                    ledger.run('9.4',sig_policy,parsed,tie=(i,)); policy_ok=ledger.checks[-1].status=='pass'
                    if policy_ok and keys.get(slot) is not None and bound.get(slot) and manifest:
                        ledger.add('9.5',signature_verifies(raw['manifest'],parsed,keys[slot]),'POSSESSION_INVALID',(i,))
    for h,header in sorted(headers.items()):
        if h in pins: ledger.add('10.1',sha256d(header)[::-1].hex()==pins[h],'HEADER_CONFLICTS_PIN',(h,))
        ledger.add('10.2',h in pins,'HEADERS_NOT_COVERED',(h,),True)
        if h+1 in headers: ledger.add('10.3',headers[h+1][4:36]==sha256d(header),'HEADER_CHAIN_BROKEN',(h,))
    receipt=anchor_checks(ledger,None,raw.get('receipt_anchor.ots'),raw.get('a_sig'),headers,pins,'receipt',raw.get('receipt_anchor.txid'))
    t=receipt.selected.time if receipt.usable else None
    declared=utc(commons[0]['declared_issue_time']) if commons else None
    if receipt.selected and declared is not None:
        for row,condition,code in [('12.1',receipt.selected.time>=declared-86400,'TIME_BEFORE_DECLARED_EPSILON'),
                                   ('12.2',receipt.selected.time<=declared+259200,'TIME_AFTER_DECLARED_DELTA'),
                                   ('12.3',receipt.selected.confirmed<=declared+259200,'CONFIRMATION_LATE')]: ledger.add(row,condition,code)
    body=raw.get('dns.snapshot_body'); snapshot=None; dns_value=None; envelope=None
    if body is not None:
        if ledger.add('13.1',1<=len(body)<=2**24,'LENGTH_CAP'):
            envelope=bytes([26])+b'tessera-v1/dnssec-snapshot'+len(body).to_bytes(4,'big')+body
            snapshot=ledger.run('13.2',parse_snapshot,body)
    if snapshot: ledger.add('13.3',not snapshot.wildcard,'DNS_WILDCARD')
    snap_anchor=anchor_checks(ledger,'13.4',raw.get('dns.ots'),envelope,headers,pins,'snapshot')
    if snapshot and snap_anchor.usable:
        for i,outcome in enumerate(validate_snapshot(snapshot,config,snap_anchor.selected.time)):
            ledger.add('13.5',outcome.status=='pass',outcome.reason,(i,),outcome.status=='unknown')
    if snapshot:
        if snapshot.txt is None or not snapshot.txt.rr: ledger.fault('13.6','DNS_EVIDENCE_MISSING',unknown=True)
        else:
            owner=(b'_tessera-v1',)+tuple(commons[0]['issuer'].encode().split(b'.')) if commons else None
            if owner is not None: owner_ok=ledger.add('13.6',snapshot.txt.owner==owner,'DNS_OWNER',(0,))
            else: owner_ok=True
            # TXT grammar is independent of authenticated DNSSEC and available frames.
            dns_value=ledger.run('13.6',txt_value,[r.data for r in snapshot.txt.rr],tie=(1,))
    if snap_anchor.selected and declared is not None:
        ledger.add('13.7',declared-86400<=snap_anchor.selected.time<=declared+259200 and snap_anchor.selected.confirmed<=declared+259200,'SNAPSHOT_TIME')
    commit=raw.get('git.commit'); parsed_commit=ledger.run('14.1',parse_commit,commit) if commit is not None else None
    sig=ledger.run('14.2',dearmor,parsed_commit[2]) if parsed_commit else None
    trees=[raw.get('git.trees.'+str(i)) for i in range(2)]; parsed_trees=[]
    for i,tree in enumerate(trees): parsed_trees.append(ledger.run('14.3',parse_tree,tree,tie=(i,)) if tree is not None else None)
    blob=raw.get('git.blob'); path_ok=False
    if commit is not None or any(tree is not None for tree in trees) or blob is not None:
        # Row 14.4 via the owner-pinned SHA-1DC (sha1dc.py; operator hook 2026-10-14).
        # Without the pinned detector: explicit residual; never pretend hashlib implements SHA-1DC.
        if not sha1dc.available(): ledger.fault('14.4','INDEPENDENT_SHA1DC_UNAVAILABLE',unknown=True)
        else:
            for i,(kind,body) in enumerate([('commit',commit),('tree',trees[0]),('tree',trees[1]),('blob',blob)]):
                if body is None: continue
                try: ledger.add('14.4',not sha1dc.collision(kind,body),'GIT_SHA1_COLLISION',(i,))
                except sha1dc.Unavailable: ledger.fault('14.4','INDEPENDENT_SHA1DC_UNAVAILABLE',(i,),unknown=True)
    if parsed_commit and all(tree is not None for tree in parsed_trees) and blob is not None:
        ledger.run('14.5',verify_path,parsed_commit[0],trees,blob); path_ok=ledger.checks[-1].status=='pass'
    stamped=(object_id('commit',commit)+'\n').encode() if commit is not None else None
    git_anchor=anchor_checks(ledger,'14.6',raw.get('git.ots'),stamped,headers,pins,'git')
    if parsed_commit and sig is not None and git_anchor.usable:
        states=[]
        for e in config['repository_keys']:
            if e['domain']==config['issuer_domain'] and signature_verifies(parsed_commit[1],sig,e['_public']): states.append(interval(e,git_anchor.selected.time,utc(config['as_of'])))
        if 'pass' in states: ledger.add('14.7',True,'')
        elif 'horizon' in states: ledger.fault('14.7','TRUST_HORIZON',unknown=True)
        elif 'outside' in states: ledger.fault('14.7','GIT_SIGNER_OUTSIDE_INTERVAL')
        else: ledger.fault('14.7','GIT_SIGNER_NOT_CONFIGURED',unknown=True)
    if receipt.selected and git_anchor.selected:
        ledger.add('14.8',git_anchor.selected.height+5<receipt.selected.height,'GIT_NOT_PRECOMMITTED')
    if dns_value and manifest:
        for i,slot in enumerate(SLOTS): ledger.add('15.1',dns_value[slot]==fps[i].split(':')[1],'DNS_KEY_MISMATCH',(i,))
    if dns_value and path_ok: ledger.add('15.2',blob==dns_value['_raw'],'CHANNEL_VALUE_MISMATCH')
    if dns_value and declared is not None and receipt.selected:
        ledger.add('16.1',declared>=dns_value['_start'] and receipt.selected.time<=dns_value['_end'],'ISSUANCE_WINDOW')
    for i,co in enumerate(commons):
        for j,(member,target) in enumerate([('spec',co['spec']['sha256']),('vectors',co['vectors_sha256']),('preamble',co['preamble_sha256'])],1):
            if member in raw: ledger.add('17.'+str(j),shahex(raw[member])==target,'BUNDLE_OBJECT_HASH',(i,))
        if entries[i] and 'dependency_manifest' in raw:
            ledger.add('17.4',shahex(raw['dependency_manifest'])==entries[i]['dependency_manifest_sha256'],'BUNDLE_OBJECT_HASH',(i,))
    result=ledger.report(t)
    return (result,ledger) if diagnostics else result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--trust',required=True); parser.add_argument('--bundle',required=True); parser.add_argument('--catalog')
    args=parser.parse_args()
    try:
        demand(sys.version_info[:2]==(3,14),'RUNTIME_UNSUPPORTED')
        demand(unicodedata.unidata_version==release.UNICODE_VERSION,'UNICODE_TABLES_UNSUPPORTED')
        trust=Path(args.trust).read_bytes()
        demand(release.TRUST_SHA256 is not None and shahex(trust)==release.TRUST_SHA256,'TRUST_CONFIG_UNAUTHENTICATED')
        config=parse_trust(trust)
        demand(release.UNICODE_MODULE_SHA256 is not None and shahex(Path(getattr(unicodedata,'__file__',sys.executable)).read_bytes())==release.UNICODE_MODULE_SHA256,'UNICODE_TABLES_UNSUPPORTED')
        catalog_raw=Path(args.catalog).read_bytes() if args.catalog else release.CATALOG_BYTES
        demand(catalog_raw is not None and shahex(catalog_raw)==release.CATALOG_SHA256,'CATALOG_UNAUTHENTICATED')
        catalog=parse_catalog(catalog_raw)
        # Bound the read, not just the later parse.
        with open(args.bundle,'rb') as f: bundle=f.read(2**27+1)
        print(jcs(verify_bundle(bundle,config,catalog)).decode())
        return 0
    except Fault as e: print(e.code,file=sys.stderr); return 2
    except OSError as e: print('INPUT_IO_ERROR: '+str(e),file=sys.stderr); return 2
if __name__=='__main__': raise SystemExit(main())
