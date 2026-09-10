"""Runner for the Canonicalization and Repetition layer."""

from typing import List, Dict, Tuple
from collections import defaultdict

from adapters.gwern_grams.models import NormalizedRecord
from canonicalization.models import (
    RepetitionReference, CanonicalTextContent, NearDuplicateCandidate
)
from canonicalization.text_hashing import (
    compute_sha256, compute_simhash, compute_shingles,
    hamming_distance, compute_containment
)

class CanonicalizationPipeline:
    def __init__(self):
        self.exact_rows: Dict[str, List[NormalizedRecord]] = defaultdict(list)
        self.market_hashes: Dict[Tuple[str, str], List[NormalizedRecord]] = defaultdict(list)
        self.market_urls: Dict[Tuple[str, str], List[NormalizedRecord]] = defaultdict(list)
        self.exact_contents: Dict[Tuple[str, str], List[NormalizedRecord]] = defaultdict(list)
        self.text_contents: List[CanonicalTextContent] = []
        
    def process_records(self, records: List[NormalizedRecord]):
        for rec in records:
            # 1. Exact full-row equality (all 11 source fields)
            row_tuple = tuple(rec.source_record.raw_values[k] for k in [
                "hash", "market_name", "item_link", "vendor_name", "price",
                "name", "description", "image_link", "add_time", "ship_from"
            ])
            # Include trailing cell for exactness
            row_sig = str(row_tuple) + rec.source_record.trailing_empty_cell
            self.exact_rows[row_sig].append(rec)
            
            # 2. (market_name, hash)
            m_raw = rec.source_record.raw_values["market_name"]
            h_raw = rec.source_record.raw_values["hash"]
            if m_raw and h_raw:
                self.market_hashes[(m_raw, h_raw)].append(rec)
                
            # 3. (market_name, item_link)
            u_raw = rec.source_record.raw_values["item_link"]
            if m_raw and u_raw:
                self.market_urls[(m_raw, u_raw)].append(rec)
                
            # 4. Exact (name, description)
            n_raw = rec.source_record.raw_values["name"]
            d_raw = rec.source_record.raw_values["description"]
            # Exclude totally empty content from exact content matches to avoid spam
            if n_raw or d_raw:
                self.exact_contents[(n_raw, d_raw)].append(rec)
                
                # Compute canonical text for near-duplicate analysis
                tc = CanonicalTextContent(
                    source_record_id=rec.source_record.id,
                    snapshot_id=rec.source_record.snapshot_id,
                    title_raw=rec.listing_observation.title,
                    description_raw=rec.listing_observation.description,
                    content_sha256=compute_sha256(rec.listing_observation.title, rec.listing_observation.description),
                    simhash_64=compute_simhash(rec.listing_observation.title, rec.listing_observation.description),
                    shingles=compute_shingles(rec.listing_observation.title, rec.listing_observation.description)
                )
                self.text_contents.append(tc)

    def extract_repetition_references(self) -> List[RepetitionReference]:
        refs = []
        
        def _extract(group_dict, ref_type, shared_val_func):
            for key, recs in group_dict.items():
                if len(recs) > 1:
                    for i in range(len(recs)):
                        for j in range(i + 1, len(recs)):
                            r1 = recs[i]
                            r2 = recs[j]
                            cross = (r1.source_record.snapshot_id != r2.source_record.snapshot_id)
                            refs.append(RepetitionReference(
                                type=ref_type,
                                from_record_id=r1.source_record.id,
                                to_record_id=r2.source_record.id,
                                shared_value=shared_val_func(key),
                                cross_snapshot=cross
                            ))
                            
        _extract(self.exact_rows, "exact_row_match", lambda k: "full_row")
        _extract(self.market_hashes, "repeated_market_hash", lambda k: f"{k[0]}:{k[1]}")
        _extract(self.market_urls, "repeated_market_item_link", lambda k: f"{k[0]}:{k[1]}")
        _extract(self.exact_contents, "exact_content_match", lambda k: "content_equality")
        
        return refs

    def compute_near_duplicates(self, max_hamming: int = 10, min_jaccard: float = 0.5) -> List[NearDuplicateCandidate]:
        candidates = []
        n = len(self.text_contents)
        for i in range(n):
            for j in range(i + 1, n):
                tc1 = self.text_contents[i]
                tc2 = self.text_contents[j]
                
                # Skip exact duplicates for near-duplicate candidates (they are already exact_content_match)
                if tc1.content_sha256 == tc2.content_sha256:
                    continue
                    
                h_dist = hamming_distance(tc1.simhash_64, tc2.simhash_64)
                if h_dist <= max_hamming:
                    jac, c1, c2 = compute_containment(tc1.shingles, tc2.shingles)
                    if jac >= min_jaccard or max(c1, c2) >= 0.8:
                        candidates.append(NearDuplicateCandidate(
                            source_record_id_1=tc1.source_record_id,
                            source_record_id_2=tc2.source_record_id,
                            hamming_distance=h_dist,
                            jaccard_similarity=jac,
                            containment_1_in_2=c1,
                            containment_2_in_1=c2
                        ))
        return candidates
