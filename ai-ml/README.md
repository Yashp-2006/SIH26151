# PRAMANA List A

- **Project:** PRAMANA List A — Evidence Generation modules for the SIH26151 dark-web attribution platform
- **Structure:** `shared/` (frozen contract + data loader), `group_a_deterministic/`, `group_b_nlp/`, `group_c_wallet_infra/` — each group built by a separate AI agent session
- **Setup:** copy `.env.example` to `.env`, fill in `HF_TOKEN` and `HF_DATASET_REPO`, then run:
  ```bash
  pip install -r requirements.txt
  python -m spacy download en_core_web_sm
  ```
- **Next step:** see `PRAMANA_ListA_Prompts.md` for the per-group build prompts (Steps 2-7)
