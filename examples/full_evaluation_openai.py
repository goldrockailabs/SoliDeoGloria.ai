#!/usr/bin/env python3
"""Full CAB evaluation using OpenAI GPT."""

import os
from openai import OpenAI
from cab_benchmark import CABEvaluator


def main():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    def gpt_model(prompt: str) -> str:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    evaluator = CABEvaluator(
        model_fn=gpt_model,
        judge_client=client,
        judge_model="gpt-4-turbo",
        num_judges=3,
    )
    
    results = evaluator.evaluate(
        dataset_path="data/CAB_v2_Dataset_965.json",
        output_path="results/gpt4_full.json",
    )
    print(f"CAB Score: {results['summary']['cab_score']:.3f}")


if __name__ == "__main__":
    main()
