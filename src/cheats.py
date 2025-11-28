"""
    Alwan - Colorbot Research Project (fork of Unibot)
    Original Copyright (C) 2025 vike256

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import win32api
import numpy as np


class Cheats:
    def __init__(self, config):
        self.cfg = config
        self.move_x, self.move_y = (0, 0)
        self.recoil_offset = 0

    def calculate_aim(self, state, target, delta_time):
        """
        UCAimColor-style smoothing formula: target / smooth * speed

        - smooth = 1.0: move (target * speed) pixels - fast snap
        - smooth = 1.5: move (target * 0.67 * speed) pixels - UCAimColor default
        - smooth = 3.0: move (target * 0.33 * speed) pixels - smooth tracking

        The speed multiplier compensates for in-game sensitivity.
        Higher speed = more aggressive movement per frame.
        """
        if state and target is not None:
            target_x, target_y = target

            # UCA formula: target / smooth * speed
            smooth = max(1.0, self.cfg.aim_smoothing_factor)  # Minimum 1.0
            speed = self.cfg.speed

            self.move_x = (target_x / smooth) * speed
            self.move_y = (target_y / smooth) * speed * self.cfg.y_speed_multiplier
        else:
            self.move_x = 0
            self.move_y = 0

    def apply_recoil(self, state, delta_time):
        if state and delta_time != 0:
            if self.cfg.recoil_mode == 'move' and win32api.GetAsyncKeyState(0x01) < 0:
                self.move_x += self.cfg.recoil_x * delta_time
                self.move_y += self.cfg.recoil_y * delta_time
            elif self.cfg.recoil_mode == 'offset':
                if win32api.GetAsyncKeyState(0x01) < 0:
                    if self.recoil_offset < self.cfg.max_offset:
                        self.recoil_offset += self.cfg.recoil_y * delta_time
                        if self.recoil_offset > self.cfg.max_offset:
                            self.recoil_offset = self.cfg.max_offset
                else:
                    if self.recoil_offset > 0:
                        self.recoil_offset -= self.cfg.recoil_recover * delta_time
                        if self.recoil_offset < 0:
                            self.recoil_offset = 0
        else:
            self.recoil_offset = 0
