# Fleasion mocktail port

> [!IMPORTANT]
> Roblox has patched [official Fleasion](https://github.com/fleasion/Fleasion) and it currently does not work. There is **no ETA** for a fix.

Fleasion replaces Roblox game assets in real time. It runs a local HTTPS proxy between Roblox and its servers so textures, audio, meshes, animations, and other assets can be swapped before reaching the client.

**Platforms:** Windows, macOS, Linux (Sober Flatpak and Mocktail native).

## Installation

To run from source:

```bash
uv run fleasion
```

## Usage

1. Launch Fleasion.
2. Add replacements in the Replacer tab.
3. Clear the cache (tray → Delete Cache) so Roblox re-downloads assets through the proxy.
4. Launch Roblox. Its traffic goes through the proxy.

## Linux clients

Fleasion supports two Linux Roblox clients:

- **Sober** — Flatpak (`org.vinegarhq.Sober`)
- **Mocktail** — native (`space.bigrat.mocktail`)

Select your client in Settings → Linux client (`auto`, `sober`, or `mocktail`).

## Development

All commands run through `uv` from the repo root:

```bash
uv run fleasion        # run the app
uv run pytest          # run the test suite
uv run ruff check .    # lint
uv run ruff format .   # format
uv run pyright         # type check
uv run build           # build standalone release
```

## Community

- Discord: https://discord.gg/hXyhKehEZF
- Website: https://fleasion.github.io/
- Download the latest official build from [Fleasion's official page](https://github.com/fleasion/Fleasion/releases). Python is not required.

This project is provided as is for educational and personal use.

**I HAVE NOT VERIFIED SUPPORT FOR THIS VERSION OF FLEASION TO WORK WITH WINDOWS OR MACOS THIS IS MAINLY A PORT TO MOCKTAIL FOR LINUX**
Tested on: Arch Linux "mocktail" AUR package 

