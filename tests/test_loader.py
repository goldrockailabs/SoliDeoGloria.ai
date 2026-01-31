"""Tests for data loader."""
import pytest
from cab_benchmark.loader import load_dataset, get_statistics, filter_questions

def test_load_dataset():
    data = load_dataset("data/CAB_v2_Dataset_965.json")
    assert "questions" in data
    assert len(data["questions"]) == 991

def test_get_statistics():
    data = load_dataset("data/CAB_v2_Dataset_965.json")
    stats = get_statistics(data)
    assert stats["total"] == 991
    assert len(stats["by_dimension"]) == 10
    assert len(stats["by_tradition"]) == 10

def test_filter_questions():
    data = load_dataset("data/CAB_v2_Dataset_965.json")
    filtered = filter_questions(data["questions"], scoring_mode="objective")
    assert all(q["scoring_mode"] == "objective" for q in filtered)
