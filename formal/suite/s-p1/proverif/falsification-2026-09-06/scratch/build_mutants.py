from pathlib import Path
import re
models={'D':'sp1_q1_strict_dns_compromised','R':'sp1_q1_strict_repo_compromised','G':'sp1_q2_degraded_compromised'}
common={
 'fp':('  if fp(kX) = kfpr then',''),
 'possession':('  let (=POSS, =t) = checksign(ppf, kX) in',''),
 'poss_tag':('let (=POSS, =t) = checksign(ppf, kX)','let (possTag: bitstring, =t) = checksign(ppf, kX)'),
 'poss_manifest':('let (=POSS, =t) = checksign(ppf, kX)','let (=POSS, possManifest: bitstring) = checksign(ppf, kX)'),
 'signature':('  let (=BYTES, =fb) = checksign(sg, kX) in',''),
 'sig_tag':('let (=BYTES, =fb) = checksign(sg, kX)','let (sigTag: bitstring, =fb) = checksign(sg, kX)'),
 'sig_bytes':('let (=BYTES, =fb) = checksign(sg, kX)','let (=BYTES, signedBytes: bitstring) = checksign(sg, kX)'),
 'sig_key':('let (=BYTES, =fb) = checksign(sg, kX)','in(c, sigKey: pkey);\n  let (=BYTES, =fb) = checksign(sg, sigKey)'),
 'frame_alg':('framed(ot, =alg, =id, =fp(kX), mh, cv, pl) = fb','framed(ot, frameAlg, =id, =fp(kX), mh, cv, pl) = fb'),
 'frame_id':('framed(ot, =alg, =id, =fp(kX), mh, cv, pl) = fb','framed(ot, =alg, frameId, =fp(kX), mh, cv, pl) = fb'),
 'frame_fp':('framed(ot, =alg, =id, =fp(kX), mh, cv, pl) = fb','framed(ot, =alg, =id, frameFp, mh, cv, pl) = fb'),
 'manifest_hash':('  if mh = h(t) then',''),
 'tuple_binding':('  let authTuple(id, kfpr, ss, alg, ver) = t in','  in(c, (id: bitstring, kfpr: bitstring, ss: bitstring, alg: bitstring, ver: bitstring));'),
 'frame_binding':('  let framed(ot, =alg, =id, =fp(kX), mh, cv, pl) = fb in','  in(c, mh: bitstring);'),
}
for mode,name in models.items():
 src=Path('proverif/'+name+'.pv').read_text()
 edits=dict(common)
 for ev,key in ([('ev','pkS')] if mode=='G' else [('evD','pkD'),('evR','pkR')]):
  line=f'  let (=STMT_DIGEST, =h(t)) = checksign({ev}, {key}) in'
  edits[ev]=(line,'')
  edits[ev+'_tag']=(line,line.replace('=STMT_DIGEST','evidenceTag: bitstring'))
  edits[ev+'_digest']=(line,line.replace('=h(t)','evidenceDigest: bitstring'))
  edits[ev+'_key']=(line,f'  in(c, evidenceKey: pkey);\n'+line.replace(', '+key+')',', evidenceKey)'))
 for label,(old,new) in edits.items():
  start=src.index('let Verifier')
  end=src.index('out(acceptCh, (kX, fb)).',start)+len('out(acceptCh, (kX, fb)).')
  body=src[start:end]
  assert body.count(old)==1,(name,label,body.count(old))
  changed=src[:start]+body.replace(old,new)+src[end:]
  Path(f'scratch/m_{mode}_{label}.pv').write_text(f'(* REVIEW MUTANT: {name}; unbind/remove {label}; inherited header describes baseline only. *)\n'+changed)
print('Generated',len(list(Path('scratch').glob('m_*.pv'))),'mutants')
