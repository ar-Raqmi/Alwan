# Usage Guide

## Quick Start

```powershell
cd src
python main.py
```

## Configuration

### 1. Configure Color Detection

Edit `config.ini` to match your target color:

```ini
[screen]
; HSV color range (Hue: 0-179, Saturation: 0-255, Value: 0-255)
upper_color = 155, 255, 255
lower_color = 140, 178, 242
```

### 2. Debug Mode (Color Tuning)

Use debug mode to visualize what the bot sees:

```ini
[debug]
enabled = true
display_mode = mask   ; 'mask' shows detection, 'game' shows actual screen
always_on = false
```

## Controls

| Key | Function |
|-----|----------|
| F1 | Reload config |
| F2 | Toggle aim assist |
| F3 | Toggle recoil control |
| F4 | Exit program |
| Right-click (hold) | Activate aim assist |
| Mouse5 | Rapid fire |

## Tuning Parameters

### Aim Settings

| Parameter | Effect | Recommended Range |
|-----------|--------|-------------------|
| `aim_smoothing_factor` | Higher = smoother, slower | 5-15 |
| `speed` | Movement multiplier | 2.0-7.0 |
| `y_speed_multiplier` | Vertical sensitivity ratio | 0.7-1.0 |
| `aim_height` | Vertical aim point (0=bottom, 1=top) | 0.8-1.0 |

### Screen Settings

| Parameter | Effect | Recommended Range |
|-----------|--------|-------------------|
| `capture_fov_x/y` | Detection area size (pixels) | 128-512 |
| `aim_fov_x/y` | Aim activation zone | 128-512 |
| `max_loops_per_sec` | Update rate | 120-500 |

### Color Detection

| Parameter | Effect |
|-----------|--------|
| `upper_color` | HSV upper bound (H, S, V) |
| `lower_color` | HSV lower bound (H, S, V) |
| `group_close_target_blobs_threshold` | Blob grouping kernel size |

## Input Methods

Configure in `config.ini`:

```ini
[aim]
bot_input_type = interception_driver  ; Recommended
; Other options:
; winapi                    - Windows API (easier to detect)
; microcontroller_serial    - External hardware via serial
; microcontroller_socket    - External hardware via network
```

### Interception Driver (Recommended)

- Kernel-level input injection
- Mimics real hardware
- Requires driver installation

### WinAPI

- No driver needed
- Easier for anti-cheat to detect
- Good for testing

### Microcontroller

For external hardware (Arduino, etc.):

```ini
[communication]
; For serial connection
com_port = 1

; For socket connection
microcontroller_ip = 0.0.0.0
microcontroller_port = 50256
```

## Example Configurations

### Snappy (Low Smooth)

```ini
[aim]
aim_smoothing_factor = 3
speed = 5.0
```

### Smooth Tracking (High Smooth)

```ini
[aim]
aim_smoothing_factor = 12
speed = 7.0
```

### Large FOV Detection

```ini
[screen]
capture_fov_x = 512
capture_fov_y = 512
aim_fov_x = 400
aim_fov_y = 400
```

## Troubleshooting

### "No target detected"

1. Enable debug mode with `display_mode = mask`
2. Check if target color appears white in mask view
3. Adjust HSV range to capture target color

### "Movement too fast/slow"

1. Adjust `speed` multiplier
2. Match to your in-game sensitivity
3. Higher `aim_smoothing_factor` = slower movement

### "Bouncy/oscillating aim"

1. Increase `aim_smoothing_factor` (try 10-15)
2. Decrease `speed` multiplier
3. Check `y_speed_multiplier` isn't too high

### "Low frame rate"

1. Disable debug mode: `enabled = false`
2. Reduce `capture_fov_x/y` size
3. Lower `max_loops_per_sec` if CPU limited
