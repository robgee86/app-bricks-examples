---
title: Add the LLM brick
summary: Wire the LargeLanguageModel brick into app.yaml and main.py — configured, not yet used.
patches:
  - path: ../assets/4.1_add-llm.patch
    label: Add arduino:llm to app.yaml; instantiate LargeLanguageModel
attachments:
  - path: ../assets/4.1_add-llm.zip
    label: rss-reader after step 4.1
---

App Lab ships a `LargeLanguageModel` brick — a clean wrapper around a local llama.cpp-backed model running on the board. We're going to use it to summarize articles on demand. But first: install and configure it, without changing any behavior yet. That keeps the setup step easy to verify on its own.

Two surface-level changes:

- **`app.yaml`** picks up an `arduino:llm:` brick with a `variables:` block. We size the context window (`X_LLAMA_ARG_CTX_SIZE` / `GENAI_CONTEXT_CAPPING` both at 64 K) so long-ish articles fit in a single prompt without truncation.
- **`main.py`** imports `LargeLanguageModel`, instantiates one with the model id (`llamacpp:gemma-4-E2B-it-Q4_0_PURE`) and a `system_prompt` that tells it to "respond with a few short markdown sentences. No preamble." We also call `llm.with_memory(0)` — we don't want conversational memory between article summaries; each request stands alone.

That's it. The `llm` object exists but nothing calls it. Step 4.2 wires the actual summarization.

> The first run after this change will pull the model — that can take a minute and a few hundred MB. Subsequent restarts are fast.

**Checkpoint:** the app starts without errors; the App Lab Logs show the LLM brick coming up. The reader looks unchanged.
