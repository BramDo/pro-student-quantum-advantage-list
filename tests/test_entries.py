import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build", ROOT / "scripts" / "build.py")
BUILD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BUILD)


class EntryTests(unittest.TestCase):
    def test_six_entries_validate(self):
        entries = BUILD.load_entries()
        self.assertEqual(len(entries), 6)
        self.assertEqual(
            {entry["scale"]["qubits"] for entry in entries}, {51, 60, 70, 80, 120}
        )

    def test_every_entry_is_challengeable(self):
        for entry in BUILD.load_entries():
            self.assertTrue(entry["official_sources"])
            self.assertTrue(entry["classical_baselines"])
            self.assertTrue(entry["claim_boundary"])
            self.assertIn("edukaizen.nl", entry["implementation"]["edukaizen_url"])
            self.assertEqual(sum(item["primary"] for item in entry["quantum"]["timings"]), 1)

    def test_q80_remains_a_lower_bound_not_a_formal_claim(self):
        entry = json.loads((ROOT / "entries" / "operator-loschmidt-echo-q80.json").read_text(encoding="utf-8"))
        self.assertEqual(entry["comparison"]["classification"], "local_runtime_lower_bound")
        self.assertTrue(entry["comparison"]["ratio_is_lower_bound"])
        self.assertIn("did not converge", " ".join(entry["claim_boundary"]))

    def test_random_graph_remains_diagnostic_only(self):
        entry = json.loads((ROOT / "entries" / "random-graph-sampling-70q.json").read_text(encoding="utf-8"))
        self.assertEqual(entry["comparison"]["classification"], "diagnostic_only")
        self.assertIsNone(entry["comparison"]["ratio"])
        boundaries = " ".join(entry["claim_boundary"])
        self.assertIn("not evidence of quantum advantage", boundaries)
        self.assertIn("restricted access to IBM Boston", boundaries)
        self.assertIn("IBM Kingston", boundaries)

    def test_qml_entry_is_a_bounded_local_runtime_advantage(self):
        entry = json.loads((ROOT / "entries" / "qos-pbmc68k-qml-60q.json").read_text(encoding="utf-8"))
        self.assertEqual(entry["comparison"]["classification"], "local_runtime_lower_bound")
        self.assertTrue(entry["comparison"]["ratio_is_lower_bound"])
        self.assertGreater(entry["comparison"]["ratio"], 99.1)
        self.assertEqual(entry["quantum"]["timings"][0]["seconds"], 26.0)
        boundaries = " ".join(entry["claim_boundary"])
        self.assertIn("did not converge", boundaries)
        self.assertIn("submission-to-retrieval", boundaries)
        self.assertIn("not an end-to-end speedup", boundaries)

    def test_floquet_entry_is_partial_time_to_signal_advantage(self):
        entry = json.loads(
            (ROOT / "entries" / "floquet-ising-51q.json").read_text(encoding="utf-8")
        )
        self.assertEqual(entry["comparison"]["classification"], "local_time_to_answer")
        self.assertAlmostEqual(entry["comparison"]["ratio"], 8.930964505048817)
        self.assertEqual(entry["quantum"]["timings"][0]["seconds"], 41.0)
        self.assertEqual(entry["classical_baselines"][0]["seconds"], 366.1695447070015)
        boundaries = " ".join(entry["claim_boundary"])
        self.assertIn("partial, task-specific", boundaries)
        self.assertIn("SRMSE 3.154", boundaries)
        self.assertIn("maximum absolute z-score 6.932", boundaries)

    def test_generated_outputs_are_current(self):
        for path, content in BUILD.outputs(BUILD.load_entries()).items():
            self.assertTrue(path.exists(), path)
            self.assertEqual(path.read_text(encoding="utf-8"), content)

    def test_edukaizen_fragment_contains_the_qml_advantage(self):
        content = (ROOT / "docs" / "edukaizen-page.html").read_text(encoding="utf-8")
        self.assertIn("PBMC68k QML 60q", content)
        self.assertIn("greater than 99.1x", content)
        self.assertIn("17/32", content)
        self.assertIn("26 quantum-seconds", content)
        self.assertNotIn("<!doctype html>", content.lower())

    def test_github_pages_contains_the_qml_score_and_timing(self):
        content = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        self.assertIn("PBMC68k QML 60q", content)
        self.assertIn("17/32", content)
        self.assertIn("greater than 99.1x", content)
        self.assertIn("greater than 5.0x", content)

    def test_readme_and_public_pages_contain_floquet_boundary(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        pages = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        edukaizen = (ROOT / "docs" / "edukaizen-page.html").read_text(
            encoding="utf-8"
        )
        for content in (readme, pages, edukaizen):
            self.assertIn("Floquet-Ising 51q", content)
            self.assertIn("8.93", content)
        self.assertIn("accuracy is not matched", readme)
        self.assertIn("SRMSE 3.154", pages)


if __name__ == "__main__":
    unittest.main()
