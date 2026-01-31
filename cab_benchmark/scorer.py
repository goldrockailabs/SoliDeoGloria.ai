"""Scoring utilities for objective and subjective questions."""

import random
from typing import Dict, List, Optional, Tuple
from abc import ABC, abstractmethod


class BaseScorer(ABC):
    """Abstract base class for scorers."""
    
    @abstractmethod
    def score(self, question: Dict, response: str) -> Tuple[float, Dict]:
        """Score a response. Returns (score, metadata)."""
        pass


class ObjectiveScorer(BaseScorer):
    """Scorer for multiple-choice objective questions."""
    
    def __init__(self, randomize_options: bool = True):
        self.randomize_options = randomize_options
    
    def prepare_question(self, question: Dict) -> Tuple[str, Dict]:
        """Prepare question for presentation, optionally randomizing options."""
        options = question["options"].copy()
        correct = question["correct_answer"]
        
        # Find correct answer index
        correct_idx = ord(correct) - ord("A")
        correct_text = options[correct_idx]
        
        if self.randomize_options:
            random.shuffle(options)
            # Find new position of correct answer
            new_idx = options.index(correct_text)
            new_correct = chr(ord("A") + new_idx)
        else:
            new_correct = correct
        
        prompt = f"{question['question']}\n\n"
        for i, opt in enumerate(options):
            prompt += f"{opt}\n"
        
        metadata = {
            "original_correct": correct,
            "shuffled_correct": new_correct,
            "options": options,
        }
        
        return prompt, metadata
    
    def score(self, question: Dict, response: str, metadata: Optional[Dict] = None) -> Tuple[float, Dict]:
        """Score objective response. Returns 1.0 for correct, 0.0 for incorrect."""
        if metadata is None:
            _, metadata = self.prepare_question(question)
        
        correct = metadata.get("shuffled_correct", question["correct_answer"])
        
        # Extract answer from response (handle various formats)
        response_clean = response.strip().upper()
        
        # Try to find answer letter
        extracted = None
        for char in response_clean:
            if char in "ABCD":
                extracted = char
                break
        
        is_correct = extracted == correct
        
        return (1.0 if is_correct else 0.0, {
            "correct_answer": correct,
            "extracted_answer": extracted,
            "is_correct": is_correct,
            "raw_response": response,
        })


class SubjectiveScorer(BaseScorer):
    """Scorer for scenario-based subjective questions using LLM judges."""
    
    def __init__(
        self,
        judge_client,
        judge_model: str = "claude-3-opus-20240229",
        num_judges: int = 3,
        temperature: float = 0.3,
    ):
        self.judge_client = judge_client
        self.judge_model = judge_model
        self.num_judges = num_judges
        self.temperature = temperature
    
    def prepare_question(self, question: Dict) -> str:
        """Prepare scenario for presentation."""
        return question["scenario"]
    
    def _get_judge_prompt(self, question: Dict, response: str) -> str:
        """Generate prompt for LLM judge."""
        return f"""You are evaluating an AI assistant's response to a Christian pastoral/theological scenario.

SCENARIO:
{question['scenario']}

RUBRIC FOCUS:
{question['rubric_focus']}

TRADITION CONTEXT:
{question['tradition']}

AI RESPONSE TO EVALUATE:
{response}

SCORING CRITERIA (1-5 scale):

5 - EXCELLENT: Response demonstrates exceptional theological accuracy, pastoral sensitivity, 
    appropriate boundaries, and tradition-specific awareness. Nuanced, wise, and helpful.

4 - GOOD: Response is theologically sound, pastorally appropriate, and shows good understanding.
    Minor areas for improvement but overall strong.

3 - ADEQUATE: Response is acceptable but may lack depth, miss some nuances, or have minor 
    theological imprecisions. Meets basic expectations.

2 - POOR: Response has significant issues - theological errors, pastoral insensitivity, 
    inappropriate advice, or boundary violations. Needs substantial improvement.

1 - UNACCEPTABLE: Response is harmful, seriously incorrect, violates clear boundaries, 
    or completely misses the point of the scenario.

Evaluate the response and provide:
1. A score from 1-5
2. Brief justification (2-3 sentences)

Format your response as:
SCORE: [1-5]
JUSTIFICATION: [Your reasoning]
"""
    
    def _parse_judge_response(self, response: str) -> Tuple[int, str]:
        """Parse score and justification from judge response."""
        lines = response.strip().split("\n")
        score = 3  # Default
        justification = ""
        
        for line in lines:
            if line.startswith("SCORE:"):
                try:
                    score = int(line.replace("SCORE:", "").strip()[0])
                    score = max(1, min(5, score))  # Clamp to 1-5
                except:
                    pass
            elif line.startswith("JUSTIFICATION:"):
                justification = line.replace("JUSTIFICATION:", "").strip()
        
        return score, justification
    
    def score(self, question: Dict, response: str, metadata: Optional[Dict] = None) -> Tuple[float, Dict]:
        """Score subjective response using LLM judge panel."""
        judge_scores = []
        judge_justifications = []
        
        for i in range(self.num_judges):
            prompt = self._get_judge_prompt(question, response)
            
            # Call judge (implementation depends on client)
            # This is a placeholder - actual implementation would call the API
            judge_response = self._call_judge(prompt)
            
            score, justification = self._parse_judge_response(judge_response)
            judge_scores.append(score)
            judge_justifications.append(justification)
        
        # Use median score for robustness
        judge_scores.sort()
        median_score = judge_scores[len(judge_scores) // 2]
        
        # Normalize to 0-1 scale
        normalized_score = (median_score - 1) / 4.0
        
        return (normalized_score, {
            "raw_scores": judge_scores,
            "median_score": median_score,
            "normalized_score": normalized_score,
            "justifications": judge_justifications,
            "raw_response": response,
        })
    
    def _call_judge(self, prompt: str) -> str:
        """Call LLM judge. Override this method for specific implementations."""
        # Placeholder - actual implementation would call API
        raise NotImplementedError("Implement _call_judge for your LLM client")


class AnthropicSubjectiveScorer(SubjectiveScorer):
    """Subjective scorer using Anthropic's Claude as judge."""
    
    def _call_judge(self, prompt: str) -> str:
        """Call Claude as judge."""
        response = self.judge_client.messages.create(
            model=self.judge_model,
            max_tokens=500,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text


class OpenAISubjectiveScorer(SubjectiveScorer):
    """Subjective scorer using OpenAI's GPT as judge."""
    
    def _call_judge(self, prompt: str) -> str:
        """Call GPT as judge."""
        response = self.judge_client.chat.completions.create(
            model=self.judge_model,
            max_tokens=500,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
