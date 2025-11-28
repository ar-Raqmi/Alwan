# Countermeasures for Game Developers

This document provides research on how to defend against color-based aim assistance.

---

## Table of Contents

1. [Color-Based Countermeasures](#color-based-countermeasures)
2. [Detection Methods](#detection-methods)
3. [Technical Countermeasures](#technical-countermeasures)
4. [Platform Security Comparison](#platform-security-comparison)
5. [Linux-Specific Information](#linux-specific-information)

---

## Color-Based Countermeasures

### 1. Dynamic Enemy Colors

- **Randomize outline colors** per match or per player
- **Gradient/animated outlines** that shift hue over time
- **Team-based color schemes** that change each round

### 2. Color Disruption Techniques

- **Flashing/pulsing highlights** - rapid color changes break detection
- **Noise injection** - add subtle color noise to outlines
- **Adaptive colors** - match outline color to background

### 3. Visual Obfuscation

- **Particle effects** around enemies that share similar colors
- **Decoy colors** - environmental objects with enemy-like colors
- **Color bleeding** - gradual color transitions instead of solid outlines

---

## Detection Methods

### 1. Input Pattern Analysis

Colorbots produce detectable patterns:

- **Perfectly smooth curves** - no human jitter
- **Consistent reaction times** - 50-100ms vs human 150-400ms
- **Fixed vertical aim ratio** - always hits same hitbox percentage
- **No prediction** - always slightly behind moving targets

### 2. Timing Analysis

```
Human reaction time distribution:
├── Mean: 200-300ms
├── Variance: High (±100ms)
└── Shape: Right-skewed

Colorbot reaction time distribution:
├── Mean: 50-100ms
├── Variance: Low (±20ms)
└── Shape: Gaussian (tight cluster)
```

### 3. Screen Capture Detection

- Detect DXGI/GDI capture hooks in process
- Monitor for suspicious DirectX calls
- Check for known capture library signatures

### 4. Movement Trajectory Analysis

Colorbots produce unnaturally smooth curves due to mathematical smoothing:

```
movement = (target_offset / smoothing) * speed
```

This creates exponential decay curves that humans can't replicate consistently.

---

## Technical Countermeasures

### 1. Variable Render Timing

Randomize when enemy highlights are drawn to desync with capture timing.

### 2. Per-Pixel Color Variation

No two pixels should be exactly the same color:

```python
# Add subtle noise to each pixel
def add_color_noise(color, variance=3):
    return color + random.randint(-variance, variance)
```

### 3. HDR Color Spaces

Use colors outside standard 8-bit detection ranges. Most colorbots assume sRGB.

### 4. Shader-Based Effects

Complex visual effects are harder to isolate:
- Bloom effects
- Chromatic aberration on outlines
- Animated distortion

---

## Platform Security Comparison

Understanding platform vulnerabilities helps prioritize countermeasures.

### Screen Capture Vulnerability by Platform

| Platform | Capture Method | Difficulty | Native Protection |
|----------|---------------|------------|-------------------|
| **Windows** | DXGI/GDI | Easy | None - any app can capture |
| **Linux X11** | XShm/XGetImage | Easy | None - X11 has no isolation |
| **Linux Wayland** | Restricted | Hard | Built-in app isolation |

### Windows (Most Vulnerable)

- **DXGI Desktop Duplication**: Any process can capture the entire screen
- **No permission system**: Applications don't need consent to capture
- **Driver-level input**: Interception driver mimics hardware perfectly
- **Why vulnerable**: Windows prioritizes compatibility over security

```
Colorbot Attack Surface (Windows):
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ DXGI Capture │───▶│ OpenCV/HSV   │───▶│ Interception │
│ (No auth)    │    │ Processing   │    │ Driver Input │
└──────────────┘    └──────────────┘    └──────────────┘
      ⚠️                  ✓                   ⚠️
   Unrestricted      Cross-platform      Kernel-level
```

### Linux X11 (Equally Vulnerable)

- **XShm/XGetImage**: Direct framebuffer access, no restrictions
- **No window isolation**: Any X client can read any window content
- **Input injection**: `xdotool` or `libevdev` for mouse control
- **Why vulnerable**: X11 was designed in 1984 without security model

### Linux Wayland (Most Secure)

- **Compositor-controlled capture**: Apps cannot capture other windows
- **Portal API required**: Screen capture needs explicit user permission
- **Per-window isolation**: Each app only sees its own content
- **Input restrictions**: Cannot inject input to other windows

```
Colorbot Attack Surface (Wayland):
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Portal API   │───▶│ OpenCV/HSV   │───▶│ libei/uinput │
│ (User auth)  │    │ Processing   │    │ (Restricted) │
└──────────────┘    └──────────────┘    └──────────────┘
      ✓                   ✓                   ✓
  Permission         Cross-platform      Needs root/
   Required                               special caps
```

**Wayland Protections:**
- `xdg-desktop-portal` requires user to select window/screen to share
- Portal shows visible indicator when screen is being captured
- `libei` (emulated input) requires compositor permission
- Games can detect if running under capture via portal hints

### Countermeasure Recommendations by Platform

**For Windows Games:**
1. Detect DXGI hooks in your process
2. Use anti-cheat that monitors for Interception driver
3. Implement all color-based countermeasures (randomization, noise)
4. Server-side behavioral detection is most reliable

**For Linux X11 Games:**
1. Same vulnerabilities as Windows - implement all countermeasures
2. Consider requiring Wayland for competitive modes
3. Detect `xdotool` or `evdev` injection patterns
4. Monitor for XShm connections to your window

**For Linux Wayland Games:**
1. **Inherently protected** - colorbot cannot capture without user consent
2. User must explicitly grant screen share (visible indicator)
3. Focus on server-side detection for edge cases
4. Can query compositor for active screen share sessions

### Migration Recommendation for Game Developers

| Priority | Action | Impact |
|----------|--------|--------|
| High | Support Wayland natively | Eliminates colorbot attack vector |
| Medium | Detect X11 fallback | Warn users or restrict features |
| Low | Implement XWayland detection | Partial protection (XWayland has X11 vulnerabilities) |

---

## Linux-Specific Information

### Why Alwan Doesn't Support Linux

This project is Windows-only intentionally:

1. **Research focus**: Windows is where colorbots are most prevalent
2. **Wayland protection**: Modern Linux desktops block the attack vector by design
3. **X11 deprecation**: Most distros now default to Wayland

### Linux Equivalent Methods (For Research Understanding)

If a colorbot were to target Linux X11, it would use:

| Windows Component | Linux X11 Equivalent | Library |
|-------------------|---------------------|---------|
| DXGI Capture | XShm/XGetImage | `python-xlib`, `mss` |
| Interception Driver | evdev/uinput | `python-evdev` |
| win32api keys | X11 key events | `pynput`, `python-xlib` |

**Example X11 screen capture (research reference only):**
```python
# This demonstrates the X11 vulnerability - NOT functional cheat code
from mss import mss
with mss() as sct:
    # Any X11 app can capture any window - no permission needed
    img = sct.grab({"top": 0, "left": 0, "width": 256, "height": 256})
```

### Wayland Security Model

Wayland's architecture prevents colorbot attacks:

```
┌─────────────────────────────────────────────────────────┐
│                    Wayland Compositor                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Game      │  │  Colorbot   │  │   Other     │     │
│  │  (Window)   │  │  (Window)   │  │   (Window)  │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│        │                ╳                │              │
│        │         Cannot access          │              │
│        └────────────────────────────────┘              │
│                    Isolated                             │
└─────────────────────────────────────────────────────────┘
```

Each application:
- Can only see its own window content
- Cannot inject input to other windows
- Must request screen capture through Portal API (user approval required)

### Detecting Display Server (For Game Developers)

```python
import os

def get_display_server():
    if os.environ.get('WAYLAND_DISPLAY'):
        return 'wayland'  # Secure
    elif os.environ.get('DISPLAY'):
        return 'x11'  # Vulnerable
    return 'unknown'

# In game launcher:
if get_display_server() == 'x11':
    print("Warning: X11 detected. For better security, use Wayland.")
```

---

## Summary

### Most Effective Countermeasures

1. **Eliminate color highlighting** - Makes colorbots 100% ineffective
2. **Dynamic color shifting** - Breaks fixed HSV detection ranges
3. **Server-side behavioral analysis** - Catches all aim assistance variants
4. **Support Wayland natively** - Platform-level protection on Linux

### Detection Priority

| Method | Effectiveness | False Positive Risk |
|--------|--------------|---------------------|
| Reaction time analysis | High | Low |
| Movement curve analysis | High | Medium |
| Screen capture detection | Medium | Low |
| Driver signature detection | Medium | Low |
| Accuracy pattern analysis | High | Medium |
