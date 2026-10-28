# Configuring Heretic

Heretic runs without a configuration file. To override defaults, create a file
named `config.toml` **in the directory from which you run Heretic**. You can
start with an empty file and add only the settings you want to change; the
remaining settings use their defaults. The model can be supplied on the command
line, for example:

```sh
heretic Qwen/Qwen3-4B-Instruct-2507
```

For the full list of settings and their defaults, see
[`config.default.toml`](../config.default.toml). Do not assume that a setting
from an older Heretic release is still supported.

## Using local prompt files

For a simple local dataset, create a UTF-8 text file with **one prompt per
line**. Blank lines are ignored. Paths can be absolute or relative to the
working directory; files do **not** need to live beside `config.toml`.

For example, create `prompts/bad-train.txt`, `prompts/good-train.txt`,
`prompts/bad-eval.txt`, and `prompts/good-eval.txt`. Then put the following
in `config.toml`:

```toml
n_trials = 10

[modifier.ARA.bad_prompts]
dataset = "./prompts/bad-train.txt"

[modifier.ARA.good_prompts]
dataset = "./prompts/good-train.txt"

[scorer.KeywordRate.prompts]
dataset = "./prompts/bad-eval.txt"

[scorer.KLDivergence.prompts]
dataset = "./prompts/good-eval.txt"
```

This example uses the default ARA modifier and the default KeywordRate and
KLDivergence scorers. For the alternative Abliteration modifier, change the
`modifiers` list as shown in `config.default.toml` and use
`[modifier.Abliteration.bad_prompts]` and
`[modifier.Abliteration.good_prompts]` instead.

The four prompt sets have different roles:

- **Bad training prompts**: Examples of behavior to reduce; used by the
  modifier to identify the undesirable direction.
- **Good training prompts**: Examples of behavior to preserve; used by the
  modifier when estimating directions.
- **Bad evaluation prompts**: Used by KeywordRate to measure how often
  configured refusal keywords appear in responses.
- **Good evaluation prompts**: Used by KLDivergence to measure deviation from
  the original model on benign inputs.

Keep training and evaluation examples separate where possible. For plain text
files, `column` is ignored and `split` is optional; for example,
`split = "[:100]"` selects the first 100 nonblank lines.

For a Hugging Face dataset ID or a local dataset directory, `split` and
`column` are required. For example:

```toml
[scorer.KeywordRate.prompts]
dataset = "mlabonne/harmful_behaviors"
split = "test[:100]"
column = "text"
```

For a dataset saved with `datasets.save_to_disk`, point `dataset` to the
saved **split** directory, not a DatasetDict containing multiple splits.
See the comments in `config.default.toml` for dataset configurations and
plugin-instance overrides.

## Optional benchmarks

Benchmarks are not required for the default refusal/KL-divergence optimization.
To report an additional metric using the Language Model Evaluation Harness,
add BenchmarkScore to the `scorers` list alongside the default scorers:

```toml
scorers = [
    { plugin = "heretic.scorers.keyword_rate.KeywordRate", optimization = "minimize" },
    { plugin = "heretic.scorers.kl_divergence.KLDivergence", optimization = "minimize" },
    { plugin = "heretic.scorers.benchmark_score.BenchmarkScore", optimization = "none" },
]

[scorer.BenchmarkScore]
score_name = "PIQA acc_norm"
task = "piqa"
metric = "acc_norm,none"
```

Here, `optimization = "none"` reports the benchmark without making it an
optimization objective. Benchmarks can add substantial evaluation time, so
start with the default scorers unless you need the extra measurement.

## Troubleshooting

If a configuration fails, first check that `config.toml` is in the process's
working directory, that paths point to existing files, and that the TOML syntax
is valid. On Windows, use forward slashes or TOML literal strings for paths
(e.g. `'C:\data\bad.txt'`); bare backslashes inside TOML double-quoted
strings are escape characters.

For help, open a [GitHub issue](https://github.com/p-e-w/heretic/issues) or
ask in the [Discord](https://discord.gg/gdXc48gSyT) or
[Matrix](https://matrix.to/#/#heretic:matrix.org) community. Include the
Heretic version, the command you ran, the error, and a minimal redacted
`config.toml`. Remove tokens, private prompts, and local personal paths.
