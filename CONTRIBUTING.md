# Contributing

Keep changes focused on the supplied-question defaults, subject-independent workflow, illustration checks, and printable output. Read [the skill](skills/worksheet-maker/SKILL.md) before proposing a behavior change.

Describe the request that exposes the problem, the current behavior, and the expected result. Use invented questions and synthetic artwork. Do not upload completed student work, names, scores, private school material, credentials, or other sensitive details to public issues or pull requests. No private vulnerability-reporting channel is documented in this repository.

## Check a change

Run the repository check from its root with Python 3:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The validator checks the repository contract; the offline integration tests exercise update behavior with temporary Git repositories. Neither generates or certifies worksheets. For a workflow change, also describe the agent, tools, input, and output you actually exercised. Distinguish executed checks from source inspection.

For changes affecting PDF production, follow the skill's full checks: inspect every rendered page and picture, compare exact-mode text with the source, and verify the answer key against the final student PDF. Do not claim those checks passed unless they ran.

## Keep the package consistent

- Preserve the `help`, `--help`, and `-h` path: print usage and stop before other work.
- Preserve the pre-work update check for non-help invocations, and reload the skill after an update. Keep failure handling explicit and preserve local edits.
- Keep both plugin manifests consistent with the skill and with each other.
- Document new behavior in [usage.md](docs/usage.md); do not invent unsupported flags or installation commands.
- Update linked assets and relevant verification evidence when presentation files change.

The owner has not selected a license. Resolve contribution and redistribution permissions with the owner before submitting material whose terms are unclear.
