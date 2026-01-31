#!/usr/bin/env python3
"""Basic example of running CAB evaluation with objective questions only."""

from cab_benchmark import CABEvaluator


def my_model(prompt: str) -> str:
    """Replace with your model. This returns random for demo."""
    import random
    return random.choice(["A", "B", "C", "D"])


def main():
    evaluator = CABEvaluator(model_fn=my_model, verbose=True)
    results = evaluator.evaluate(
        dataset_path="data/CAB_v2_Dataset_965.json",
        scoring_mode="objective",
        output_path="results/objective_results.json",
    )
    print(f"\nScore: {results['summary']['overall_score']:.3f}")


if __name__ == "__main__":
    main()
