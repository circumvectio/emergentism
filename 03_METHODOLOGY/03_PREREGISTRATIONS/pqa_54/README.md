# PQA-54 reference harness

This standard-library package implements the offline reference contracts for
PQA-54 protocol `0.1.0`. It contains the public 9×6 denominator, schemas,
synthetic fixtures, recorded responses, vector scoring, public projection and
freeze custody.

```text
python3 -B run_pqa.py validate prompts/questions.json
python3 -B run_pqa.py generate --check
python3 -B run_pqa.py run --dry-run --arm NEUTRAL
python3 -B run_pqa.py score --check
python3 -B run_pqa.py freeze --check
python3 -B -m unittest discover -s tests -p 'test_*.py'
```

Live network use is intentionally unavailable in this reference release. EUB-1
is referenced by hash only and remains frozen. Synthetic fixtures do not enter
the public benchmark counts.
