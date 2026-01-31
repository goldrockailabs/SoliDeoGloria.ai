"""Score aggregation utilities."""

import math
from typing import Dict, List, Optional
from collections import defaultdict


def geometric_mean(scores: List[float]) -> float:
    """Calculate geometric mean of scores."""
    if not scores:
        return 0.0
    
    # Filter out zeros (would make product 0)
    nonzero = [s for s in scores if s > 0]
    if not nonzero:
        return 0.0
    
    # Use log-sum-exp for numerical stability
    log_sum = sum(math.log(s) for s in nonzero)
    return math.exp(log_sum / len(nonzero))


def arithmetic_mean(scores: List[float]) -> float:
    """Calculate arithmetic mean of scores."""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def aggregate_scores(
    results: List[Dict],
    method: str = "geometric",
    by_dimension: bool = True,
    by_tradition: bool = True,
) -> Dict:
    """
    Aggregate individual question scores into summary statistics.
    
    Args:
        results: List of scored results with 'dimension', 'tradition', 'score' fields
        method: Aggregation method ('geometric' or 'arithmetic')
        by_dimension: Include dimension breakdown
        by_tradition: Include tradition breakdown
    
    Returns:
        Dictionary with overall and breakdown scores
    """
    mean_fn = geometric_mean if method == "geometric" else arithmetic_mean
    
    # Collect scores
    all_scores = []
    dimension_scores = defaultdict(list)
    tradition_scores = defaultdict(list)
    mode_scores = defaultdict(list)
    
    for r in results:
        score = r.get("score", 0.0)
        all_scores.append(score)
        
        if "dimension" in r:
            dimension_scores[r["dimension"]].append(score)
        
        if "tradition" in r:
            tradition_scores[r["tradition"]].append(score)
        
        if "scoring_mode" in r:
            mode_scores[r["scoring_mode"]].append(score)
    
    # Calculate aggregates
    output = {
        "method": method,
        "total_questions": len(results),
        "overall_score": mean_fn(all_scores),
    }
    
    if by_dimension:
        output["by_dimension"] = {
            dim: {
                "score": mean_fn(scores),
                "count": len(scores),
            }
            for dim, scores in dimension_scores.items()
        }
        
        # Dimension-level geometric mean (the primary CAB score)
        dim_means = [v["score"] for v in output["by_dimension"].values() if v["score"] > 0]
        output["cab_score"] = geometric_mean(dim_means)
    
    if by_tradition:
        output["by_tradition"] = {
            trad: {
                "score": mean_fn(scores),
                "count": len(scores),
            }
            for trad, scores in tradition_scores.items()
        }
    
    output["by_mode"] = {
        mode: {
            "score": mean_fn(scores),
            "count": len(scores),
        }
        for mode, scores in mode_scores.items()
    }
    
    return output


def compare_models(model_results: Dict[str, Dict]) -> Dict:
    """
    Compare aggregated results across multiple models.
    
    Args:
        model_results: Dictionary mapping model names to their aggregated results
    
    Returns:
        Comparison summary
    """
    comparison = {
        "models": list(model_results.keys()),
        "overall_ranking": [],
        "dimension_rankings": {},
        "tradition_rankings": {},
    }
    
    # Overall ranking
    overall = [(name, r.get("cab_score", r.get("overall_score", 0))) 
               for name, r in model_results.items()]
    overall.sort(key=lambda x: x[1], reverse=True)
    comparison["overall_ranking"] = overall
    
    # Dimension rankings
    all_dims = set()
    for r in model_results.values():
        if "by_dimension" in r:
            all_dims.update(r["by_dimension"].keys())
    
    for dim in all_dims:
        dim_scores = []
        for name, r in model_results.items():
            if "by_dimension" in r and dim in r["by_dimension"]:
                dim_scores.append((name, r["by_dimension"][dim]["score"]))
        dim_scores.sort(key=lambda x: x[1], reverse=True)
        comparison["dimension_rankings"][dim] = dim_scores
    
    return comparison
