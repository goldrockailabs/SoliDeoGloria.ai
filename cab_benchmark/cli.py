"""Command-line interface for CAB benchmark."""

import click
import json
from pathlib import Path


@click.group()
@click.version_option(version="2.0.0")
def main():
    """Christian AI Benchmark (CAB) - Evaluation CLI"""
    pass


@main.command()
@click.argument("dataset", type=click.Path(exists=True))
def validate(dataset):
    """Validate a CAB dataset file."""
    from .loader import load_dataset, get_statistics
    
    try:
        data = load_dataset(dataset)
        stats = get_statistics(data)
        
        click.echo(f"✓ Dataset valid: {stats['total']} questions")
        click.echo(f"\nBy dimension:")
        for dim, count in sorted(stats["by_dimension"].items()):
            click.echo(f"  {dim}: {count}")
        click.echo(f"\nBy tradition:")
        for trad, count in sorted(stats["by_tradition"].items()):
            click.echo(f"  {trad}: {count}")
        click.echo(f"\nBy mode:")
        for mode, count in stats["by_mode"].items():
            click.echo(f"  {mode}: {count}")
            
    except Exception as e:
        click.echo(f"✗ Validation failed: {e}", err=True)
        raise SystemExit(1)


@main.command()
@click.argument("dataset", type=click.Path(exists=True))
@click.option("--dimension", "-d", multiple=True, help="Filter by dimension")
@click.option("--tradition", "-t", multiple=True, help="Filter by tradition")
@click.option("--mode", "-m", type=click.Choice(["objective", "subjective"]))
@click.option("--limit", "-n", type=int, help="Limit number of questions")
@click.option("--output", "-o", type=click.Path(), help="Output file")
def sample(dataset, dimension, tradition, mode, limit, output):
    """Sample questions from dataset."""
    from .loader import load_dataset, filter_questions
    import random
    
    data = load_dataset(dataset)
    questions = filter_questions(
        data["questions"],
        dimensions=list(dimension) if dimension else None,
        traditions=list(tradition) if tradition else None,
        scoring_mode=mode,
    )
    
    if limit and limit < len(questions):
        questions = random.sample(questions, limit)
    
    if output:
        with open(output, "w") as f:
            json.dump({"questions": questions}, f, indent=2)
        click.echo(f"Saved {len(questions)} questions to {output}")
    else:
        for q in questions:
            click.echo(f"\n[{q['id']}] {q['dimension']} / {q['tradition']}")
            text = q.get("question", q.get("scenario", ""))
            click.echo(f"  {text[:100]}...")


@main.command()
@click.argument("results", type=click.Path(exists=True))
def summarize(results):
    """Summarize evaluation results."""
    with open(results) as f:
        data = json.load(f)
    
    summary = data.get("summary", {})
    
    click.echo(f"\n{'='*50}")
    click.echo(f"CAB EVALUATION SUMMARY")
    click.echo(f"{'='*50}")
    
    click.echo(f"\nOverall CAB Score: {summary.get('cab_score', 'N/A'):.3f}")
    click.echo(f"Total Questions: {summary.get('total_questions', 'N/A')}")
    
    if "by_dimension" in summary:
        click.echo(f"\nBy Dimension:")
        for dim, info in sorted(summary["by_dimension"].items()):
            click.echo(f"  {dim}: {info['score']:.3f} (n={info['count']})")
    
    if "by_tradition" in summary:
        click.echo(f"\nBy Tradition:")
        for trad, info in sorted(summary["by_tradition"].items()):
            click.echo(f"  {trad}: {info['score']:.3f} (n={info['count']})")


if __name__ == "__main__":
    main()
