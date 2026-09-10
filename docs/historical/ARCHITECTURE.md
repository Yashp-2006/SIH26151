# PRAMANA Architecture

## Component Diagram
```text
[External Data] --> [Ingestion Adapter] --> [Canonicalization]
                                                |
                                                v
[List-B Probabilistic] <--- [Redaction] <--- [List-A Deterministic]
        |                                       |
        +------------> [Fusion Core] <----------+
                             | (Applies tau and k limits)
                             v
                     [Balance Sheet] ---> [FastAPI Gateway] ---> [Analyst / LLM]
```

## Data Flow & Control Flow
1. Raw listing text is canonicalized.
2. `List-A` indicators (PGP, BTC) are extracted deterministically.
3. `Redaction` mathematically scrubs `List-A` from the raw text.
4. `List-B` extracts stylometric and semantic embeddings from the scrubbed text.
5. Both output `EvidenceCandidate` objects to the `Fusion Core`.
6. Fusion enforces independence ($k \ge 2$) and rarity scaling.
7. Outputs an immutable `BalanceSheetResponse`.

## Trust Boundaries
- **UNTRUSTED:** Raw dark-web text.
- **TRUSTED:** Cryptographic validations (PGP signatures).
- **AIR-GAPPED:** The LLM Analyst. The LLM is strictly prohibited from mutating the Log-LR scores. It may only read the finalized Balance Sheet to output English explanations.
