from pathlib import Path
import re,json
fixed=[]
for out in Path('scratch').glob('q*.out'):
 if 'should be declared with a type' in out.read_text():
  p=out.with_suffix('.pv');s=p.read_text()
  s=re.sub(r'\b(unused(?:Tag|Digest|Manifest|Bytes))\b',r'\1: bitstring',s)
  dest=p.with_name(p.stem+'_typed.pv');dest.write_text(s);fixed.append(str(dest))
p=Path('scratch/attack_hash_only.pv');s=p.read_text()
s=s.replace('event HashOnlyAccepted.','free hashTarget: channel [private].\nevent HashOnlyAccepted.',1)
s=s.replace('  in(scopeCh, (wctx(kwx: pkey, idx: bitstring, fwx: bitstring), kix: pkey, idix: bitstring, h(original: bitstring)));','  in(hashTarget, target: bitstring);\n  in(scopeCh, (wctx(kwx: pkey, idx: bitstring, fwx: bitstring), kix: pkey, idix: bitstring, =target));')
s=s.replace('  out(c, (cvA, h(bytes), seen)).','  (out(hashTarget, h(bytes)) | out(c, (cvA, h(bytes), seen))).')
dest=p.with_name('attack_hash_only_fixed.pv');dest.write_text(s);fixed.append(str(dest))
Path('scratch/fixed_files.json').write_text(json.dumps(fixed))
print(len(fixed))
