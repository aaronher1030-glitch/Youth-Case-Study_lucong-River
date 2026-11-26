# Research Workflow

Use this reference for experiment planning, idea generation, debugging a stuck research project, or designing a first research sprint.

## Do Not Only Think. Play.

Avoid generating ideas only by sitting and thinking. In crowded AI fields, ideas invented entirely in the head are often already explored, too obvious, or detached from the system's actual behavior.

Start by playing with the system:

- Reproduce a baseline.
- Change one assumption.
- Visualize failures.
- Probe data and representations.
- Run small ablations.
- Inspect weird cases manually.

Treat research like a game or toy during the early phase. The point is not sloppiness; the point is contact with reality.

## Search For Gradients

The real idea often comes from the gradient produced by exploration. A negative movement can be useful because its opposite direction may be positive. The most worrying result is no movement at all.

After each experiment, classify the signal:

- **Positive**: improves target behavior or reveals a promising mechanism.
- **Negative but informative**: hurts for an interpretable reason.
- **Surprising**: violates the prediction and deserves inspection.
- **Flat**: changes little and may indicate the experiment was not diagnostic.

Flat results are not automatically useless, but repeated flatness means the project needs sharper probes.

## Predict Before Running

Every experiment should have a prediction before it runs. This turns experiments into learning rather than lottery tickets.

Minimum experiment log:

```text
Experiment:
Hypothesis:
Prediction:
Setup:
Expected failure mode:
Observed result:
Signal type:
Interpretation:
Next decision:
```

If the prediction is correct, continue the line. If it is wrong, inspect the surprise. Surprise is often where the project becomes yours.

## Respect Nonlinearity

Good research often looks unproductive for a long time, then converges quickly after the right signal appears. Do not force a linear project narrative during exploration.

Use this pattern:

1. Reserve an explicit exploration phase.
2. Run broad small probes before locking the claim.
3. Keep an experiment ledger.
4. Let strong evidence change the idea.
5. Build the final narrative only after the decision path is clear.

## Pivot Rules

Pivot when:

- The problem definition is weak.
- Experiments repeatedly produce flat signal.
- The only path forward is more compute without deeper understanding.
- The interesting observation is adjacent to the original idea.
- The strongest story is no longer the first story.

Do not pivot merely because the first results are negative. Negative signal can be a direction.

## Sprint Template

For a 1-2 week research sprint, propose:

```text
Question:
Baseline to reproduce:
Three probes:
Prediction for each probe:
One representation or failure visualization:
Stop condition:
Pivot condition:
Story candidate if signal appears:
```
