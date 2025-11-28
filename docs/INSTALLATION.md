# Installation Guide

## Prerequisites

- Python 3.10+
- Windows 10/11
- [Interception Driver](https://github.com/oblitum/Interception) (for mouse input)

## Dependencies

```bash
pip install -r requirements.txt
```

### Required Packages

| Package | Version | Purpose |
|---------|---------|---------|
| `bettercam` | 1.0.0 | Fast DXGI screen capture |
| `opencv-python` | 4.10.0.84 | Image processing & color detection |
| `numpy` | >=2.1.0 | Numerical operations |
| `interception-python` | 1.12.4 | Low-level mouse input |
| `pywin32` | 308 | Windows API access |
| `pyautogui` | 0.9.54 | Screen resolution detection |
| `pyserial` | 3.5 | Serial communication (optional) |

## Interception Driver Setup

1. Download [Interception](https://github.com/oblitum/Interception/releases)
2. Run as Administrator:
   ```cmd
   install-interception.exe /install
   ```
3. **Restart your computer**

## Platform Compatibility

### Windows (Supported)

This project runs on Windows only due to platform-specific dependencies:

| Component | Windows Library | Why Windows-Only |
|-----------|----------------|------------------|
| Screen Capture | `bettercam` (DXGI) | DirectX is Windows-exclusive |
| Mouse Input | `interception-python` | Kernel driver for Windows |
| Key Detection | `pywin32` | Windows API |

### Linux (Not Supported)

The current implementation does not support Linux. See [COUNTERMEASURES.md](COUNTERMEASURES.md#platform-security-comparison) for:
- Why Linux X11 has similar vulnerabilities
- Why Linux Wayland is inherently protected
- What Linux equivalents would be (for research understanding)

### Why No Linux Support?

This is intentional for research purposes:
1. **Wayland blocks colorbots by design** - no need to test countermeasures
2. **X11 is being phased out** - most distros default to Wayland now
3. **Focus on Windows** - where colorbots are most prevalent

If you're a game developer testing countermeasures on Linux, the documentation in [COUNTERMEASURES.md](COUNTERMEASURES.md) explains the attack vectors without providing functional code.

## Verification

After installation, verify everything works:

```powershell
cd src
python -c "import bettercam; import cv2; import interception; print('All dependencies OK')"
```

If you get import errors, ensure:
1. Python 3.10+ is installed
2. `pip install -r requirements.txt` completed successfully
3. Interception driver is installed and system was restarted
