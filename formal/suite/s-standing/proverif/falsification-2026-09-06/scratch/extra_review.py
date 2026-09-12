from pathlib import Path
for mode,name in {'dns':'ss_q1_strict_dns_compromised','repo':'ss_q1_strict_repo_compromised','deg':'ss_q1d_degraded_compromised'}.items():
 s=Path('proverif',name+'.pv').read_text()
 def emit(lab,text):Path('scratch',f'm_{mode}_{lab}.pv').write_text('(* REVIEW single-check mutant; original header below is not asserted. *)\n'+text)
 a=s.index('let StandingPath(');b=s.index('(* --- the envelope path',a)
 sub=s[a:b]
 emit('lookup_identity',s[:a]+sub.replace('let d = lookup2(aid, lin) in','in(c, lookupId: bitstring);\n                  let d = lookup2(lookupId, lin) in')+s[b:])
 for ch in (['S'] if mode=='deg' else ['D','R']):
  ev='ev' if ch=='S' else 'ev'+ch
  old=f'let (=STMT_DIGEST, =h(t)) = checksign({ev}, pk{ch}) in'
  emit('authority_tag'+ch,s[:a]+sub.replace(old,old.replace('=STMT_DIGEST','uncheckedAuthTag: bitstring'))+s[b:])
 # Preserve event identity = actual presented core; only verifier selection identity becomes attacker supplied.
 x=s.replace('let aid = h(core) in','in(c, aid: bitstring);',1)
 old='let StandingDecide(kT: pkey, t: bitstring, aid: bitstring, d: bitstring, terminal: bitstring) ='
 x=x.replace(old,old.replace('terminal: bitstring)','terminal: bitstring, presentedAid: bitstring)'))
 c=x.index('let StandingDecide(');d=x.index('(* Bundle:',c)
 part=x[c:d].replace('event Established(kT, t, aid)','event Established(kT, t, presentedAid)').replace('kT, t, aid);','kT, t, presentedAid);').replace('out(estCh, (kT, t, aid))','out(estCh, (kT, t, presentedAid))')
 x=x[:c]+part+x[d:]
 x=x.replace('StandingDecide(kT, t, aid, d, terminal)','StandingDecide(kT, t, aid, d, terminal, h(core))')
 emit('derived_identity',x)
