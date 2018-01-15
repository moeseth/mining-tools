For AMD GPU, install

- AMDGPU Pro Driver

`https://math.dartmouth.edu/~sarunas/amdgpu.html`

- AMD APP SDK

- Add user to `video` group

---

Miners

- [https://github.com/nanopool/Claymore-Dual-Miner](https://github.com/nanopool/Claymore-Dual-Miner)

- [https://github.com/nanopool/Claymore-XMR-Miner/releases](https://github.com/nanopool/Claymore-XMR-Miner/releases)

---

Remove claymore fee based on https://github.com/gkovacs/remove_miner_fees/issues/9

#### Change `port` in `remove_ether_devfee.py` if required

--

Run `sudo python remove_ether_devfee.py`

----

Tips

- Use `ngrok` for ssh tunneling

- Use windows to bio mods GPU and then install on Linux (PolarisBiosEditor, GPU-Z, AtiFlash)

### Bios Mod on window

1. Use GPU-Z to save original.rom
2. Use [PolarisBiosEditor](https://github.com/jaschaknack/PolarisBiosEditor/blob/master/notice) to patch time and clock setting
3. Use `AtiWinFlash.exe` to re-program all the cards.
4. Reboot



