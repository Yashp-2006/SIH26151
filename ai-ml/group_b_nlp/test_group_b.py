import sys
import os
import unittest
from pathlib import Path

# Add root to sys.path so 'shared' and 'group_b_nlp' can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

from group_b_nlp.lang_ner import analyze_text
from group_b_nlp.stylometry import extract_style_features
from group_b_nlp.style_shift import detect_style_shift
from group_b_nlp.template_fp import template_fingerprint

class TestGroupBNLP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = Path(__file__).parent.parent / "data"
        cls.darknet_dir = cls.test_dir / "darknet_archives_sample"
        cls.stylometry_dir = cls.test_dir / "stylometry_sample"
        
        cls.darknet_dir.mkdir(parents=True, exist_ok=True)
        cls.stylometry_dir.mkdir(parents=True, exist_ok=True)
        
        cls.sample_darknet = cls.darknet_dir / "sample1.txt"
        cls.sample_darknet.write_text("Hello John Doe from Microsoft. Buy BTC at 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa for $5.00.", encoding="utf-8")
        
        cls.sample_stylo_1 = cls.stylometry_dir / "stylo1.txt"
        cls.sample_stylo_1.write_text("This is the first document. It has some very basic words.", encoding="utf-8")
        cls.sample_stylo_2 = cls.stylometry_dir / "stylo2.txt"
        cls.sample_stylo_2.write_text("This is the second document. Indeed, it possesses different vocabulary.", encoding="utf-8")
        cls.sample_stylo_3 = cls.stylometry_dir / "stylo3.txt"
        cls.sample_stylo_3.write_text("Hola. Me llamo Juan.", encoding="utf-8")

    def test_lang_ner(self):
        text = self.sample_darknet.read_text(encoding="utf-8")
        result = analyze_text(text)
        self.assertIn("language", result)
        self.assertIn("en", result["language"])
        self.assertIn("John Doe", str(result.get("entities", [])))
        self.assertIn("Microsoft", str(result.get("entities", [])))
        self.assertIn("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", str(result.get("crypto_addresses", [])))

    def test_stylometry(self):
        text = self.sample_stylo_1.read_text(encoding="utf-8")
        features = extract_style_features(text)
        self.assertIn("function_words", features)
        self.assertIn("char_ngrams", features)
        self.assertTrue(len(features["function_words"]) > 0)

    def test_style_shift(self):
        docs = [
            self.sample_stylo_1.read_text(encoding="utf-8"),
            self.sample_stylo_1.read_text(encoding="utf-8"),
            self.sample_stylo_2.read_text(encoding="utf-8"),
            self.sample_stylo_3.read_text(encoding="utf-8")
        ]
        shifts = detect_style_shift(docs)
        self.assertTrue(isinstance(shifts, list))
        self.assertTrue(len(shifts) > 0)
        self.assertIn("shift_score", shifts[0])

    def test_template_fp(self):
        text = "Item: 1g Weed\nPrice: $10.00\nContact: user@jabber.ru"
        fp = template_fingerprint(text)
        self.assertTrue(isinstance(fp, str))
        self.assertTrue(len(fp) > 0)

if __name__ == '__main__':
    unittest.main()
