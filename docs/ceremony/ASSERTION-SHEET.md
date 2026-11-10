# Signing the key assertion — operator sheet (one short sitting)

YubiKey A signs one git commit that names the window's two service keys and dates. The NUC built the commit; the
script shows it to you, checks it, and signs only if you type `yes`.

Sticks: **INPUT** and **OUT**, both never in the NUC (the reformatted purple rehearsal sticks will do).
**[PHOTO]** = photograph the screen. Nothing secret appears on screen except the PIN prompt.

## 1. Fetch (a networked Tails boot)

The owner names a commit and three SHA-256 values: `sign-assertion.sh`, `payload.txt` and `root.pub.asc`.
```
git clone https://github.com/fsgeek/tessera.git
```
```
cd tessera
```
```
git checkout <the commit>
```
```
sha256sum docs/ceremony/sign-assertion.sh docs/ceremony/assertion/payload.txt docs/ceremony/assertion/root.pub.asc
```
All three must equal the owner's values. Format INPUT (FAT, volume name `INPUT`), open it in *Files*, then:
```
cp docs/ceremony/sign-assertion.sh docs/ceremony/assertion/payload.txt docs/ceremony/assertion/root.pub.asc /media/amnesia/INPUT/
```
Eject; shut down.

## 2. Sign (an offline Tails boot)

Network off. Insert INPUT and OUT (format OUT: FAT, volume name `OUT`); open both in *Files*. Not YubiKey A yet.
```
cp /media/amnesia/INPUT/sign-assertion.sh /tmp/s.sh
```
```
sha256sum /tmp/s.sh
```
Same as the owner's value. Read it (`less /tmp/s.sh`). Then:
```
bash /tmp/s.sh
```
**[PHOTO]** the commit text and the `MATCH` line. Read the text: `kms=a33c216e…`, `gpg=6a2d7e75…`, and the two
dates the owner gave you. If they are right, type `yes`, insert YubiKey A when asked, enter the PIN, touch when it
blinks. Want `==> PASS`. **[PHOTO]**. Eject both sticks, remove YubiKey A, shut down. OUT goes to the owner.

If anything fails: nothing has been signed or changed on the card. Photograph it and stop.
