"""Offline release inputs. No policy is learned from a bundle."""
import re
from codec import Fault,demand,parse_json,b64,utc,HEX,PROFILE,ALG,public_key
from dnssec import dnskey,keytag

TRUST_KEYS={'format','profile','version','previous_sha256','as_of','issuer_domain','header_pins','root_ksks','repository_keys'}
KSK_KEYS={'name','key_tag','algorithm','dnskey_rdata','ds_sha256','signing_start','signing_end','reliance_lifetime_s','publication','revocation','sources'}
REPO_KEYS={'domain','key','signing_end','signing_start','sources'}
CAT_KEYS={'spec_sha256','vectors_sha256','preamble_sha256','dependency_manifest_sha256','alg','alg_prohibited','binding_forms','issuer_domain','delta_s','epsilon_s','k','dnssec_algorithms','ds_digest_types'}

def closed(obj,keys): demand(isinstance(obj,dict) and set(obj)==keys,'TRUST_CONFIG_UNAUTHENTICATED')
def dec(value,low=0,high=4294967295):
    demand(isinstance(value,str) and re.fullmatch(r'0|[1-9][0-9]*',value) and len(value)<=10,'TRUST_CONFIG_UNAUTHENTICATED')
    n=int(value); demand(low<=n<=high,'TRUST_CONFIG_UNAUTHENTICATED'); return n

def hex64(value): demand(isinstance(value,str) and HEX.fullmatch(value),'TRUST_CONFIG_UNAUTHENTICATED')
def sources(items):
    demand(isinstance(items,list) and bool(items),'TRUST_CONFIG_UNAUTHENTICATED')
    for item in items:
        closed(item,{'description','sha256','uri'}); hex64(item['sha256'])
        demand(isinstance(item['description'],str) and isinstance(item['uri'],str),'TRUST_CONFIG_UNAUTHENTICATED')

def period(entry,as_of):
    start=utc(entry['signing_start']); end=entry['signing_end']
    demand(start<=(as_of if end is None else utc(end)),'TRUST_CONFIG_UNAUTHENTICATED')

def parse_trust(raw):
    try:
        from codec import shahex
        obj=parse_json(raw,canonical=True,no_numbers=True); closed(obj,TRUST_KEYS)
        demand(obj['format']=='tessera-v1-trust/1' and obj['profile']==PROFILE and obj['issuer_domain']=='wamason.com','TRUST_CONFIG_UNAUTHENTICATED')
        version=dec(obj['version'],1); hex64(obj['previous_sha256']); as_of=utc(obj['as_of'])
        demand(version!=1 or obj['previous_sha256']=='0'*64,'TRUST_CONFIG_UNAUTHENTICATED')
        pins=obj['header_pins']; demand(isinstance(pins,dict) and bool(pins),'TRUST_CONFIG_UNAUTHENTICATED')
        for h,v in pins.items(): dec(h); hex64(v)
        roots=obj['root_ksks']; repos=obj['repository_keys']
        demand(isinstance(roots,list) and bool(roots) and isinstance(repos,list) and bool(repos),'TRUST_CONFIG_UNAUTHENTICATED')
        orders=[]; names=[]; keys=[]
        for e in roots:
            closed(e,KSK_KEYS); key=b64(e['dnskey_rdata']); alg,pub=dnskey(key)
            demand(key[:3]==b'\x01\x01\x03' and alg in (8,13),'TRUST_CONFIG_UNAUTHENTICATED')
            demand(dec(e['key_tag'],0,65535)==keytag(key) and dec(e['algorithm'],0,255)==alg,'TRUST_CONFIG_UNAUTHENTICATED')
            hex64(e['ds_sha256']); demand(e['ds_sha256']==shahex(b'\x00'+key),'TRUST_CONFIG_UNAUTHENTICATED')
            demand(isinstance(e['name'],str),'TRUST_CONFIG_UNAUTHENTICATED'); names.append(e['name']); keys.append(key)
            period(e,as_of); dec(e['reliance_lifetime_s'],1,2592000); sources(e['sources'])
            for f in ('publication','revocation'):
                if e[f] is not None: utc(e[f])
            orders.append((e['signing_start'],int(e['key_tag']),key)); e['_key']=key
        demand(orders==sorted(orders) and len(set(names))==len(names) and len(set(keys))==len(keys),'TRUST_CONFIG_UNAUTHENTICATED')
        orders=[]; keys=[]
        for e in repos:
            closed(e,REPO_KEYS); demand(e['domain']==obj['issuer_domain'],'TRUST_CONFIG_UNAUTHENTICATED')
            key=b64(e['key']); pub=public_key(key,'gpg'); period(e,as_of); sources(e['sources'])
            orders.append((e['signing_start'],key)); keys.append(key); e['_key']=key; e['_public']=pub
        demand(orders==sorted(orders) and len(set(keys))==len(keys),'TRUST_CONFIG_UNAUTHENTICATED')
        obj['_pins']={int(k):v for k,v in pins.items()}; return obj
    except (Fault,TypeError,ValueError,KeyError,OverflowError): raise Fault('TRUST_CONFIG_UNAUTHENTICATED') from None

def parse_catalog(raw):
    """Instrument transport for the profile's one immutable catalog entry."""
    try:
        obj=parse_json(raw,canonical=True,no_numbers=True); closed(obj,{'format','entries'})
        demand(obj['format']=='tessera-v1-independent-catalog/1' and isinstance(obj['entries'],list) and len(obj['entries'])==1,'CATALOG_UNAUTHENTICATED')
        e=obj['entries'][0]; closed(e,CAT_KEYS)
        for field in ('spec_sha256','vectors_sha256','preamble_sha256','dependency_manifest_sha256'): hex64(e[field])
        demand(isinstance(e['alg'],str) and re.fullmatch(r'[A-Z0-9][A-Z0-9-]{0,63}',e['alg']),'CATALOG_UNAUTHENTICATED')
        demand(e['alg_prohibited']==[] and e['binding_forms']==['STMT_DIRECT'] and e['issuer_domain']=='wamason.com','CATALOG_UNAUTHENTICATED')
        demand(e['delta_s']=='259200' and e['epsilon_s']=='86400' and e['k']=='6' and e['dnssec_algorithms']==['8','13'] and e['ds_digest_types']==['2','4'],'CATALOG_UNAUTHENTICATED')
        return {e['spec_sha256']:e}
    except (Fault,TypeError,ValueError,KeyError): raise Fault('CATALOG_UNAUTHENTICATED') from None

def check_extension(previous,current,previous_raw):
    """Build-time append-only checker, not an offline previous-config fetch."""
    from codec import shahex
    demand(int(current['version'])==int(previous['version'])+1 and current['previous_sha256']==shahex(previous_raw),'TRUST_CONFIG_UNAUTHENTICATED')
    demand(utc(current['as_of'])>=utc(previous['as_of']),'TRUST_CONFIG_UNAUTHENTICATED')
    demand(current['issuer_domain']==previous['issuer_domain'],'TRUST_CONFIG_UNAUTHENTICATED')
    for height,pin in previous['header_pins'].items(): demand(current['header_pins'].get(height)==pin,'TRUST_CONFIG_UNAUTHENTICATED')
    for category,keyfield,extension in [('root_ksks','dnskey_rdata',True),('repository_keys','key',False)]:
        for old in previous[category]:
            new=next((e for e in current[category] if e[keyfield]==old[keyfield]),None)
            demand(new is not None,'TRUST_CONFIG_UNAUTHENTICATED')
            immutable=('name','key_tag','algorithm','dnskey_rdata','ds_sha256','signing_start','reliance_lifetime_s') if extension else ('domain','key','signing_start')
            for f in immutable: demand(old[f]==new[f],'TRUST_CONFIG_UNAUTHENTICATED')
            if old['signing_end'] is not None: demand(new['signing_end']==old['signing_end'],'TRUST_CONFIG_UNAUTHENTICATED')
            elif new['signing_end'] is not None:
                end=utc(new['signing_end'])+(int(new['reliance_lifetime_s']) if extension else 0)
                demand(end>=utc(previous['as_of']),'TRUST_CONFIG_UNAUTHENTICATED')
