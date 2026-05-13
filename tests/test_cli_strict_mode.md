# test_cli_strict_mode.py

## Purpose

Tests strict-mode CLI exit code behavior.

---

## Tested File

```text
scripts/run_csv_pipeline.py
```

---

## Covered Behavior

- non-strict validation failures return exit code `0`
- strict validation failures return exit code `2`
- execution errors return exit code `1`
- output CSV is still written when strict mode reports policy failure

---

## Run Tests

```bash
python -m pytest tests/test_cli_strict_mode.py
```

---

## Exit Codes

```text
0 = successful execution
1 = execution error
2 = strict policy failure
```
