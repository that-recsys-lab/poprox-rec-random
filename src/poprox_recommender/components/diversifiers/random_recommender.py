import random

import torch
from poprox_concepts import ArticleSet, InterestProfile

from poprox_recommender.lkpipeline import Component
from poprox_recommender.pytorch.decorators import torch_inference


class RandomRecommender(Component):
    def __init__(self, num_slots: int = 10):
        self.num_slots = num_slots

    @torch_inference
    def __call__(self, candidate_articles: ArticleSet, interest_profile: InterestProfile) -> ArticleSet:
        if candidate_articles.scores is None:
            return candidate_articles

        num_candidates = len(candidate_articles.articles)
        num_slots = min(self.num_slots, num_candidates)
        article_indices = random.sample(range(num_candidates), num_slots)

        return ArticleSet(articles=[candidate_articles.articles[int(idx)] for idx in article_indices])
