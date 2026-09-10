# Security Model

## Threat Vectors Analyzed
1. **List-A / List-B Leakage (Fixed):** Handled by `ai-ml/shared/redaction.py`.
2. **Clone / Hub Attacks (Fixed):** Adversaries pasting another's PGP key. Handled by the $k \ge 2$ refusal and Rarity ($	au$) scaling.
3. **Prompt Injection (Mitigated):** Handled by completely removing the LLM from the scoring loop.
4. **Tarbombs (Vulnerable - DEMO ONLY):** Archive extraction uses standard `tarfile`. Do not ingest untrusted hostile archives in production without patching with `data_filter`.
5. **API Auth (Missing - DEMO ONLY):** FastAPI Gateway currently lacks OAuth2 / API Key authentication.
