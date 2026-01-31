# Christian AI Benchmark (CAB) v2.0

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Questions](https://img.shields.io/badge/Questions-991-blue.svg)]()
[![Dimensions](https://img.shields.io/badge/Dimensions-10-green.svg)]()
[![Traditions](https://img.shields.io/badge/Traditions-10-orange.svg)]()

A comprehensive framework for evaluating AI alignment with Christian faith across theological dimensions and denominational traditions.

## Overview

CAB v2.0 is a rigorous benchmark designed to assess how well AI systems understand and appropriately engage with Christian theology, pastoral care, ethics, and denominational diversity. Unlike general religious knowledge tests, CAB evaluates nuanced theological reasoning, pastoral sensitivity, and appropriate boundary recognition.

## Key Features

- **991 Unique Questions** - 100% unique, no duplicates
- **10 Theological Dimensions** - Comprehensive coverage of Christian knowledge domains
- **10 Denominational Traditions** - Fair representation across Christian traditions
- **Dual Scoring Modes** - Objective (multiple choice) and subjective (scenario-based)
- **Scientific Methodology** - Geometric mean aggregation, LLM judge panels, human validation

## Dimensions

| Dimension | Questions | Description |
|-----------|-----------|-------------|
| Biblical Literacy | 121 | Scripture knowledge, hermeneutics, exegesis |
| Systematic Theology | 123 | Doctrine, Christology, soteriology, eschatology |
| Pastoral Care | 189 | Counseling scenarios, grief, crisis intervention |
| Christian Ethics | 110 | Moral reasoning, bioethics, social ethics |
| Church History | 91 | Historical knowledge, movements, figures |
| Worship & Sacraments | 90 | Liturgy, sacramental theology, worship practice |
| Apologetics | 79 | Defending faith, engaging objections |
| Spiritual Formation | 77 | Disciplines, growth, sanctification |
| Denominational Awareness | 61 | Understanding other traditions fairly |
| Boundary Respect | 50 | Recognizing AI limitations, appropriate referrals |

## Traditions

- **Cross-Tradition** (480 questions) - Shared Christian beliefs
- **Catholic** (75) | **Orthodox** (68) | **Reformed** (61)
- **Lutheran** (57) | **Baptist** (53) | **Methodist** (51)
- **Pentecostal** (50) | **Evangelical** (49) | **Anglican** (47)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/GoldRockAI/cab-benchmark.git
cd cab-benchmark

# Install dependencies
pip install -r requirements.txt

# Run evaluation on your model
python evaluation/evaluate.py --model your-model --output results/
```

## Dataset Structure

```json
{
  "id": "CAB-0001",
  "scoring_mode": "objective|subjective",
  "dimension": "Biblical Literacy",
  "tradition": "Cross-Tradition",
  "difficulty": "L1|L2|L3",
  "question": "...",           // for objective
  "options": ["A)...", ...],   // for objective
  "correct_answer": "B",       // for objective
  "scenario": "...",           // for subjective
  "rubric_focus": "..."        // for subjective
}
```

## Scoring Methodology

### Objective Questions (75 questions)
- Multiple choice with randomized answer positions
- Binary scoring (correct/incorrect)
- Prevents pattern exploitation

### Subjective Questions (916 questions)
- Scenario-based requiring nuanced responses
- Evaluated by 3-judge LLM panel
- 1-5 Likert scale with behavioral anchors
- Median score used for robustness

### Aggregation
- **Geometric mean** across dimensions prevents compensation
- A model cannot hide weaknesses by excelling elsewhere
- Dimension scores weighted equally

## Evaluation

```python
from cab_benchmark import CABEvaluator

evaluator = CABEvaluator(
    model="your-model-name",
    judge_model="claude-3-opus",  # or gpt-4
    num_judges=3
)

results = evaluator.evaluate("data/CAB_v2_Dataset_965.json")
print(results.summary())
```

## Results Format

```json
{
  "model": "model-name",
  "timestamp": "2026-01-31T...",
  "overall_score": 0.73,
  "dimension_scores": {
    "Biblical Literacy": 0.81,
    "Pastoral Care": 0.69,
    ...
  },
  "tradition_scores": {...},
  "detailed_results": [...]
}
```

## Citation

```bibtex
@misc{cab2026,
  title={Christian AI Benchmark (CAB): A Framework for Evaluating AI Alignment with Christian Faith},
  author={GoldRock AI},
  year={2026},
  publisher={Soli Deo Gloria Research Initiative},
  url={https://github.com/GoldRockAI/cab-benchmark}
}
```

## License

This dataset is released under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

You are free to:
- **Share** — copy and redistribute the material
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — Give appropriate credit
- **ShareAlike** — Distribute contributions under the same license

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Contact

- **Website**: [SoliDeoGloria.ai](https://SoliDeoGloria.ai)
- **Publisher**: Eldest AI LLC dba GoldRock AI
- **Issues**: GitHub Issues

## Acknowledgments

Developed as part of the Soli Deo Gloria Research Initiative to advance responsible AI development that respects and understands religious faith.
