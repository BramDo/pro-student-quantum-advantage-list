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
            {entry["scale"]["qubits"] for entry in entries}, {51, 70, 72, 80, 120}
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

    def test_withdrawn_qml_project_is_absent_from_public_register(self):
        # Feature-generation timing does not establish useful QML advantage.
        withdrawn = "qos-pbmc68k-qml-60q"
        self.assertNotIn(withdrawn, {entry["id"] for entry in BUILD.load_entries()})
        for path in [ROOT / "README.md", *BUILD.outputs(BUILD.load_entries())]:
            content = path.read_text(encoding="utf-8")
            self.assertNotIn(withdrawn, content, path)
            self.assertNotIn("PBMC68k QML 60q", content, path)

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

    def test_nighthawk_preserves_timing_and_accuracy_boundaries(self):
        entry = json.loads((ROOT / "entries" / "fermi-hubbard-2d-nighthawk-72q.json").read_text(encoding="utf-8"))
        self.assertEqual(entry["comparison"]["classification"], "local_execution_metric")
        self.assertFalse(entry["comparison"]["ratio_is_lower_bound"])
        self.assertEqual(BUILD.primary_timing(entry)["seconds"], 7.0)
        self.assertEqual([t["seconds"] for t in entry["quantum"]["timings"]], [7.0, 8.0, 180.858322])
        self.assertAlmostEqual(entry["comparison"]["ratio"], entry["classical_baselines"][0]["seconds"] / 7)
        boundaries = " ".join(entry["claim_boundary"])
        for text in ["not a 20x shorter end-to-end", "Both TFLO holdout checks failed", "not converged", "Chi128 was not performed", "remains private"]:
            self.assertIn(text, boundaries)
        self.assertIn("not a replacement for measured N", boundaries)
        self.assertIn("public project-report route", entry["implementation"]["access_note"])

    def test_nighthawk_access_note_and_ratio_are_visible(self):
        for file in ["docs/index.html", "docs/edukaizen-page.html", "ADVANTAGE_LIST.md"]:
            content = (ROOT / file).read_text(encoding="utf-8")
            for text in ["2D Hubbard Nighthawk", "21.55x", "circa 20x", "accuracy unvalidated", "private GitHub repository", "Both TFLO holdout checks failed"]:
                self.assertIn(text, content)
        wp = (ROOT / "docs/edukaizen-page.html").read_text(encoding="utf-8")
        self.assertIn("6 student-scale project reports", wp)
        self.assertNotIn("Five complete", wp)

    def test_classification_contract_matches_renderer(self):
        schema = json.loads((ROOT / "schema" / "entry.schema.json").read_text())
        values = schema["properties"]["comparison"]["properties"]["classification"]["enum"]
        self.assertEqual(set(values), set(BUILD.CLASSIFICATIONS))

    def test_edukaizen_fragment_is_embeddable(self):
        content = (ROOT / "docs" / "edukaizen-page.html").read_text(encoding="utf-8")
        self.assertNotIn("<!doctype html>", content.lower())

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
