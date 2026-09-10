import sys
import os
import unittest
from pathlib import Path
import pandas as pd

# Add root to sys.path so 'shared' and 'group_c_wallet_infra' can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

from group_c_wallet_infra.wallet_cluster import cluster_wallets, lookup_risk
from group_c_wallet_infra.infra_fp import fingerprint_infra
from group_c_wallet_infra.temporal import temporal_overlap

class TestGroupC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = Path(__file__).parent.parent / "data"
        cls.test_dir.mkdir(parents=True, exist_ok=True)
        
        cls.csv_path = cls.test_dir / "bitcoinheist_sample.csv"
        # Mock CSV: address, year, day, length, weight, count, loop, neighbors, income, label
        csv_content = """address,year,day,length,weight,count,loop,neighbors,income,label
1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa,2011,1,18,0.08,1,0,2,100,white
1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2,2012,2,144,0.1,1,0,2,200,princetonCerber
1EZ69XwA12M9g2zR9Wv1wXQZqW2wB3n8v,2013,3,2,0.5,1,0,2,300,white
"""
        cls.csv_path.write_text(csv_content, encoding="utf-8")

    def test_wallet_cluster(self):
        # same-transaction multi-input
        transactions = [
            {"txid": "tx1", "inputs": ["addr1", "addr2"], "outputs": ["addr3"]},
            {"txid": "tx2", "inputs": ["addr2", "addr4"], "outputs": ["addr5"]}
        ]
        clusters = cluster_wallets(transactions)
        self.assertEqual(clusters["addr1"], clusters["addr4"])
        
        # lookup_risk
        label = lookup_risk("1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2")
        self.assertEqual(label, "princetonCerber")
        label_safe = lookup_risk("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
        self.assertEqual(label_safe, "white")

    def test_infra_fp(self):
        metadata = {
            "tls": {"subject": "CN=example.com", "san": ["example.com"]},
            "favicon_hash": "12345abcd",
            "headers": {"Server": "nginx", "X-Powered-By": "PHP"}
        }
        fp = fingerprint_infra(metadata)
        self.assertIn("tls_subject", fp)
        self.assertEqual(fp["favicon_hash"], "12345abcd")
        self.assertIn("Server", fp["headers"])

    def test_temporal(self):
        events_a = ["2023-01-01T10:00:00", "2023-01-05T12:00:00"]
        events_b = ["2023-01-01T10:05:00", "2023-01-20T08:00:00"]
        score = temporal_overlap(events_a, events_b, window_days=1)
        self.assertTrue(score > 0.0)

if __name__ == '__main__':
    unittest.main()
