from pathlib import Path
import re
root=Path('.')
models={'dns':'ss_q1_strict_dns_compromised','repo':'ss_q1_strict_repo_compromised','deg':'ss_q1d_degraded_compromised'}
manifest=[]
for mode,name in models.items():
 s=(root/'proverif'/f'{name}.pv').read_text()
 start=s.index('let StandingPath('); end=s.index('(* --- judges')
 def emit(label,text,desc):
  p=root/'scratch'/f'm_{mode}_{label}.pv';p.write_text('(* REVIEW MUTANT: '+desc+'; original header below is not a claim about this mutant. *)\n'+text);manifest.append((p.name,desc))
 def patch(label,old,new,scope='standing'):
  a,b=(start,s.index('(* --- the envelope path',start)) if scope=='standing' else ((s.index('let EnvelopePath('),end) if scope=='envelope' else (0,len(s)))
  sub=s[a:b];assert old in sub,(mode,label);sub=sub.replace(old,new,1);emit(label,s[:a]+sub+s[b:],label)
 for channel in (['S'] if mode=='deg' else ['D','R']):
  ev='ev' if mode=='deg' else 'ev'+channel
  old=f'let (=STMT_DIGEST, =h(t)) = checksign({ev}, pk{channel}) in'
  patch('authority'+channel,old,'')
  patch('authority_digest'+channel,old,old.replace('=h(t)','ignoredDigest'))
 patch('entitled','if fp(kT) = kfpr then','if true then')
 patch('key_equal','if kT = kX then','if true then')
 patch('signature_key','let (=TLR, (lin: bitstring, terminal: bitstring, declT: bitstring)) = checksign(tlrSig, kT) in','in(c, uncheckedKey: pkey);\n          let (=TLR, (lin: bitstring, terminal: bitstring, declT: bitstring)) = checksign(tlrSig, uncheckedKey) in')
 patch('tlr_tag','let (=TLR,','let (uncheckedTag,')
 patch('anchor','let anchorProof(=h(tlrSig)) = ap in','let ignoredAnchor = ap in')
 patch('lookup','let d = lookup2(aid, lin) in','let d = DISP_SHIPPED in')
 patch('terminal_identity','if shippedId = aid then','if true then','all')
 patch('entry_disposition','if d = DISP_SHIPPED then','if true then','all')
 patch('refused_branch','if terminal = TERM_REFUSED then','if false then','all')
 patch('missing_branch','if se = noTLR then','if false then')
 # Each envelope predicate independently; unbind matching fields without deleting required variable bindings.
 env=[('fingerprint','if fp(kX) = kfpr then',''),('core_tuple','let attemptCore(=t,','let attemptCore(ignoredTuple,'),('possession','let (=POSS, =t) = checksign(ppf, kX) in',''),('bytes','let (=BYTES, =fb) = checksign(sg, kX) in',''),('frame_alg','=alg, =id,','=ignoredNever, =id,')]
 for lab,old,new in env[:4]:patch('env_'+lab,old,new,'envelope')
 for field in ['alg','id','fp(kX)']:
  patch('env_frame_'+{'alg':'alg','id':'id','fp(kX)':'fp'}[field],'='+field, 'ignoredField','envelope')
 patch('env_manifest','if mh = h(t) then','','envelope')
 for channel in (['S'] if mode=='deg' else ['D','R']):
  ev='ev' if mode=='deg' else 'ev'+channel
  patch('env_authority'+channel,f'let (=STMT_DIGEST, =h(t)) = checksign({ev}, pk{channel}) in','','envelope')
 # remove whole envelope process, leaving its definition unused
 call='!EnvelopePath(pkS)' if mode=='deg' else '!EnvelopePath(pkD), pkR)' # handled literally below
 call='!EnvelopePath(pk(skS))' if mode=='deg' else '!EnvelopePath(pk(skD), pk(skR))'
 emit('envelope',s.replace(' | '+call,''),'remove envelope process')
base=(root/'proverif'/f"{models['dns']}.pv").read_text()
def attack(name,query,modify=lambda s:s,decl=''):
 s=modify(base);s=s.replace('(* --- queries',decl+'\n(* --- queries',1);s=s.replace('(* --- authority channels',query+'\n(* --- authority channels',1)
 p=root/'scratch'/f'a_{name}.pv';p.write_text('(* REVIEW ATTACK: unchanged verifier; original header applies only to original fixture. *)\n'+s);manifest.append((p.name,name))
attack('wrapper','query k:pkey,t:bitstring,x:bitstring,y:bitstring; event(Established(k,t,h(wrapCore(x,y)))).')
attack('dsks','query s:bitstring,r:bitstring,t:bitstring,a:bitstring; event(Established(pk(dsks(s,r)),t,a)).')
# Re-contextualize a valid core under another honestly published tuple naming the same key.
alias='authTuple(issuerId2, fp(pk(skH1)), ssetH, algH, verH)'
attack('alias_replay',f'query p:bitstring,s:bitstring,d:bitstring; event(Established(pk(skH1),{alias},h(attemptCore(authTuple(issuerId,fp(pk(skH1)),ssetH,algH,verH),p,s,d)))).',lambda s:s.replace('| !Judge | !ReasonJudge',f'| !AuthorityDNS(skD,{alias}) | !AuthorityRepo(skR,{alias})\n  | !Judge | !ReasonJudge'))
# Third legitimate issuer, adversary controls its OWN key, no authority key beyond DNS is leaked.
at='authTuple(attackerId,fp(pk(skA)),ssetH,algH,verH)'
attack('own_registered_key',f'query a:bitstring; event(Established(pk(skA),{at},a)).',lambda s:s.replace('| !Judge | !ReasonJudge',f'| !AuthorityDNS(skD,{at}) | !AuthorityRepo(skR,{at})\n  | !Judge | !ReasonJudge'), 'free skA:skey.\nfree attackerId:bitstring.')
# A1.3 omission: fixed fixture ships a public core but carries no TLR in an explicitly submitted bundle.
attack('omit_tlr','query p:bitstring,s:bitstring,d:bitstring; event(StandingReport(ABSENT,NO_TERMINAL_DISPOSITION_EVIDENCE,pk(skH1),authTuple(issuerId,fp(pk(skH1)),ssetH,algH,verH),h(attemptCore(authTuple(issuerId,fp(pk(skH1)),ssetH,algH,verH),p,s,d)))).')
(root/'scratch'/'manifest.tsv').write_text('\n'.join('\t'.join(x) for x in manifest)+'\n')
