# PR 96 review: the paper's Word copy is in the repository (#95)

| Check | Result |
|---|---|
| Branch `docs/95-word-copy`, `Closes #95` | ok |
| Merge: the owner asked on November 12, 2026 for the Word copy to be in GitHub. Merging starts no run and publishes nothing outside this repository | ok |
| Test first: `paper/check_docx.py` was written before the build and failed twice, with no Word copy ("is missing") and against the copy made before this change ("does not say which text it was built from"); it passes on the file built here | ok |
| The Word copy's text is the paper's: compared as plain text with the copy already sent to the owner for version 14, which had been compared with the paper's Markdown (the only difference there was Figure 1's alternative text) | ok |
| The check is exact, not a guess from the words: the build writes the SHA-256 of the paper's Markdown into the file's description, and the check compares it with the Markdown in the repository. It also looks for the abstract's first sentence in the body | ok |
| CI runs the check on every change to `paper/`, in the workflow that already checks the paper against the competition's rules; it needs only the standard library | ok |
| The build fails at once, naming what it needs, when it is not told what the header should say; run here without it: exit 1 | ok |
| The file passes the Word schema validator; LibreOffice opens it as 8 pages with the header "Review copy · version 14 · November 12, 2026 · repository commit d6decb4", looked at in a render | ok |
| The competition's list of allowed file types is for the agent's bundle (`agent.yaml`, `prompts/`, `sub_agents/`, `configs/`, `eval_config.yaml`, `skills/`); `paper/` is outside it and already holds a PDF and images | ok |
| The paper's text, its PDF and `paper/sources.md` are not touched; `check_rules.py --check` exits 0 (15 rows pass); `docs/build_decks.py --check` exits 0; the tag `paper-v14` and the branch `release/paper-track` stay at `d6decb4` | ok |
| No secrets, real data or organisation names | ok |

Nothing blocking.

## Notes
- From now on a change to the paper's text needs the Word copy built again, or CI fails. That is the point of the
  check, and it is one more command beside the PDF's.
- The Word file is not byte-for-byte the one sent to the owner earlier: its description now holds the hash. The
  text, layout and header are the same.
- The release `paper-v14` has the PDF and not the Word copy: the Word copy came after the tag. It is on `main`.
