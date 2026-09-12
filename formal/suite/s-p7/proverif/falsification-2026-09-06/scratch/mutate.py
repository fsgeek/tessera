from pathlib import Path
import re,json
sources={'q1d':'sp7_q1_strict_dns_compromised','q1r':'sp7_q1_strict_repo_compromised','q2':'sp7_q2_degraded_compromised','q4o':'sp7_q4_control_opaque_twoversion','q5':'sp7_q5_depth2_correct'}
records=[]
for short,stem in sources.items():
 s=Path('proverif',stem+'.pv').read_text(); lines=s.splitlines()
 Path('scratch',short+'_baseline.pv').write_text(s)
 active=False
 for i,line in enumerate(lines):
  if line.startswith('let InnerCheck'): active=True
  if '(* --- judges' in line: active=False
  if not active: continue
  changes={}
  m=re.search(r'let \(=STMT_DIGEST, =h\(t([IWOM])\)\) = checksign\((\w+), (\w+)\) in',line)
  if m:
   level=m[1]; ev=m[2]
   changes={f'{level}_{ev}_evidence':'(* removed evidence check *)',f'{level}_{ev}_tag':line.replace('=STMT_DIGEST','unusedTag'),f'{level}_{ev}_digest':line.replace('=h(t'+level+')','unusedDigest')}
  m=re.search(r'if fp\(k([IWOM])\) = kfpr\1 then',line)
  if m: changes={m[1]+'_slot':'(* removed slot check *)'}
  m=re.search(r'let \(=POSS, =t([IWOM])\) = checksign',line)
  if m:
   l=m[1]; changes={l+'_possession':'(* removed possession check *)',l+'_poss_tag':line.replace('=POSS','unusedTag'),l+'_poss_manifest':line.replace('=t'+l,'unusedManifest')}
  m=re.search(r'let \(=BYTES, =fb([IWOM])\) = checksign',line)
  if m:
   l=m[1];changes={l+'_signature':'(* removed signature check *)',l+'_sig_tag':line.replace('=BYTES','unusedTag'),l+'_sig_bytes':line.replace('=fb'+l,'unusedBytes')}
  m=re.search(r'framed\(=(OT_\w+), =alg([IWOM]), =id\2, =fp\(k\2\)',line)
  if m:
   l=m[2]; changes={l+'_type':line.replace('='+m[1],'unusedType'),l+'_alg':line.replace('=alg'+l,'unusedAlg'),l+'_id':line.replace('=id'+l,'unusedId'),l+'_fp':line.replace('=fp(k'+l+')','unusedFp')}
  m=re.search(r'if mh([IWOM]) = h\(t\1\) then',line)
  if m:changes={m[1]+'_hash':'(* removed manifest hash check *)'}
  for name,replacement in changes.items():
   # Keep syntax for Q5 middle branch's leading parallel bar.
   if line.lstrip().startswith('| ') and not replacement.lstrip().startswith('| '): replacement='  | '+replacement
   out=lines.copy();out[i]=replacement
   target=f'{short}_{name}'
   Path('scratch',target+'.pv').write_text('\n'.join(out)+'\n')
   records.append(dict(name=target,source='proverif/'+stem+'.pv',line=i+1,old=line,new=replacement))
Path('scratch/mutations.json').write_text(json.dumps(records,indent=2))
print(len(records),'single-check mutants')
