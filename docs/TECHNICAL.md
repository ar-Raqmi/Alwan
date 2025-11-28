# Technical Analysis

Deep dive into how the colorbot works and why.

---

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Screen Capture │────▶│  Color Detection │────▶│  Mouse Movement │
│   (bettercam)   │     │    (OpenCV)      │     │  (Interception) │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
   DXGI capture           HSV filtering            Driver-level
   256x256 region         Contour finding          input injection
```

---

## Processing Pipeline

### 1. Screen Capture

DXGI grab of configurable region around crosshair:

```python
# bettercam uses DirectX Desktop Duplication API
self.cam = bettercam.create(output_color="BGR")
image = self.cam.grab(region)  # Returns numpy array
```

**Performance**: ~1-2ms per capture at 256x256

### 2. Color Space Conversion

BGR to HSV for better color isolation:

```python
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
```

**Why HSV?**
- Hue = color type (independent of lighting)
- Saturation = color intensity
- Value = brightness

This separates "what color" from "how bright", making detection more robust.

### 3. Mask Creation

Binary mask isolating target color:

```python
mask = cv2.inRange(hsv, lower_color, upper_color)
# Result: white (255) where color matches, black (0) elsewhere
```

**HSV Range Example** (purple/magenta):
```ini
upper_color = 155, 255, 255  ; H=155, S=255, V=255
lower_color = 140, 178, 242  ; H=140, S=178, V=242
```

### 4. Morphological Operations

Dilation groups nearby pixels into blobs:

```python
kernel = np.ones((12, 12), np.uint8)
dilated = cv2.dilate(mask, kernel, iterations=1)
```

**Purpose**: Merge fragmented detections into single targets

### 5. Contour Detection

Find target outlines:

```python
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
```

### 6. Target Selection

Choose closest target to crosshair center:

```python
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    center_x = x + w // 2
    center_y = y + h * (1 - aim_height)  # Configurable vertical aim point

    distance = sqrt((center_x - fov_center_x)**2 + (center_y - fov_center_y)**2)
    if distance < min_distance:
        target = (center_x - fov_center_x, center_y - fov_center_y)
```

### 7. Movement Calculation

UCA-style smoothing formula:

```python
move_x = (target_x / smoothing) * speed
move_y = (target_y / smoothing) * speed * y_multiplier
```

**Parameters**:
- `smoothing = 12` → Divide movement across frames
- `speed = 7.0` → Compensate for in-game sensitivity
- `y_multiplier = 0.8` → Vertical sensitivity ratio

### 8. Input Injection

Send mouse delta via Interception driver:

```python
interception.move_relative(move_x, move_y)
```

**Why Interception?**
- Kernel-level driver
- Mimics real hardware input
- Bypasses user-space input hooks

---

## Smoothing Algorithm

### The Formula

```
movement = (target_offset / smoothing) * speed
```

### How It Works

Each frame moves a fraction of the remaining distance:

```
Frame 1: target=100px, smooth=10, speed=5 → move 50px (100/10*5)
Frame 2: target=50px,  smooth=10, speed=5 → move 25px
Frame 3: target=25px,  smooth=10, speed=5 → move 12.5px
...converges to target
```

This creates an **exponential decay curve** - fast initial movement, slowing as it approaches target.

### Sub-Pixel Precision

Mouse APIs accept integers, but calculations produce floats:

```python
def calculate_move_amount(self, move_x, move_y):
    move_x += self.remainder_x  # Add previous remainder
    move_y += self.remainder_y

    int_x = round(move_x)  # Round to nearest integer
    int_y = round(move_y)

    self.remainder_x = move_x - int_x  # Store fractional part
    self.remainder_y = move_y - int_y

    return (int_x, int_y)
```

This accumulates sub-pixel movement across frames for perfect targeting.

---

## Why Colorbots Are Effective

### 1. No Memory Access

- Doesn't touch game memory
- Bypasses memory-based anti-cheat
- Works on any game with color highlights

### 2. External Operation

- Runs as separate process
- No DLL injection
- Harder to detect from within game

### 3. Driver-Level Input

- Interception mimics real mouse hardware
- Input appears to come from physical device
- Bypasses user-space input monitoring

### 4. Mathematical Precision

- Sub-pixel accuracy over time
- Consistent smoothing curves
- No human jitter or hesitation

---

## Why Colorbots Are Detectable

### 1. Unnatural Movement Patterns

**Human mouse movement:**
- Variable speed (acceleration/deceleration)
- Micro-corrections and overshoots
- Jitter and noise

**Colorbot movement:**
- Perfect exponential curves
- No overshoots (converges mathematically)
- Unnaturally smooth

### 2. Reaction Time Signatures

**Human:**
- 150-400ms reaction time
- High variance
- Affected by fatigue, attention

**Colorbot:**
- 50-100ms (capture + process + send)
- Low variance
- Consistent regardless of conditions

### 3. Aim Placement Distribution

**Human:**
- Variable vertical aim (head, chest, legs)
- Affected by distance, movement, panic
- ~20-40% headshots naturally

**Colorbot:**
- Fixed `aim_height` ratio (e.g., 0.8 = upper chest)
- Always hits same vertical percentage
- Statistically detectable clustering

### 4. Screen Capture Detection

- DXGI hooks can be detected
- Capture timing patterns are recognizable
- Known library signatures (bettercam, etc.)

### 5. Driver Signatures

- Interception driver has known fingerprint
- Can be blacklisted by anti-cheat
- Registry/driver enumeration reveals presence

---

## Performance Characteristics

### Timing Breakdown

| Stage | Time |
|-------|------|
| Screen capture | 1-2ms |
| HSV conversion | 0.5ms |
| Mask + dilation | 0.5-1ms |
| Contour finding | 0.2ms |
| Target selection | 0.1ms |
| Mouse send | 0.1ms |
| **Total** | **~3-5ms** |

### Achievable Loop Rate

- Without debug: 200-300 Hz
- With debug window: 60-120 Hz
- Bottleneck: Screen capture and dilation

### Latency Analysis

```
Target appears on screen
    ↓ (~16ms at 60fps game)
Next capture includes target
    ↓ (~3-5ms processing)
Mouse movement sent
    ↓ (~1ms driver)
Crosshair moves on screen
    ↓ (~16ms at 60fps game)
Total: ~35-40ms end-to-end
```

---

## Code References

| File | Purpose |
|------|---------|
| `src/unibot.py` | Main loop, timing control |
| `src/screen.py` | Capture and color detection |
| `src/cheats.py` | Smoothing algorithm |
| `src/mouse/` | Input injection implementations |
| `src/configReader.py` | Configuration parsing |
| `src/utils.py` | Key bindings, state management |
