# Alwan - Colorbot Research Project

> **Alwan** (ألوان) means "colors" in Arabic

A fork of [Unibot](https://github.com/vike256/Unibot) for educational research on color-based aim assistance in games and potential countermeasures.

---

## Disclaimer

**This project is for educational and research purposes only.**

- Do NOT use this in online multiplayer games
- Using cheats violates Terms of Service and can result in bans
- This research aims to help game developers understand and counter color-based exploits

---

## Documentation

| Document | Description |
|----------|-------------|
| [Installation Guide](../docs/INSTALLATION.md) | Setup, dependencies, platform compatibility |
| [Usage Guide](../docs/USAGE.md) | Configuration, controls, tuning parameters |
| [Countermeasures](../docs/COUNTERMEASURES.md) | Defense strategies, platform security comparison |
| [Technical Analysis](../docs/TECHNICAL.md) | How it works, detection methods, code deep dive |
| [Detection Guide](../docs/DETECTION_GUIDE.md) | Visual indicators for identifying colorbot users |

---

## Quick Start

```powershell
# Install dependencies
pip install -r requirements.txt

# Run (Windows only)
cd src
python main.py
```

**Controls:** F2 = Toggle aim | Right-click = Activate | F4 = Exit

See [Usage Guide](../docs/USAGE.md) for configuration details.

---

## What is a Colorbot?

A colorbot is aim assistance software that:

1. Captures a region of the screen around the crosshair
2. Detects specific colors (e.g., enemy outlines/highlights)
3. Calculates the offset from crosshair to target
4. Moves the mouse to aim at the detected color

Unlike memory-based cheats, colorbots don't read game memory, making them harder to detect through traditional anti-cheat methods.

### Research Results

| Metric | Without Colorbot | With Colorbot |
|--------|------------------|---------------|
| Headshot Accuracy | ~20% | 50-70% |
| Test Conditions | 800 DPI, 0.5 in-game sensitivity | Same settings |

---

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Screen Capture │────▶│  Color Detection │────▶│  Mouse Movement │
│   (bettercam)   │     │    (OpenCV)      │     │  (Interception) │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

**Smoothing formula:** `movement = (target_offset / smoothing) * speed`

See [Technical Analysis](../docs/TECHNICAL.md) for implementation details.

---

## Platform Compatibility

| Platform | Status | Notes |
|----------|--------|-------|
| Windows | ✅ Supported | Full functionality |
| Linux X11 | ❌ Not supported | Similar vulnerabilities exist |
| Linux Wayland | ❌ Not supported | Inherently protected by design |

See [Countermeasures](../docs/COUNTERMEASURES.md#platform-security-comparison) for detailed platform security analysis.

---

## For Game Developers

Key countermeasures against colorbots:

1. **Dynamic colors** - Randomize enemy highlight colors
2. **Color noise** - Add per-pixel variation to outlines
3. **Server-side detection** - Analyze reaction times and movement patterns
4. **Support Wayland** - Eliminates the attack vector on Linux

Full details in [Countermeasures](../docs/COUNTERMEASURES.md).

---

## Project Structure

```
Alwan/
├── src/
│   ├── main.py              # Entry point
│   ├── unibot.py            # Main loop (Alwan class)
│   ├── screen.py            # Screen capture & color detection
│   ├── cheats.py            # Aim calculation
│   ├── configReader.py      # Configuration parser
│   ├── utils.py             # Key bindings
│   └── mouse/               # Input implementations
├── docs/
│   ├── INSTALLATION.md      # Setup guide
│   ├── USAGE.md             # Usage guide
│   ├── COUNTERMEASURES.md   # Defense strategies
│   ├── TECHNICAL.md         # Technical deep dive
│   └── DETECTION_GUIDE.md   # Visual detection indicators
├── config.ini               # Configuration
└── requirements.txt         # Dependencies
```

---

## License

GNU General Public License v3.0

```
Alwan (fork of Unibot), a colorbot research project.
Original Copyright (C) 2025 vike256
```

---

## Contributing

Contributions focused on **countermeasure development**, **detection methods**, and **educational documentation** are welcome.

**Do NOT submit:**
- Anti-cheat evasion improvements
- New cheating features
- Commercial game targeting

---

## Acknowledgments

- **vike256** - Original Unibot creator
- **oblitum** - Interception driver
- **UCA** - Smoothing algorithm reference

---

## References

- [Unibot](https://github.com/vike256/Unibot) - Original implementation
- [Interception Driver](https://github.com/oblitum/Interception) - Input injection
- [BetterCam](https://github.com/RootKit-Org/BetterCam) - Screen capture
- [OpenCV](https://opencv.org/) - Computer vision
