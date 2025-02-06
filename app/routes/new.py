import os
import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from bs4.element import Tag  # Import Tag for proper type checking
from flask import Blueprint, render_template
from openai import OpenAI
from typing import List, Dict, Any

bp = Blueprint("news", __name__, url_prefix="/news")


class NewsFetcher:
    """
    Encapsulates fetching, parsing, and annotating news articles with AI-generated comments.
    Implements caching to avoid frequent updates.
    """
    CACHE_DURATION = timedelta(hours=24)

    def __init__(self) -> None:
        self.cached_news_result: List[Dict[str, Any]] = []
        self.last_update_time: datetime | None = None

    def is_cache_expired(self) -> bool:
        """Return True if no cache exists or if the cache is expired."""
        return (
            self.last_update_time is None or
            (datetime.now() - self.last_update_time) > self.CACHE_DURATION
        )

    def fetch_news_page(self, url: str, timeout: int = 10) -> str:
        """Fetch the HTML content of the news page."""
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching news page: {e}")
            return ""

    def parse_news(self, html: str) -> List[Dict[str, str]]:
        """Parse news items from the HTML using BeautifulSoup."""
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.find_all("article")
        news_items: List[Dict[str, str]] = []
        for article in articles:
            # Ensure article is a Tag
            if not isinstance(article, Tag):
                continue
            try:
                h3 = article.find("h3")
                if not (h3 and isinstance(h3, Tag)):
                    continue
                a_tag = h3.find("a")
                if not (a_tag and isinstance(a_tag, Tag)):
                    continue

                title = a_tag.get_text(strip=True)
                link = a_tag.get("href", "#")
                semi_div = article.select_one("div.mt-3.xl\\:text-lg")
                semi_news = semi_div.get_text(strip=True) if isinstance(semi_div, Tag) else ""
                time_tag = article.find("time")
                date = time_tag.get_text(strip=True) if isinstance(time_tag, Tag) else ""

                news_items.append({
                    "title": title,
                    "link": link,
                    "semi_news": semi_news,
                    "date": date
                })
            except Exception as e:
                print("Error parsing an article:", e)
                continue

        # Optionally assign ranking numbers to each item
        for index, item in enumerate(news_items, start=1):
            item["rank"] = str(index)  # rank stored as string for consistency

        return news_items

    def generate_ai_comments(self, news_items: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Generate AI comments for each news item using OpenAI's Chat Completion API.
        Instructs the AI to return a JSON array (or newline-separated lines) of comments.
        """
        if not news_items:
            return news_items

        prompt = (
            "다음 뉴스 기사들에 대해, 각 기사 제목과 요약을 참고하여 한 줄짜리 간단한 코멘트를 "
            "한국어로만 작성해 주세요.\n\n"
        )
        for item in news_items:
            prompt += f"제목: {item['title']}\n요약: {item['semi_news']}\n\n"

        api_key = os.getenv("OPENAI_API_KEY")
        default_model = os.getenv("OPENAI_DEFAULT_MODEL")
        if not api_key or not default_model:
            print("API key or default model not configured properly.")
            for item in news_items:
                item["ai_comment"] = "코멘트 없음"
            return news_items

        try:
            # Initialize the new OpenAI client
            client = OpenAI(api_key=api_key)
            # Annotate messages with explicit type for Pyright.
            messages: List[Dict[str, str]] = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
            # The type stubs may complain; use type: ignore if necessary.
            response = client.chat.completions.create(  # type: ignore
                model=default_model,
                messages=messages,
                temperature=0.7,
            )
        except Exception as e:
            print("Error with GPT API:", e)
            for item in news_items:
                item["ai_comment"] = "코멘트 없음"
            return news_items

        # Safely call strip() even if content might be None.
        ai_response = (response.choices[0].message.content or "").strip()
        if not ai_response:
            print("No content returned from GPT API.")
            for item in news_items:
                item["ai_comment"] = "코멘트 없음"
            return news_items

        # Try to parse the response as JSON; if that fails, fall back to newline splitting.
        try:
            ai_comments = json.loads(ai_response)
            if not isinstance(ai_comments, list):
                raise ValueError("Parsed JSON is not a list.")
        except Exception as json_e:
            print("Error parsing JSON response, falling back to newline splitting:", json_e)
            ai_comments = [line.strip() for line in ai_response.split("\n") if line.strip()]

        for idx, item in enumerate(news_items):
            item["ai_comment"] = ai_comments[idx] if idx < len(ai_comments) else "코멘트 없음"

        return news_items

    def update_cache(self) -> None:
        """Fetch news from the external source, generate AI comments, and update the cache."""
        url = "https://dbknews.com/category/news/"
        html = self.fetch_news_page(url)
        if not html:
            return
        news_items = self.parse_news(html)
        news_items = self.generate_ai_comments(news_items)
        self.cached_news_result = news_items
        self.last_update_time = datetime.now()
        print(f"News result updated at {self.last_update_time}")

    def get_news(self) -> List[Dict[str, str]]:
        """Return current news items; update cache if expired."""
        if self.last_update_time is None or (datetime.now() - self.last_update_time) > self.CACHE_DURATION:
            self.update_cache()
        return self.cached_news_result if self.cached_news_result else []


# Create a singleton instance of NewsFetcher.
news_fetcher = NewsFetcher()

# ---- Global functions (preserved for compatibility) ----

def fetch_and_update_news() -> None:
    """
    외부 사이트에서 뉴스를 가져와서 제목, 간략 기사 요약(semi_news) 등 필요한 정보를 추출한 후,
    OpenAI API를 통해 각 뉴스 기사에 대해 간단한 AI 코멘트를 생성하여 캐시를 업데이트합니다.
    """
    news_fetcher.update_cache()

def get_news_global() -> List[dict]:
    """
    캐시된 뉴스 결과를 반환합니다.
    """
    return news_fetcher.get_news()

# ---- Blueprint route remains the same ----

@bp.route("/")
def get_news_route():
    """
    Route handler for /news that renders the news template with the current news items.
    """
    news_items = news_fetcher.get_news()
    error = None if news_items else "News result not available."
    return render_template("news.html", error=error, news_items=news_items)
