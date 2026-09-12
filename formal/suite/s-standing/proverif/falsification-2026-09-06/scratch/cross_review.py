from pathlib import Path
s=Path('proverif/ss_q1_strict_dns_compromised.pv').read_text()
# A bounded extra honest protocol role emits a REFUSAL-tagged object with TLR-shaped body.
# The chosen body deliberately maximizes replay compatibility; no claim about an absent family.
role='''let ForeignIssuer(skI:skey) =
  in(c, foreignCore:bitstring);
  let body = (lineage2(entry(h(foreignCore),DISP_SHIPPED),entry(fbH,DISP_ABANDONED)),TERM_SHIPPED(h(foreignCore)),fbH) in
  out(c,sign((REFUSAL,body),skI)).

'''
x=s.replace('process\n',role+'process\n',1).replace('| !Judge | !ReasonJudge','| !ForeignIssuer(skH1) | !Judge | !ReasonJudge')
x=x.replace('(* --- authority channels','query t:bitstring; event(Established(pk(skH1),t,h(fbH))).\n\n(* --- authority channels',1)
Path('scratch/a_foreign_tag.pv').write_text('(* REVIEW ATTACK: added honest foreign-tag signing role; verifier unchanged. *)\n'+x)
# Isolate cross-family domain tag dependence under that same fixture extension.
start=x.index('let StandingPath(');end=x.index('(* --- the envelope path',start)
y=x[:start]+x[start:end].replace('let (=TLR,','let (uncheckedTag: bitstring,',1)+x[end:]
Path('scratch/m_foreign_tlr_tag.pv').write_text('(* REVIEW MUTANT of a_foreign_tag: only standing TLR tag unbound. *)\n'+y)
for mode,name in {'dns':'ss_q1_strict_dns_compromised','repo':'ss_q1_strict_repo_compromised','deg':'ss_q1d_degraded_compromised'}.items():
 x=Path('proverif',name+'.pv').read_text();start=x.index('let StandingDecide(');end=x.index('(* Bundle:',start)
 role='''let StandingDecide(kT:pkey,t:bitstring,aid:bitstring,d:bitstring,terminal:bitstring) =
  if d = DISP_SHIPPED then
    ( event Established(kT,t,aid);
      event StandingReport(ESTABLISHED,TERMINAL_DISPOSITION_SHOWN,kT,t,aid);
      out(estCh,(kT,t,aid)) )
  else event StandingReport(UNVERIFIABLE,STANDING_EVIDENCE_MALFORMED,kT,t,aid).

'''
 Path('scratch',f'm_{mode}_terminal_predicate.pv').write_text('(* REVIEW MUTANT: all terminal decisions removed; entry disposition check preserved. *)\n'+x[:start]+role+x[end:])
