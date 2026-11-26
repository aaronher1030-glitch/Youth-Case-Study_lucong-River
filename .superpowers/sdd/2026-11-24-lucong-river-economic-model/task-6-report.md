## Task 6 implementation

Status: complete. Implemented joint seeded uncertainty, strict invalid-draw withholding, common random numbers, deterministic robust-selection tie-breaking, and one-at-a-time sensitivity.

### TDD RED

Command:

```text
python -m pytest tests/test_uncertainty.py -v
```

Output:

```text
============================= test session starts =============================
platform win32 -- Python 3.13.6, pytest-9.0.3, pluggy-1.6.0 -- C:\Program Files\Python313\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR
plugins: anyio-4.13.0
collecting ... collected 0 items / 1 error

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_uncertainty.py ______________________
ImportError while importing test module 'C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\tests\test_uncertainty.py'.
Traceback (most recent call last):
  File "C:\Program Files\Python313\Lib\importlib\__init__.py", line 1010, in _find_and_load
  File "C:\Program Files\Python313\Lib\importlib\__init__.py", line 688, in _load_unlocked
  File "C:\Program Files\Python313\Lib\importlib\__init__.py", line 884, in _load
  File "C:\Program Files\Python313\Lib\importlib\__init__.py", line 1019, in _bootstrap
  File "C:\Program Files\Python313\Lib\importlib\__init__.py", line 1072, in _load_unlocked
  File "C:\Program Files\Python313\Lib\importlib\__init__.py", line 1042, in _exec
  File "C:\Program Files\Python313\Lib\importlib\__init__.py", line 1173, in exec_module
  File "<frozen importlib._bootstrap>", line 684, in _get
  File "<frozen importlib._bootstrap>", line 703, in _get
  File "<frozen importlib._bootstrap>", line 414, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1475, in _find_and_load
--> File "C:\Program Files\Python313\Lib\importlib\__init__.py", line 1266, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 696, in _load_unlocked
  File "<frozen importlib._bootstrap>", line 884, in _load_unlocked
  File "<frozen importlib._bootstrap>", line 988, in _load_module_shims
  File "<frozen importlib._bootstrap>", line 1148, in load_unlocked
tests\test_uncertainty.py:10: in <module>
    from river_model import uncertainty as uncertainty_module
E   ImportError: cannot import name 'uncertainty' from 'river_model' (C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\river_model\__init__.py)

=========================== short test summary info ===========================
ERROR tests/test_uncertainty.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !==========================
1 error in 1.17s
```

The failure was the expected missing-module import failure before production code was written.

### Focused GREEN

Command:

```text
python -m pytest tests/test_uncertainty.py -q
```

Output:

```text
........................................................................ [ 36%]
........................................................................ [ 73%]
.................................................... [100%]
196 passed in 1.41s
```

The focused suite was also run in verbose mode after GREEN; all 196 tests passed.

### Required 20,000-draw smoke

Exact command:

```text
python -c "from pathlib import Path; from dataclasses import replace; from river_model.inputs import Params,load_census; from river_model.design import enumerate_designs; from river_model.uncertainty import UncertaintySpec,run_uncertainty,select_robust_design; p=replace(Params(),land_available_ha=20.0); s=load_census(Path('tests/fixtures/census.csv')); e=enumerate_designs(p,s); r=run_uncertainty(p,s,e,UncertaintySpec()); x=select_robust_design(p,e,r); print('selected', x.design if x else None, 'probability', r[x.design].p_target if x else None)"
```

Output:

```text
selected None probability None
```

Follow-up inspection found 8 deterministic-feasible designs, 8 uncertainty results, no withheld results, and `p_target=0.00025` for every feasible design. Selection correctly returned `None` because none met the unchanged 0.80 threshold.

### Full suite

Command:

```text
python -m pytest -q
```

Output:

```text
........................................................................ [  9%]
........................................................................ [ 19%]
........................................................................ [ 28%]
........................................................................ [ 38%]
........................................................................ [ 47%]
........................................................................ [ 57%]
........................................................................ [ 66%]
........................................................................ [ 76%]
........................................................................ [ 85%]
........................................................................ [ 95%]
...................................                                     [100%]
755 passed in 16.01s
```

### Files changed

- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\river_model\uncertainty.py` (new)
- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\tests\test_uncertainty.py` (new)
- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-6-report.md` (new verification report)

A filesystem comparison against `review/task-6/base/` confirmed that the only implementation/test additions are `river_model/uncertainty.py` and `tests/test_uncertainty.py`; no existing source or test file changed.

### Self-review

- Required dataclass defaults and all six public function signatures were inspected and match the brief, including seed 2026, 20,000 production draws, and the 0.80 target threshold.
- Draw generation uses `np.random.default_rng(seed)`, log-uniform `q`/`e`, and NumPy triangular distributions. Zero-width triangular sensitivity settings are represented by their degenerate constant limit while consuming the same random-stream width.
- Specs, counts, seeds, concentration parameters, and draw mappings are validated before evaluation. There are no fallback values.
- Monte Carlo calculations are vectorized. Any nonfinite or physically invalid draw, including any strict `r > 1.0`, withholds all probability and percentile claims, retains `invalid_fraction`, reports `valid_draws=0`, and returns an empty float endpoint array.
- Head counts use only selected, confirmed eligible shed IDs. Missing, unknown, unconfirmed, and duplicate selected IDs raise rather than being silently dropped.
- `run_uncertainty` creates one shared draw object for all deterministic-feasible designs. Robust selection rejects missing, withheld, below-threshold, and infeasible candidates and uses `(eac, cash_12m, -shed_count)` ordering.
- One-at-a-time sensitivity produces exactly 14 low/high rows with the required keys, preserves the seed, detects controlled decision flips, and leaves probability/decision unchanged for cost-only variation while changing median EAC.
- Tests independently cover exact NumPy draw streams and distribution statistics, strict boundary invalidity, controlled percentile recalculation, design-specific heads, common random numbers, all selection tie-breaks, sensitivity behavior, and the 20,000-draw smoke case.
- No Git repository, commit, worktree, or subagent was used.

Concern: the default fixture smoke run yields no robust selection because the best feasible target probability is 0.00025, far below 0.80. This is a model outcome, not an invalid-draw withholding case; the threshold was not lowered and no probability claim was fabricated.
