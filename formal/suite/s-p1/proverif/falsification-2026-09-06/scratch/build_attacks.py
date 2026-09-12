from pathlib import Path
src=Path('proverif/sp1_q2_degraded_compromised.pv').read_text()
# Retain all declarations, original queries and the exact verifier, but use bounded fixed issuances.
prefix=src[:src.index('\nprocess\n')]
fixed=prefix[prefix.index('let Issuer('):prefix.index('(* Judge H')].replace('let Issuer(skI: skey, id: bitstring, m: bitstring) =\n  in(c, payload: bitstring);','let FixedIssuer(skI: skey, id: bitstring, m: bitstring, payload: bitstring) =')
prefix+='\n'+fixed
extra='''
free goodPayload: bitstring.
free alteredPayload: bitstring.
free dsksSalt: bitstring.
free issuerId3: bitstring.
free badVersion: bitstring.
free arbitrarySet: bitstring.
free targetCh: channel [private].
event Attack.
query event(Attack).
let TargetJudge =
  in(targetCh, (targetKey: pkey, targetBytes: bitstring));
  in(acceptCh, (=targetKey, =targetBytes));
  event Attack.
'''
main='''
process
  new skS: skey; new skI: skey; new skI2: skey; new skI3: skey;
  let m = authTuple(issuerId, fp(pk(skI)), ssetH, algH, verH) in
  let m2 = authTuple(issuerId2, fp(pk(skI2)), ssetH, algH, verH) in
  let m3 = authTuple(issuerId3, fp(pk(skI3)), ssetH, algH, verH) in
  let original = framed(OT_ATTEST, algH, issuerId, fp(pk(skI)), h(m), canonVerH, goodPayload) in
  let observed = sign((BYTES, original), skI) in
  let derived = dsks(observed, dsksSalt) in
  let derivedManifest = authTuple(issuerId, fp(pk(derived)), arbitrarySet, algH, verH) in
  out(c, pk(skS)); out(c, skS);
  out(c, pk(skI)); out(c, pk(skI2)); out(c, pk(skI3));
  out(c, m); out(c, m2); out(c, m3);
  ( TARGET
  | !out(honestKeyCh, pk(skI)) | !out(honestKeyCh, pk(skI2)) | !out(honestKeyCh, pk(skI3))
  | !AuthorityS(skS, m) | !AuthorityS(skS, m2) | !AuthorityS(skS, m3)
  | FixedIssuer(skI, issuerId, m, goodPayload)
  | FixedIssuer(skI2, issuerId2, m2, goodPayload)
  | FixedIssuer(skI3, issuerId3, m3, goodPayload)
  | !VerifierS(pk(skS))
  | !JudgeH | !JudgeN1 | TargetJudge )
'''
targets={
 'a1_payload_tamper':('After exactly one issuance per honest party, change payload and reuse signature.','out(targetCh, (pk(skI), framed(OT_ATTEST, algH, issuerId, fp(pk(skI)), h(m), canonVerH, alteredPayload)));'),
 'a2_party_swap':('Replay first issuer frame under third honest party key.','out(targetCh, (pk(skI3), original));'),
 'a3_dsks_replay':('DSKS-derived key verifies seen signature; try accepting its original signed frame under derived key.','out(targetCh, (pk(derived), original));'),
 'a4_dsks_resign':('After observing signature derive held key, craft arbitrary signer-set manifest and sign a new consistent altered frame.','out(targetCh, (pk(derived), framed(OT_ATTEST, algH, issuerId, fp(pk(derived)), h(derivedManifest), canonVerH, alteredPayload)));'),
 'a5_repeat_replay':('One honest issuance, same bytes accepted twice; no transaction-context check.','out(targetCh, (pk(skI), original));'),
 'a6_foreign_type':('Extra honest fixture signs OT_WRAPPER and another canonicalization version; original verifier accepts it.','out(targetCh, (pk(skI), framed(OT_WRAPPER, algH, issuerId, fp(pk(skI)), h(m), badVersion, goodPayload)));'),
}
for name,(desc,target) in targets.items():
 text=prefix+extra+main.replace('TARGET',target.rstrip(';'))
 if name=='a5_repeat_replay':
  text=text.replace('  event Attack.','  in(acceptCh, (=targetKey, =targetBytes));\n  event Attack.')
 if name=='a6_foreign_type':
  start=text.index('let FixedIssuer(');end=text.index('free goodPayload',start)
  text=text[:start]+text[start:end].replace('framed(OT_ATTEST,','framed(OT_WRAPPER,').replace('canonVerH, payload','badVersion, payload')+text[end:]
  # Declare the alternate version before its producer definition.
  text=text.replace('free badVersion: bitstring.\n','')
  text='free badVersion: bitstring.\n'+text
 Path('scratch/'+name+'.pv').write_text('(* REVIEW ATTACK: '+desc+' Baseline header is inherited; fixture changed only. *)\n'+text)
# Cross-model replay from Q1 issuer into Q2 verifier, sharing one honest key and a valid frame.
strict=Path('proverif/sp1_q1_strict_dns_compromised.pv').read_text()
issuer=strict[strict.index('let Issuer('):strict.index('(* Verifier:')].replace('let Issuer(', 'let StrictIssuer(')
text=prefix+issuer+extra+main.replace('TARGET','out(targetCh, (pk(skI), original))').replace('FixedIssuer(skI, issuerId, m, goodPayload)','StrictIssuer(skI, issuerId, m)')
Path('scratch/a7_cross_mode.pv').write_text('(* REVIEW ATTACK: Q1 issuer body copied intact (renamed) into Q2 verifier fixture; replay across modes. *)\n'+text)
# Conditional composition probe: add the supplied broken Q4 issuance endpoint under the same key.
broken=Path('proverif/sp1_q4_companionB_frame_unsigned.pv').read_text()
issuer=broken[broken.index('let Issuer('):broken.index('let JudgeH')].replace('let Issuer(', 'let PayloadOnlyIssuer(')
text=prefix+issuer+extra+main.replace('TARGET','out(targetCh, (pk(skI), framed(OT_ATTEST, algH, issuerId, fp(pk(skI)), h(m), canonVerH, alteredPayload)))').replace('| !VerifierS(pk(skS))','| PayloadOnlyIssuer(skI, issuerId, m)\n  | !VerifierS(pk(skS))')
Path('scratch/a8_cross_broken_endpoint.pv').write_text('(* CONDITIONAL COMPOSITION: correct Q2 verifier plus supplied Q4 broken issuer under same key. Not an original-fixture A1.3 break. *)\n'+text)
# Verify every attack kept the verifier byte-for-byte unchanged.
def verifier(s):
 start=s.index('let VerifierS('); end=s.index('out(acceptCh, (kX, fb)).',start)+len('out(acceptCh, (kX, fb)).')
 return s[start:end]
for p in Path('scratch').glob('a*.pv'): assert verifier(p.read_text())==verifier(src),p
print('Generated 8 attack fixtures; verifier byte-identical.')
