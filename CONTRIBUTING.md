# Contributing to CAB

Thank you for your interest in contributing to the Christian AI Benchmark!

## Ways to Contribute

### 1. Question Contributions
- Submit new questions via Pull Request
- Ensure questions meet quality standards (see below)
- Include appropriate metadata (dimension, tradition, difficulty)

### 2. Bug Reports
- Report issues with existing questions
- Identify theological inaccuracies
- Flag potentially biased or unfair questions

### 3. Evaluation Improvements
- Improve scoring rubrics
- Enhance evaluation scripts
- Add support for new model APIs

### 4. Documentation
- Improve README and docs
- Add usage examples
- Translate documentation

## Question Quality Standards

### Objective Questions
- Clear, unambiguous wording
- One definitively correct answer
- Plausible distractors
- Appropriate difficulty level
- Theologically accurate

### Subjective Questions
- Realistic pastoral/theological scenarios
- No single "correct" answer
- Tests nuanced reasoning
- Clear rubric focus
- Pastorally sensitive

## Theological Guidelines

1. **Accuracy**: Questions must reflect genuine theological positions
2. **Fairness**: Represent traditions charitably and accurately
3. **Balance**: Avoid privileging one tradition over others
4. **Sensitivity**: Handle pastoral topics with appropriate care
5. **Boundaries**: Respect what AI should/shouldn't do

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-questions`)
3. Make your changes
4. Run validation (`python scripts/validate.py`)
5. Submit PR with clear description
6. Address review feedback

## Question Format

```json
{
  "scoring_mode": "objective|subjective",
  "dimension": "One of 10 dimensions",
  "tradition": "One of 10 traditions",
  "difficulty": "L1|L2|L3",
  "question": "For objective",
  "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "correct_answer": "B",
  "scenario": "For subjective",
  "rubric_focus": "What to evaluate"
}
```

## Code of Conduct

Please review our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Questions?

Open an issue or contact us at the repository discussions.
