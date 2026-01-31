"""Dataset loading and validation utilities."""

import json
from pathlib import Path
from typing import Dict, List, Optional, Union
import jsonschema

QUESTION_SCHEMA = {
    "type": "object",
    "required": ["id", "scoring_mode", "dimension", "tradition", "difficulty"],
    "properties": {
        "id": {"type": "string", "pattern": "^CAB-\\d{4}$"},
        "scoring_mode": {"enum": ["objective", "subjective"]},
        "dimension": {"type": "string"},
        "tradition": {"type": "string"},
        "difficulty": {"enum": ["L1", "L2", "L3"]},
        "question": {"type": "string"},
        "options": {"type": "array", "items": {"type": "string"}},
        "correct_answer": {"type": "string"},
        "scenario": {"type": "string"},
        "rubric_focus": {"type": "string"},
    }
}

DIMENSIONS = [
    "Biblical Literacy",
    "Systematic Theology", 
    "Pastoral Care",
    "Christian Ethics",
    "Church History",
    "Worship & Sacraments",
    "Apologetics",
    "Spiritual Formation",
    "Denominational Awareness",
    "Boundary Respect",
]

TRADITIONS = [
    "Cross-Tradition",
    "Catholic",
    "Orthodox",
    "Reformed",
    "Lutheran",
    "Baptist",
    "Methodist",
    "Anglican",
    "Pentecostal",
    "Evangelical",
]


def load_dataset(path: Union[str, Path]) -> Dict:
    """Load and validate CAB dataset from JSON file."""
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Basic validation
    if "questions" not in data:
        raise ValueError("Dataset missing 'questions' field")
    
    questions = data["questions"]
    
    # Validate each question
    errors = []
    for i, q in enumerate(questions):
        try:
            jsonschema.validate(q, QUESTION_SCHEMA)
            
            # Check dimension
            if q["dimension"] not in DIMENSIONS:
                errors.append(f"Q{i}: Invalid dimension '{q['dimension']}'")
            
            # Check tradition
            if q["tradition"] not in TRADITIONS:
                errors.append(f"Q{i}: Invalid tradition '{q['tradition']}'")
            
            # Check objective questions have required fields
            if q["scoring_mode"] == "objective":
                if "question" not in q or "options" not in q or "correct_answer" not in q:
                    errors.append(f"Q{i}: Objective question missing required fields")
            
            # Check subjective questions have required fields
            if q["scoring_mode"] == "subjective":
                if "scenario" not in q or "rubric_focus" not in q:
                    errors.append(f"Q{i}: Subjective question missing required fields")
                    
        except jsonschema.ValidationError as e:
            errors.append(f"Q{i}: {e.message}")
    
    if errors:
        raise ValueError(f"Dataset validation errors:\n" + "\n".join(errors[:10]))
    
    return data


def filter_questions(
    questions: List[Dict],
    dimensions: Optional[List[str]] = None,
    traditions: Optional[List[str]] = None,
    scoring_mode: Optional[str] = None,
    difficulty: Optional[List[str]] = None,
) -> List[Dict]:
    """Filter questions by criteria."""
    filtered = questions
    
    if dimensions:
        filtered = [q for q in filtered if q["dimension"] in dimensions]
    
    if traditions:
        filtered = [q for q in filtered if q["tradition"] in traditions]
    
    if scoring_mode:
        filtered = [q for q in filtered if q["scoring_mode"] == scoring_mode]
    
    if difficulty:
        filtered = [q for q in filtered if q["difficulty"] in difficulty]
    
    return filtered


def get_statistics(data: Dict) -> Dict:
    """Get dataset statistics."""
    questions = data["questions"]
    
    stats = {
        "total": len(questions),
        "by_dimension": {},
        "by_tradition": {},
        "by_mode": {"objective": 0, "subjective": 0},
        "by_difficulty": {"L1": 0, "L2": 0, "L3": 0},
    }
    
    for q in questions:
        # By dimension
        dim = q["dimension"]
        stats["by_dimension"][dim] = stats["by_dimension"].get(dim, 0) + 1
        
        # By tradition
        trad = q["tradition"]
        stats["by_tradition"][trad] = stats["by_tradition"].get(trad, 0) + 1
        
        # By mode
        stats["by_mode"][q["scoring_mode"]] += 1
        
        # By difficulty
        stats["by_difficulty"][q["difficulty"]] += 1
    
    return stats
