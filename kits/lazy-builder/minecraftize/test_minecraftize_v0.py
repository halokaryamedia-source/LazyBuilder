from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from minecraftize_v0 import GridSpec, MinecraftizeError, blocks_from_occupied, grid_spec_from_bounds, index_to_minecraft

class MinecraftizeV0PureTests(unittest.TestCase):
    def test_grid_width_drives_pitch_and_other_axes(self):
        spec = grid_spec_from_bounds((0, 0, 0), (10, 5, 3), 10)
        self.assertEqual(spec, GridSpec(pitch=1.0, nx=10, ny=5, nz=3))

    def test_grid_rounds_non_width_axes_up(self):
        spec = grid_spec_from_bounds((0, 0, 0), (8, 4.1, 2.01), 8)
        self.assertEqual((spec.nx, spec.ny, spec.nz), (8, 5, 3))

    def test_blender_y_reverses_to_minecraft_z(self):
        spec = GridSpec(1.0, 3, 4, 2)
        self.assertEqual(index_to_minecraft(1, 0, 1, spec), (1, 1, 3))
        self.assertEqual(index_to_minecraft(1, 3, 1, spec), (1, 1, 0))

    def test_full_block_mapping_is_deterministic(self):
        spec = GridSpec(1.0, 2, 2, 2)
        blocks = blocks_from_occupied([(1, 1, 1), (0, 0, 0)], spec)
        self.assertEqual([(b.x, b.y, b.z) for b in blocks], [(1, 1, 0), (0, 0, 1)])

    def test_invalid_target_width_rejected(self):
        with self.assertRaises(MinecraftizeError):
            grid_spec_from_bounds((0, 0, 0), (1, 1, 1), 0)

    def test_blender_import_is_lazy(self):
        self.assertNotIn("bpy", sys.modules)

if __name__ == "__main__":
    unittest.main()
