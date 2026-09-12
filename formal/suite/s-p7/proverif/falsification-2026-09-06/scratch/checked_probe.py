from pathlib import Path
s=Path('scratch/attack_dsks.pv').read_text()
s=s.replace('event AttackSent.', 'free checkedSigCh: channel [private].\nevent WrongKeyVerified.\nquery event(WrongKeyVerified).\nevent AttackSent.',1)
s=s.replace('  let (=BYTES, =fbI) = checksign(sgI, kI) in\n  let framed', '  let (=BYTES, =fbI) = checksign(sgI, kI) in\n  ( out(checkedSigCh, (ctx, kI, sgI)) |\n  let framed',1)
s=s.replace('| out(sigCh, (ctx, kI, sgI)) ).','| out(sigCh, (ctx, kI, sgI)) ) ).',1)
s=s.replace('\nprocess\n','''
let CheckedJudge =
  in(honestSigCh, (originalKey: pkey, honestSignature: bitstring));
  in(checkedSigCh, (wctx(outerKey: pkey, outerId: bitstring, outerBytes: bitstring), checkedKey: pkey, =honestSignature));
  if checkedKey <> originalKey then event WrongKeyVerified.

process
''',1)
pos=s.rfind(')');s=s[:pos]+' | !CheckedJudge '+s[pos:]
Path('scratch/attack_dsks_checked.pv').write_text(s)
