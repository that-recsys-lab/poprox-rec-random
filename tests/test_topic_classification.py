import json
import logging
import random

from poprox_concepts import Article, ArticleSet, Click
from poprox_recommender.paths import project_root
from poprox_recommender.topics import GENERAL_TOPICS, extract_general_topics, match_news_topics_to_general

logger = logging.getLogger(__name__)


def load_test_articles():
    test_dir = project_root() / "tests"
    event_path = test_dir / "request_data" / "request_body.json"

    with open(event_path, "r") as j:
        req_body = json.loads(j.read())

        candidate = ArticleSet(articles=[Article.model_validate(attrs) for attrs in req_body["todays_articles"]])
        past = ArticleSet(articles=[Article.model_validate(attrs) for attrs in req_body["past_articles"]])
        click_history = [Click.model_validate(attrs) for attrs in req_body["click_data"]]
        num_recs = req_body["num_recs"]

    return candidate, past, click_history, num_recs


def test_topic_classification():
    candidate, _, _, _ = load_test_articles()
    topic_matched_dict, todays_article_matched_topics = match_news_topics_to_general(candidate.articles)
    assert len(todays_article_matched_topics.keys()) > 0

    random_10_topic = random.sample(list(topic_matched_dict.keys()), 10)
    for article_topic in random_10_topic:
        assert len(topic_matched_dict[article_topic]) > 0


def test_extract_generalized_topic():
    candidate, _, _, _ = load_test_articles()
    for article in candidate.articles:
        generalized_topics = extract_general_topics(article)
        for topic in generalized_topics:
            assert topic in GENERAL_TOPICS
