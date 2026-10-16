"""Write synthetic public test inputs below this instrument, never real evidence."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'tests'))
from fixtures import make_fixture
from codec import jcs

def main():
    directory=Path(__file__).resolve().parent/'examples'; directory.mkdir(exist_ok=True)
    bundle,trust,catalog=make_fixture()
    for name,obj in [('bundle',bundle),('trust',trust),('catalog',catalog)]:
        (directory/(name+'.json')).write_bytes(jcs(obj))
    print('Synthetic inputs written; headers/pins are fabricated, not Bitcoin history.')
if __name__=='__main__': main()
