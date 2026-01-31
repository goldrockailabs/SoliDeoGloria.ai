#!/usr/bin/env python3
"""Full CAB evaluation using Anthropic Claude."""

import os
from anthropic import Anthropic
from cab_benchmark import CABEvaluator


def main():
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    def claude_model(prompt: str) -> str:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    evaluator = CABEvaluator(
        model_fn=claude_model,
        judge_client=client,
        judge_model="claude-3-opus-20240229",
        num_judges=3,
    )
    
    results = evaluator.evaluate(
        dataset_path="data/CAB_v2_Dataset_965.json",
        output_path="results/claude_sonnet_full.json",
    )
    print(f"CAB Score: {results['summary']['cab_score']:.3f}")


if __name__ == "__main__":
    main()
