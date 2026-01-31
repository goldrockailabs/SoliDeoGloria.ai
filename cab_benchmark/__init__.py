"""
Christian AI Benchmark (CAB) v2.0

A comprehensive framework for evaluating AI alignment with Christian faith.
"""

__version__ = "2.0.0"
__author__ = "GoldRock AI"

from .evaluator import CABEvaluator
from .loader import load_dataset
from .scorer import ObjectiveScorer, SubjectiveScorer
from .aggregator import aggregate_scores

__all__ = [
    "CABEvaluator",
    "load_dataset", 
    "ObjectiveScorer",
    "SubjectiveScorer",
    "aggregate_scores",
]
