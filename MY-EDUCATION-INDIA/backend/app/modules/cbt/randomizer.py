import random
from typing import Any, List


class PseudoRandomizer:
    """Provides deterministic question and option randomization unique to each candidate's random seed."""

    @staticmethod
    def shuffle_items_with_seed(items: List[Any], seed: int) -> List[Any]:
        shuffled = list(items)
        rng = random.Random(seed)
        rng.shuffle(shuffled)
        return shuffled

    @staticmethod
    def randomize_candidate_paper(questions: List[dict], candidate_seed: int, shuffle_options: bool = True) -> List[dict]:
        paper = PseudoRandomizer.shuffle_items_with_seed(questions, candidate_seed)
        if shuffle_options:
            for idx, q in enumerate(paper):
                if q.get("options") and isinstance(q["options"], list):
                    opt_seed = candidate_seed + idx + 997
                    q["options"] = PseudoRandomizer.shuffle_items_with_seed(q["options"], opt_seed)
        return paper
