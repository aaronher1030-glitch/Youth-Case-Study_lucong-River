# Task 1/1A Fix Round 2 Brief

Work from: `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR`

## Context

The scoped re-review closed both Important findings. One Minor issue remains: `test_synthetic_prior_uses_equal_weights_deterministically` infers the selected connection level from 200 Bernoulli observations per scenario, so it still passes when connection weights are changed to `(0.21, 0.20, 0.19, 0.20, 0.20)`.

Production behavior is already correct. This round changes only the test guard and must mutation-prove that guard.

## Required change

Replace the noisy statistical inference test with a deterministic test that observes the real NumPy RNG calls while still executing the real generator and real NumPy methods.

Recommended implementation:

- Add a small recording proxy in the test that delegates `integers`, `triangular`, `random`, and `choice` to a real `numpy.random.default_rng(seed)` instance.
- Record each `choice` call's candidate sequence, positional arguments, and keyword arguments, then delegate to the real RNG.
- Monkeypatch only `river_model.synthetic.np.random.default_rng` for the duration of one test.
- Generate one small census and assert exactly two `choice` calls: first for `spec.connection_levels`, second for `spec.barangays`.
- Assert neither call supplies positional or keyword probability weights. NumPy's default `choice` behavior is then uniform by contract.
- Keep the test deterministic and do not replace generated values with canned outputs.

A different deterministic design is acceptable if it directly detects the stated modest unequal-weight mutation, tests the public generator, and does not depend on fragile hard-coded random counts.

## Mutation proof required

1. Run the new test against current correct production code and confirm it passes.
2. Temporarily mutate only the connection selection to pass `p=(0.21, 0.20, 0.19, 0.20, 0.20)` to `rng.choice`.
3. Run the focused test and capture the expected failure.
4. Restore the correct production code immediately.
5. Rerun the focused test and confirm it passes.
6. Run the full current suite once and self-review that no mutation remains.

Do not initialize Git or create commits. Do not dispatch subagents.

## Report

Append `## Fix round 2` to:
`C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-1-report.md`

Include the baseline pass, mutation command/output, restored pass, full-suite result, files changed, and confirmation that production code is unchanged. Return only status, one-line test summary, concerns, and report path.
