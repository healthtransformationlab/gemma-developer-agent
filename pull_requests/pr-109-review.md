# PR 109 review: serve the copyfix LoRA so exact-text edits stop failing (#108)

| Check | Result |
|---|---|
| Branch `feat/108-copyfix-adapter`, `Closes #108`, issue written before the first commit with its four parts | ok |
| Test first: the two new tests fail on main (no `adapter:` line, no files) and pass here; 11 pass | ok |
| Files are the published ones: SHA-256 of `adapter_config.json` `3786855f…` and `adapter_model.safetensors` `9ce83a7c…`, as the dataset's description lists them, checked by test | ok |
| The harness's contract (HARNESS_README 3.4): `adapters/<name>/` with `adapter_config.json` and `adapter_model.safetensors`; name matches `[A-Za-z0-9][A-Za-z0-9._-]*`; `adapter: <name>` on an `LlmAgent`; rank at most `max_lora_rank` 128 (the adapter's `r` is 128) | ok |
| One base model across agents (`gemma-4-e4b-it-qat-w4a16-ct` unchanged) | ok |
| Allowed extensions (`.json`, `.safetensors`) and size (3.3 MB of the 3 GiB limit); `adapters` added to the test's submission list | ok |
| Licence: Apache-2.0 adapter derived from an Apache-2.0 tensor; `NOTICE` names author, licence, source and that the files are unmodified | ok |
| Nothing else in the submission changes from main `76bc6d6` (prompt, sampling, budgets) | ok: diff is NOTICE, the adapter, two `adapter:` lines, tests |
| Secrets, real data, claims | none; the PR claims no score change |
| Compiled files | none committed |

## Findings

- Important, not blocking: no GPU run has loaded this adapter in our harness (the weekly Kaggle hours are spent). The
  evidence that it loads in the competition's stack is another team's leaderboard entries with it (0.10 and 0.05,
  write-up 92175) and the author's vLLM 0.19.1 check. If it fails to load, the November 16 entry scores 0; the next
  day's entry can drop it.
- Minor: the analyzer is read-only, so the adapter matters mostly for the coder's edits. Serving it on both keeps one
  model behaviour across the bundle, as the measured bundles did.
- The reported gain is mixed (0.10 then 0.05 for the same bundle), within the leaderboard's noise of about 1.6 of 58
  tasks. The mechanism (copy failures 15 of 18 → 1 of 18, and our 44% failed edits) is the stronger evidence.

## Verdict

Nothing blocking. Merge when CI is green; it starts no run and publishes nothing. The entry it feeds is a separate,
owner-approved step.
