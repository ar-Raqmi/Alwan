# Visual Detection Guide: Identifying Colorbot Users When Spectating

## Overview
This guide helps you identify players using colorbots like Unibot through visual observation when spectating. Based on the actual behavior of this colorbot implementation.

---

## Key Visual Indicators (Ranked by Detectability)

### 🔴 HIGH CONFIDENCE INDICATORS

#### 1. **Unnatural Aim Smoothing Patterns**
**What to look for:**
- **Perfect exponential curves** when tracking targets
- Aim follows a mathematically smooth arc (not human micro-corrections)
- Movement looks "floaty" or "magnetic" rather than snappy

**Why it happens:**
- Unibot uses exponential smoothing: `new_position = (1 - smoothing) * old + smoothing * target`
- Produces consistent curved movements every time
- Real players have jitter, micro-adjustments, and inconsistent tracking

**Test:** Watch them track a moving target - colorbot will have perfect smooth curves, humans have choppy corrections.

---

#### 2. **Instant Target Switching to Closest Enemy**
**What to look for:**
- When multiple enemies appear, aim **instantly snaps to the closest one**
- No consideration for threat level, positioning, or tactics
- Switches targets mid-spray if a closer enemy enters detection zone

**Why it happens:**
- Unibot selects target by minimum Euclidean distance: `distance = sqrt(x² + y²)`
- Always picks closest contour, ignoring game context
- Code location: `screen.py` lines 104-118

**Test:** Watch them engage multiple enemies - they'll always prioritize distance over tactical sense.

---

#### 3. **Consistent Vertical Targeting (aim_height)**
**What to look for:**
- Always aims at **exactly the same vertical point** on enemy model
- Never varies between head, chest, or legs based on situation
- Statistical anomaly in shot placement across many engagements

**Why it happens:**
- Unibot uses fixed `aim_height` parameter (0.5 = center, 0.3 = head)
- Calculation: `y = rect_y + rect_h * (1 - aim_height)`
- Real players vary aim based on recoil, panic, distance, movement

**Test:** Analyze killcam footage - colorbot users have identical vertical aim placement ratio across kills.

---

#### 4. **Perfect Sub-Pixel Precision**
**What to look for:**
- Crosshair centers **perfectly** on target hitbox every time
- No overshooting or undershooting when acquiring targets
- Perfectly smooth deceleration when reaching target

**Why it happens:**
- Unibot accumulates fractional pixels: `remainder_x = move_x - int(move_x)`
- Sub-pixel precision tracking in `base_mouse.py` lines 28-36
- Humans can't achieve perfect pixel-level centering consistently

**Test:** Frame-by-frame analysis of target acquisition - colorbot has pixel-perfect centering.

---

#### 5. **Reaction Time Anomalies**
**What to look for:**
- **Too fast**: Aims/shoots before human reaction time (< 150ms)
- **Too consistent**: Reaction time variance is very low across engagements
- **Robotic timing**: Same delay pattern every encounter

**Why it happens:**
- Unibot runs at 60 FPS (16.67ms per frame)
- Zero cognitive delay between detection and response
- Optional `trigger_delay` adds fixed/randomized delay but creates patterns

**Test:** Measure time from enemy appearing on screen to first shot - humans: 180-300ms avg, bots: < 100ms or suspiciously consistent.

---

### 🟡 MEDIUM CONFIDENCE INDICATORS

#### 6. **Detection-Based Aiming (Not Prediction-Based)**
**What to look for:**
- Aims at **current position** of enemy, not where they're moving
- Always slightly behind fast-moving targets
- No lead shots or prediction

**Why it happens:**
- Unibot detects enemy position each frame and aims at current center
- No velocity calculation or movement prediction
- Code: `screen.py` calculates static contour center, not trajectory

**Test:** Watch them shoot at strafing enemies - will track behind movement direction.

---

#### 7. **Only Engages When Enemy Highlighted**
**What to look for:**
- Perfect accuracy when enemies are highlighted/visible
- Completely misses or ignores enemies without highlight color
- No aiming at smoke/walls where enemies might be (no pre-fire instinct)

**Why it happens:**
- Colorbot only detects HSV color range (140-155 hue for your purple config)
- No ESP or wallhack capability
- Blind to enemies without the configured highlight color

**Test:** Check if they ignore non-highlighted enemies or have 100% engagement rate with highlighted ones.

---

#### 8. **FOV-Restricted Awareness**
**What to look for:**
- Only reacts to enemies in **small center region** of screen (256x256 pixels default)
- Ignores enemies at screen edges even if visible
- Never pre-aims at corners outside detection zone

**Why it happens:**
- Unibot only scans `capture_fov_x/y` region (default 256x256)
- Detection zone: `screen_center ± 128 pixels` in each direction
- Config setting in your `config.ini` line 33-34

**Test:** Enemies at screen edges won't trigger aim assist - they'll aim manually with different movement patterns.

---

#### 9. **Identical Click Timing Patterns**
**What to look for:**
- Time between clicks is **suspiciously regular** when using triggerbot
- Rapid fire has consistent CPS (clicks per second)
- No variation in fire rate under pressure

**Why it happens:**
- Triggerbot uses CPS limiter: `1 / config.target_cps` (default 10 CPS = 100ms)
- Random humanization delay: 40-80ms + 25-35ms per click
- Statistical pattern emerges over many shots

**Test:** Measure inter-shot timing - humans vary wildly (panic spray vs calm), bots have tight distribution.

---

#### 10. **Crosshair Micro-Movements During Tracking**
**What to look for:**
- Tiny continuous adjustments when tracking
- Movement continues even when already on target
- "Hunting" behavior with small oscillations

**Why it happens:**
- Unibot recalculates aim offset every frame (60 times/sec)
- No "good enough" threshold - always adjusting
- Small detection variations cause micro-corrections

**Test:** Slow-motion footage shows constant tiny adjustments, humans have brief "settled" periods.

---

### 🟢 LOW CONFIDENCE INDICATORS (Require Context)

#### 11. **No Recoil Compensation Errors**
**What to look for:**
- Perfect spray patterns with no drift
- Consistent recoil control even during movement/panic
- Never over-compensates or under-compensates

**Why it happens:**
- Recoil control: `move_y += recoil_y * delta_time`
- Fixed offset applied every frame
- Config: `recoil_x`, `recoil_y` in your `config.ini` line 42-43

**Note:** Less reliable - skilled players can have good recoil control too.

---

#### 12. **Screen Center Dependency**
**What to look for:**
- Better performance when enemy near screen center
- Struggles more with peripheral targets
- Accuracy drops at screen edges

**Why it happens:**
- Aim calculation uses distance from screen center
- FOV limitations (256x256 center region)
- Speed/smoothing optimized for center targets

**Test:** Compare engagement success rate: center vs peripheral vision.

---

## Advanced Detection: Statistical Analysis

### Metrics to Track Over Multiple Games

1. **Aim Smoothing Consistency**
   - Calculate aim acceleration variance
   - Colorbot: Very low variance (same exponential curve)
   - Human: High variance (different corrections each time)

2. **Target Switch Speed Distribution**
   - Measure time to switch between targets
   - Colorbot: Gaussian distribution, tight clustering
   - Human: Wide variance, context-dependent

3. **Vertical Aim Placement Ratio**
   - Calculate `(hitbox_y - hit_y) / hitbox_height` for each kill
   - Colorbot: Clusters around configured `aim_height` value
   - Human: Distributed across full hitbox based on recoil/situation

4. **Reaction Time Distribution**
   - Plot histogram of reaction times (enemy visible → shot fired)
   - Colorbot: Tight distribution around configured delay
   - Human: Right-skewed distribution (180-400ms range)

5. **Crosshair Velocity Analysis**
   - Calculate pixels/second during target acquisition
   - Colorbot: Smooth exponential decay curve
   - Human: Spiky, inconsistent acceleration patterns

---

## Behavioral Patterns (Non-Visual)

### Gameplay Behavior That Suggests Colorbot Use:

1. **Over-reliance on highlighted enemies**
   - Ignores tactical positioning
   - Doesn't check common angles without highlights
   - No game sense, pure mechanical aim

2. **No pre-aiming or prediction**
   - Reacts only after seeing highlighted enemy
   - No anticipation of enemy positions
   - Doesn't pre-fire common spots

3. **Inconsistent performance across situations**
   - Godlike aim when enemies highlighted
   - Potato aim on non-highlighted targets
   - Struggles with smoke/utility fights

4. **Unusual target prioritization**
   - Always shoots closest target (even if low HP enemy is safer)
   - Ignores threats from dangerous positions
   - No tactical target selection

---

## Detection Countermeasures for Your Game

Based on Unibot's behavior, implement these anti-cheat features:

### Server-Side Detection

1. **Aim Curve Analysis**
   ```
   - Track mouse input patterns
   - Flag exponential smoothing curves (mathematical signature)
   - Compare to known colorbot smoothing algorithms
   ```

2. **Target Switch Speed Checks**
   ```
   - Measure target acquisition time between enemies
   - Flag instant switches (< 100ms) with perfect centering
   - Build profile of normal human switching behavior
   ```

3. **Vertical Aim Consistency**
   ```
   - Calculate shot placement distribution per player
   - Flag if >80% of shots hit same vertical ratio (e.g., all at 0.5 height)
   - Human shots should vary based on recoil, movement, etc.
   ```

4. **Reaction Time Analysis**
   ```
   - Measure time from enemy entering FOV → first shot
   - Flag reaction times < 150ms or extremely consistent patterns
   - Build behavioral profile over multiple matches
   ```

### Client-Side Visual Obfuscation

1. **Dynamic Enemy Colors**
   - Randomly shift highlight hue by ±10-20°
   - Makes HSV detection unreliable
   - Adjust frequently (every 30-60 seconds)

2. **Color Noise Injection**
   - Add slight color variations to enemy models
   - Breaks contour detection accuracy
   - Introduces false positives in color masking

3. **Decoy Highlights**
   - Display fake highlight colors in environment
   - Confuses closest-target selection
   - Causes colorbot to aim at walls/decoys

4. **Remove Highlight System**
   - Most reliable solution
   - Forces players to use game sense instead of color indicators
   - Makes colorbots completely ineffective

---

## Testing Methodology

### How to Test If Someone Is Using This Colorbot:

1. **Spectate 5-10 engagements** and check for:
   - [ ] Smooth exponential aim curves
   - [ ] Instant closest-target switching
   - [ ] Consistent vertical aim placement
   - [ ] Sub-pixel centering precision
   - [ ] Reaction time < 150ms or suspiciously consistent

2. **Frame-by-frame analysis** (slow down killcam):
   - [ ] Check for micro-adjustments (continuous corrections)
   - [ ] Measure pixel-perfect centering
   - [ ] Calculate aim curve acceleration

3. **Statistical analysis** (across multiple matches):
   - [ ] Plot reaction time distribution
   - [ ] Calculate vertical aim consistency
   - [ ] Measure target switch speed variance

4. **Behavioral observation**:
   - [ ] Check if they ignore non-highlighted enemies
   - [ ] Test FOV limitations (edges vs center performance)
   - [ ] Look for no-prediction aiming (lagging behind moving targets)

---

## Summary: Most Reliable Indicators

**If you see 3+ of these, high probability of colorbot:**

1. ✅ Perfect exponential smooth aim curves
2. ✅ Instant closest-target prioritization
3. ✅ Consistent vertical aim placement (same hitbox ratio every time)
4. ✅ Reaction times < 150ms or extremely consistent
5. ✅ Pixel-perfect centering on target
6. ✅ Only engages highlighted enemies, ignores others

**Single strongest indicator:**
> Mathematical smoothing patterns in aim movement - humans cannot replicate exponential curves consistently.

---

## Configuration Context

Your current Unibot setup:
- **Color target**: RGB(248, 76, 254) - Bright purple/magenta
- **HSV range**: H: 140-155, S: 178-255, V: 242-255
- **Detection area**: 256x256 pixels (center of screen)
- **Aim smoothing**: 0.0 (disabled, instant snap - VERY OBVIOUS)
- **Speed**: 1.0x
- **Aim height**: 0.5 (center mass)
- **Trigger**: Right-click (0x02)
- **Loop rate**: 60 FPS

**Note:** With `aim_smoothing_factor = 0.0`, the aim will snap **instantly** to targets, making it extremely obvious. Consider testing with 0.3-0.5 for more realistic research.

---

## Files Referenced

- Detection algorithm: [src/screen.py](src/screen.py) lines 84-140
- Aim calculation: [src/cheats.py](src/cheats.py) lines 28-67
- Sub-pixel tracking: [src/mouse/base_mouse.py](src/mouse/base_mouse.py) lines 28-36
- Main loop: [src/unibot.py](src/unibot.py) lines 30-75
- Configuration: [config.ini](config.ini)

---

**Remember:** This is for anti-cheat research purposes. Use these insights to build detection systems and improve your game's competitive integrity.
