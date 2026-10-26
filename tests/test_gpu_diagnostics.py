import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from gpu_diagnostics import parse_nvidia_smi


class DiagnosticsTest(unittest.TestCase):
    def test_health_classification(self):
        fixture = (Path(__file__).parent / "fixtures" / "nvidia_smi.csv").read_text()
        gpus = parse_nvidia_smi(fixture)
        self.assertEqual([g.status for g in gpus], ["healthy", "critical"])
        self.assertTrue(gpus[1].throttle_active)

    def test_invalid_columns(self):
        with self.assertRaises(ValueError):
            parse_nvidia_smi("0, H100")


if __name__ == "__main__":
    unittest.main()
