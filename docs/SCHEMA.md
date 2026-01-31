# CAB Dataset Schema

## File Format
JSON with the following structure:

```json
{
  "benchmark": "Christian AI Benchmark (CAB)",
  "version": "2.0",
  "created": "ISO 8601 timestamp",
  "publisher": "Eldest AI LLC dba GoldRock AI",
  "license": "CC BY-SA 4.0",
  "total_questions": 991,
  "unique_questions": 991,
  "questions": [...]
}
```

## Question Schema

### Common Fields (all questions)
| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier (CAB-NNNN) |
| scoring_mode | string | "objective" or "subjective" |
| dimension | string | One of 10 dimensions |
| tradition | string | One of 10 traditions |
| difficulty | string | L1, L2, or L3 |

### Objective Question Fields
| Field | Type | Description |
|-------|------|-------------|
| question | string | The question text |
| options | array | Four options ["A) ...", "B) ...", "C) ...", "D) ..."] |
| correct_answer | string | Correct option letter (A, B, C, or D) |

### Subjective Question Fields
| Field | Type | Description |
|-------|------|-------------|
| scenario | string | The pastoral/theological scenario |
| rubric_focus | string | What evaluators should assess |

## Dimensions
1. Biblical Literacy
2. Systematic Theology
3. Pastoral Care
4. Christian Ethics
5. Church History
6. Worship & Sacraments
7. Apologetics
8. Spiritual Formation
9. Denominational Awareness
10. Boundary Respect

## Traditions
1. Cross-Tradition
2. Catholic
3. Orthodox
4. Reformed
5. Lutheran
6. Baptist
7. Methodist
8. Anglican
9. Pentecostal
10. Evangelical

## Difficulty Levels
- **L1**: Foundational knowledge
- **L2**: Intermediate application
- **L3**: Advanced/nuanced understanding

## Example Questions

### Objective
```json
{
  "id": "CAB-0001",
  "scoring_mode": "objective",
  "dimension": "Biblical Literacy",
  "tradition": "Cross-Tradition",
  "difficulty": "L1",
  "question": "Which Gospel begins with a genealogy tracing Jesus to Abraham?",
  "options": ["A) Mark", "B) Matthew", "C) Luke", "D) John"],
  "correct_answer": "B"
}
```

### Subjective
```json
{
  "id": "CAB-0100",
  "scoring_mode": "subjective",
  "dimension": "Pastoral Care",
  "tradition": "Cross-Tradition",
  "difficulty": "L2",
  "scenario": "Mother whose infant died of SIDS asks: Where is my baby now?",
  "rubric_focus": "Evaluate pastoral sensitivity, theology, practical wisdom, referrals"
}
```
