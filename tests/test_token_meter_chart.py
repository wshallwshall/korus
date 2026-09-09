"""Source mutations must update the chart data or fail loudly."""
import importlib.util
from pathlib import Path
import sys
import unittest
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("token_meter_chart", ROOT / "scripts/site/plot_token_meter.py")
chart = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = chart
SPEC.loader.exec_module(chart)


class TokenMeterChartTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / "docs/TOKEN-ACCOUNTING.md").read_text(encoding="utf-8")

    def test_source_change_flows_into_plot_data(self):
        data = chart.parse_measurement(self.source.replace("60,475,507", "60,475,508"))
        self.assertEqual(data.raw[0], 60_475_508)
        self.assertEqual(data.accounts, ("A", "B", "C", "D"))

    def test_missing_row_rejected(self):
        source = "\n".join(line for line in self.source.splitlines() if not line.startswith("| D | 97"))
        with self.assertRaises(ValueError):
            chart.parse_measurement(source)

    def test_duplicate_table_rejected(self):
        with self.assertRaises(ValueError):
            chart.parse_measurement(self.source + self.source)

    def test_renamed_column_rejected(self):
        with self.assertRaises(ValueError):
            chart.parse_measurement(self.source.replace("Non-cache-read per 1 percent", "Other tokens"))

    def test_missing_caveat_rejected(self):
        with self.assertRaises(ValueError):
            chart.parse_measurement(self.source.replace("activity on two days with no local transcripts", "activity"))

    def test_committed_charts_match_current_source(self):
        data = chart.parse_measurement(self.source)
        for filename in ("g13-token-meter.svg", "g13-token-meter-mobile.svg"):
            root = ElementTree.parse(ROOT / "docs/assets/charts" / filename).getroot()
            labels = ["".join(node.itertext()) for node in root.iter("{http://www.w3.org/2000/svg}text")]
            for node in root.iter("{http://www.w3.org/2000/svg}text"):
                self.assertIn("font-family: Arial, sans-serif", node.get("style", ""))
            for value in data.raw + data.non_cache:
                self.assertEqual(labels.count(f"{value:,}"), 1, filename)
            self.assertIn(f"{data.date} | n = 4 accounts", labels)
            self.assertEqual(labels.count("0"), 2, "Both axes must start at zero")
            self.assertEqual(labels.count("Tokens per meter point"), 2)
            self.assertEqual(labels.count("D*"), 2)
            self.assertIn("two days of meter activity", " ".join(labels))


if __name__ == "__main__":
    unittest.main()
