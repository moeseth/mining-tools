For AMD GPU, install

- AMDGPU Pro Driver

`https://math.dartmouth.edu/~sarunas/amdgpu.html`

- AMD APP SDK

- Add user to `video` group

---

Miners

- Claymore Dual Miner - [https://bitcointalk.org/index.php?topic=1433925.0](https://bitcointalk.org/index.php?topic=1433925.0)

- Claymore Cryptonight [https://bitcointalk.org/index.php?topic=638915.0](https://bitcointalk.org/index.php?topic=638915.0)

- PhoenixMiner [https://bitcointalk.org/index.php?topic=2647654.0](https://bitcointalk.org/index.php?topic=2647654.0)

---

Remove claymore fee based on https://github.com/gkovacs/remove_miner_fees/issues/9
--

Run `sudo python noethfee.py`

----

Tips

- Use `ngrok` for ssh tunneling

- Use windows to bio mods GPU and then install on Linux (PolarisBiosEditor, GPU-Z, AtiFlash)

### Bios Mod on window

1. Use GPU-Z to save original.rom
2. Use [PolarisBiosEditor](https://github.com/jaschaknack/PolarisBiosEditor/blob/master/notice) to patch time and clock setting
3. Use `AtiWinFlash.exe` to re-program all the cards.
4. Reboot


### Autorun on boot

1. make sure home encryption is disabled
2. set up `ether.service`


