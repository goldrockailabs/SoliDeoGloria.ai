# CAB v2.0 Methodology

## Overview

The Christian AI Benchmark (CAB) evaluates AI systems on their ability to engage appropriately with Christian theology, pastoral care, ethics, and denominational diversity.

## Design Principles

### 1. Comprehensive Coverage
- 10 theological dimensions covering the breadth of Christian knowledge
- 10 denominational traditions ensuring fair representation
- Balance of factual knowledge and applied wisdom

### 2. Dual Scoring Modes
- **Objective**: Tests factual knowledge with verifiable answers
- **Subjective**: Tests pastoral wisdom and nuanced reasoning

### 3. Anti-Gaming Measures
- Randomized answer positions prevent pattern exploitation
- Geometric mean aggregation prevents dimension compensation
- Multiple judges reduce scoring variance

## Scoring Methodology

### Objective Questions
- Multiple choice (A/B/C/D)
- Score = 1.0 if correct, 0.0 if incorrect
- Answer positions randomized per administration

### Subjective Questions
- 3-judge LLM panel
- 1-5 Likert scale with behavioral anchors
- Median score used for robustness
- Normalized to 0-1 scale

### Aggregation
1. Within-dimension: Geometric mean of question scores
2. CAB Score: Geometric mean across all dimension scores

Geometric mean ensures models cannot compensate for weakness in one area by excelling in another.

## Validation
- 30% expert panel review
- Krippendorff's alpha >= 0.80
- Regular bias audits
