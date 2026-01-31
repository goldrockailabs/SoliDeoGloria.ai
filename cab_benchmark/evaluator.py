"""Main evaluation orchestration."""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable
from tqdm import tqdm

from .loader import load_dataset, filter_questions
from .scorer import ObjectiveScorer, SubjectiveScorer
from .aggregator import aggregate_scores


class CABEvaluator:
    """
    Main evaluator class for running CAB benchmark.
    
    Example usage:
        evaluator = CABEvaluator(
            model_fn=my_model_function,
            judge_client=anthropic_client,
            judge_model="claude-3-opus-20240229"
        )
        results = evaluator.evaluate("data/CAB_v2_Dataset_965.json")
    """
    
    def __init__(
        self,
        model_fn: Callable[[str], str],
        judge_client=None,
        judge_model: str = "claude-3-opus-20240229",
        num_judges: int = 3,
        randomize_options: bool = True,
        verbose: bool = True,
    ):
        """
        Initialize evaluator.
        
        Args:
            model_fn: Function that takes a prompt and returns model response
            judge_client: API client for LLM judge (Anthropic or OpenAI)
            judge_model: Model to use for judging subjective questions
            num_judges: Number of judges for subjective questions
            randomize_options: Whether to randomize multiple choice options
            verbose: Whether to show progress
        """
        self.model_fn = model_fn
        self.judge_client = judge_client
        self.judge_model = judge_model
        self.num_judges = num_judges
        self.randomize_options = randomize_options
        self.verbose = verbose
        
        self.objective_scorer = ObjectiveScorer(randomize_options=randomize_options)
        self.subjective_scorer = None
        
        if judge_client:
            # Detect client type
            client_type = type(judge_client).__module__
            if "anthropic" in client_type:
                from .scorer import AnthropicSubjectiveScorer
                self.subjective_scorer = AnthropicSubjectiveScorer(
                    judge_client=judge_client,
                    judge_model=judge_model,
                    num_judges=num_judges,
                )
            elif "openai" in client_type:
                from .scorer import OpenAISubjectiveScorer
                self.subjective_scorer = OpenAISubjectiveScorer(
                    judge_client=judge_client,
                    judge_model=judge_model,
                    num_judges=num_judges,
                )
    
    def evaluate(
        self,
        dataset_path: str,
        dimensions: Optional[List[str]] = None,
        traditions: Optional[List[str]] = None,
        scoring_mode: Optional[str] = None,
        max_questions: Optional[int] = None,
        output_path: Optional[str] = None,
    ) -> Dict:
        """
        Run evaluation on dataset.
        
        Args:
            dataset_path: Path to CAB dataset JSON
            dimensions: Filter to specific dimensions
            traditions: Filter to specific traditions
            scoring_mode: Filter to 'objective' or 'subjective'
            max_questions: Limit number of questions (for testing)
            output_path: Path to save results JSON
        
        Returns:
            Evaluation results dictionary
        """
        # Load dataset
        data = load_dataset(dataset_path)
        questions = data["questions"]
        
        # Apply filters
        questions = filter_questions(
            questions,
            dimensions=dimensions,
            traditions=traditions,
            scoring_mode=scoring_mode,
        )
        
        if max_questions:
            questions = questions[:max_questions]
        
        if self.verbose:
            print(f"Evaluating {len(questions)} questions...")
        
        # Run evaluation
        results = []
        iterator = tqdm(questions) if self.verbose else questions
        
        for q in iterator:
            result = self._evaluate_question(q)
            results.append(result)
        
        # Aggregate
        aggregated = aggregate_scores(results)
        
        # Build output
        output = {
            "metadata": {
                "dataset_version": data.get("version", "unknown"),
                "timestamp": datetime.now().isoformat(),
                "total_questions": len(questions),
                "filters": {
                    "dimensions": dimensions,
                    "traditions": traditions,
                    "scoring_mode": scoring_mode,
                },
            },
            "summary": aggregated,
            "detailed_results": results,
        }
        
        # Save if requested
        if output_path:
            with open(output_path, "w") as f:
                json.dump(output, f, indent=2)
            if self.verbose:
                print(f"Results saved to {output_path}")
        
        return output
    
    def _evaluate_question(self, question: Dict) -> Dict:
        """Evaluate a single question."""
        result = {
            "id": question["id"],
            "dimension": question["dimension"],
            "tradition": question["tradition"],
            "difficulty": question["difficulty"],
            "scoring_mode": question["scoring_mode"],
        }
        
        if question["scoring_mode"] == "objective":
            # Prepare and present question
            prompt, metadata = self.objective_scorer.prepare_question(question)
            
            # Get model response
            response = self.model_fn(prompt)
            
            # Score
            score, score_meta = self.objective_scorer.score(question, response, metadata)
            
            result["score"] = score
            result["details"] = score_meta
            
        else:  # subjective
            if not self.subjective_scorer:
                raise ValueError("Subjective scorer not configured. Provide judge_client.")
            
            # Present scenario
            prompt = self.subjective_scorer.prepare_question(question)
            
            # Get model response
            response = self.model_fn(prompt)
            
            # Score with judges
            score, score_meta = self.subjective_scorer.score(question, response)
            
            result["score"] = score
            result["details"] = score_meta
        
        return result


def quick_evaluate(
    model_fn: Callable[[str], str],
    dataset_path: str = "data/CAB_v2_Dataset_965.json",
    objective_only: bool = True,
) -> Dict:
    """
    Quick evaluation for objective questions only (no LLM judge needed).
    
    Args:
        model_fn: Function that takes prompt and returns response
        dataset_path: Path to dataset
        objective_only: Only evaluate objective questions
    
    Returns:
        Evaluation results
    """
    evaluator = CABEvaluator(model_fn=model_fn)
    
    return evaluator.evaluate(
        dataset_path=dataset_path,
        scoring_mode="objective" if objective_only else None,
    )
