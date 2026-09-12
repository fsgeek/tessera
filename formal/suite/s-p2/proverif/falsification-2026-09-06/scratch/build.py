from pathlib import Path
import re,json
root=Path('proverif'); dst=Path('scratch'); jobs=[]
models={'D':'sp2_q1_strict_dns_compromised','R':'sp2_q1_strict_repo_compromised','G':'sp2_q2_degraded_compromised','C3':'sp2_q5_c3_manifestposs_frame_nomh'}
for alias,name in models.items():
 s=(root/(name+'.pv')).read_text(); lines=s.splitlines(True); start=s.index('let Verifier'); end=s.index('let SetJudge')
 offset=0
 for i,line in enumerate(lines):
  inside=start<=offset<end; offset+=len(line)
  if not inside: continue
  variants=[]
  if line.lstrip().startswith('if '): variants.append(('drop', '  (* removed check *)\n'))
  if 'checksign(' in line:
   variants.append(('drop','  (* removed signature check *)\n'))
   tag=next(x for x in ['STMT_DIGEST','POSS','BYTES'] if '='+x in line)
   variants.append(('tag',line.replace('='+tag,'tagLoose: bitstring')))
   match=re.search(r', =(.*?)\) = checksign',line)
   if match: variants.append(('binding',line[:match.start(1)-1]+'valueLoose: bitstring'+line[match.end(1):]))
  if 'let authTuple' in line and '=signers0' in line: variants.append(('arity',line.replace('=signers0','ssLoose')))
  if 'let framed' in line:
   for token,label in [('=alg','alg'),('=id','id'),('=fp(kA)','fp'),('=fp(kB)','fp')]:
    if token in line: variants.append((label,line.replace(token,label+'Loose')))
  for label,new in variants:
   out=lines.copy(); out[i]=new
   p=dst/f'm_{alias}_{i+1}_{label}.pv'; p.write_text(''.join(out));jobs.append({'file':str(p),'base':alias,'line':i+1,'kind':label})
base=(root/(models['D']+'.pv')).read_text()
def attack(name,s,cond,branch=2):
 s=s.replace('(* --- registered queries', 'event Attack.\nquery event(Attack).\n\n(* --- registered queries',1)
 marker='  event Accept2(evD, evR, t, kA, kB, fa, fb);' if branch==2 else '  event Accept(evD, evR, t, kA, fa);'
 # parallel monitor preserves verifier continuation
 pos=s.index(marker)+len(marker); tail=s[pos:]; stop=tail.index(' ).')
 s=s[:pos]+'\n  ( ('+cond+' event Attack) | '+tail[:stop]+' )'+tail[stop:]
 p=dst/f'a_{name}.pv';p.write_text(s);jobs.append({'file':str(p),'attack':name})
attack('mixed_payload',base,'let framed(x1,x2,x3,x4,x5,x6,p1) = fa in let framed(y1,y2,y3,y4,y5,y6,p2) = fb in if p1 <> p2 then')
attack('duplicate_signature',base,'if kA = kB && sgA = sgB then')
attack('reordered_keys',base,'if kA = pk(skB2) && kB = pk(skA2) then')
fb='framed(OT_ATTEST, algH, issuerId2, fp(pk(skB2)), h(authTuple(issuerId2, fp(pk(skA2)), signers1(fp(pk(skB2))), algH, verH)), canonVerH, fbH)'
attack('dsks',base,f'if kB = pk(dsks(sign((BYTES, {fb}), skB2), fbH)) then')
attack('shrink',base,'if t = authTuple(issuerId2, fp(pk(skA2)), signers0, algH, verH) then',1)
s=base.replace('  out(c, m1); out(c, m2);','  let m3 = authTuple(issuerId, fp(pk(skA1)), signers0, algH, fbH) in\n  out(c, m3); out(c, m1); out(c, m2);').replace('  | !Registrar(m1)', '  | !AuthorityDNS(skD, m3) | !AuthorityRepo(skR, m3) | !Registrar(m3) | !Signer(skA1, issuerId, m3)\n  | !Registrar(m1)')
p=dst/'a_key_reuse.pv';p.write_text(s);jobs.append({'file':str(p),'attack':'key_reuse'})
start=base.index('let Signer(');end=base.index('(* Verifier, n = 1',start)
producer=base[start:end].replace('let Signer(', 'let WrapperSigner(').replace('OT_ATTEST','OT_WRAPPER')
s=base[:end]+producer+base[end:];s=s.replace('| !Signer(skA1, issuerId,  m1)','| !WrapperSigner(skA1, issuerId, m1) | !Signer(skA1, issuerId,  m1)')
attack('wrapper_replay',s,'let framed(=OT_WRAPPER,x2,x3,x4,x5,x6,x7) = fa in',1)
(dst/'jobs.json').write_text(json.dumps(jobs,indent=2))
print(len(jobs),'jobs')
