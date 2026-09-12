from pathlib import Path
q2=Path('proverif/sp7_q2_degraded_compromised.pv').read_text()
q1=Path('proverif/sp7_q1_strict_dns_compromised.pv').read_text()
def extend(name,src,decl,macros,branches):
 src=src.replace('(* --- model-local declarations',decl+'\n(* --- model-local declarations',1)
 src=src.replace('\nprocess\n','\n'+macros+'\nprocess\n',1)
 pos=src.rfind(')');src=src[:pos]+'\n  '+branches+' '+src[pos:]
 Path('scratch/attack_'+name+'.pv').write_text(src)
# Adversary chooses false cvInner through the existing honest Wrapper input.
extend('version_lie',q1,'event BadVersion.\nquery event(BadVersion).', '''let VersionJudge =
  in(scopeCh, (wctx(kwv: pkey, idwv: bitstring, fwv: bitstring), kiv: pkey, idiv: bitstring, fiv: bitstring));
  let framed(otv, av, iv, fv, mv, cvv, wrap(recorded: bitstring, (biv: bitstring, siv: bitstring))) = fwv in
  let framed(oti, ai, ii, fi, mi, actual, pli) = fiv in
  if recorded <> actual then event BadVersion.
''','| !VersionJudge')
# Concrete post-signature key substitution and attacker-authorized wrapper (Q2 mode).
extend('dsks',q2,'event AttackSent.\nquery event(AttackSent).', '''let DSKSDriver(knownIssuer: pkey, compromised: skey) =
  in(c, seen: bitstring);
  let (=BYTES, bytes: bitstring) = checksign(seen, knownIssuer) in
  new salt: bitstring;
  let derived = dsks(seen, salt) in
  let forgedManifest = authTuple(idA, fp(pk(derived)), ssetH, algH, verH) in
  let evidence = sign((STMT_DIGEST, h(forgedManifest)), compromised) in
  let possession = sign((POSS, forgedManifest), derived) in
  let outer = framed(OT_WRAPPER, algH, idA, fp(pk(derived)), h(forgedManifest), cvB, wrap(cvA, (bytes, seen))) in
  event AttackSent;
  out(c, (forgedManifest, evidence, pk(derived), possession, sign((BYTES, outer), derived), outer,
          forgedManifest, evidence, pk(derived), possession)).
''','| !DSKSDriver(pk(skI1), skS)')
# Honest issuer exercises all declared framed types under its existing certified key.
extend('extra_types',q1,'','', '| !OtherSigner(skI2, issuerId2, mI2, OT_MANIFEST, cvB)\n  | !OtherSigner(skI2, issuerId2, mI2, OT_AUTHEVID, cvB)\n  | !OtherSigner(skI2, issuerId2, mI2, OT_CONFVEC, cvB)\n  | !OtherSigner(skI2, issuerId2, mI2, OT_TLR, cvB)\n  | !OtherSigner(skI2, issuerId2, mI2, OT_REFUSAL, cvB)')
# Q4-shaped honest attestation shares Q1 keys/manifests, type vocabulary and judges.
extend('cross_model',q1,'fun canon(bitstring, bitstring): bitstring [data].\nevent CrossAccepted.\nquery event(CrossAccepted).', '''let Q4Signer(skX: skey, mx: bitstring) =
  in(c, chosen: bitstring);
  let bx = canon(cvA, framed(OT_ATTEST, algH, issuerId, fp(pk(skX)), h(mx), cvA, chosen)) in
  let sx = sign((BYTES, bx), skX) in
  (out(c, sx) | out(c, sign((POSS, mx), skX)) | out(honestTypeCh, (OT_ATTEST, bx))
   | out(honestCh, (pk(skX), bx)) | out(honestInnerCh, (pk(skX), issuerId, bx)) | out(honestSigCh, (pk(skX), sx))).
let CrossJudge =
  in(acceptCh, (cx: bitstring, kx: pkey, ix: bitstring, canon(vx: bitstring, bx: bitstring)));
  event CrossAccepted.
''','| !Q4Signer(skI1, mI1) | !CrossJudge')
# Extra honest identity with the same certified signing key, two signed manifests.
extend('alias_issuer',q1,'free aliasId: bitstring.','', '''| let aliasManifest = authTuple(aliasId, fp(pk(skI1)), ssetH, algH, verH) in
    (!AuthorityD(skD, aliasManifest) | !AuthorityR(skR, aliasManifest)
     | out(c, aliasManifest) | !Attester(skI1, aliasId, aliasManifest, cvB))''')
# Test altering embedded bytes to a hash, keeping a genuine inner signature.
extend('hash_only',q1,'event HashOnlyAccepted.\nquery event(HashOnlyAccepted).', '''let HashJudge =
  in(scopeCh, (wctx(kwx: pkey, idx: bitstring, fwx: bitstring), kix: pkey, idix: bitstring, h(original: bitstring)));
  event HashOnlyAccepted.
let HashDriver(knownIssuer: pkey) =
  in(c, seen: bitstring);
  let (=BYTES, bytes: bitstring) = checksign(seen, knownIssuer) in
  out(c, (cvA, h(bytes), seen)).
''','| !HashDriver(pk(skI1)) | !HashJudge')
