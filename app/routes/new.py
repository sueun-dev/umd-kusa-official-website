import os
import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from flask import Blueprint, render_template
from openai import OpenAI

bp = Blueprint("news", __name__, url_prefix="/news")

# 전역 변수: 캐싱된 뉴스 결과와 마지막 업데이트 시간
cached_news_result = None
last_update_time = None

def fetch_and_update_news():
    """
    외부 사이트에서 뉴스를 가져와서 제목, 간략 기사 요약(semi_news) 등 필요한 정보를 추출한 후,
    OpenAI API를 통해 각 뉴스 기사에 대해 간단한 AI 코멘트를 생성하여 캐시를 업데이트합니다.
    (JSON 구조 대신 단순 텍스트 응답을 가정)
    """
    global cached_news_result, last_update_time

    url = "https://dbknews.com/category/news/"
    news_items = []

    # 뉴스 페이지 가져오기
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching news page: {e}")
        return

    # BeautifulSoup을 사용해 페이지 파싱
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article")

    # 각 기사에서 제목, 기사 요약, 날짜 등 필요한 정보 추출
    for article in articles:
        try:
            h3 = article.find("h3")
            if not h3:
                continue
            a_tag = h3.find("a")
            if not a_tag:
                continue

            title = a_tag.get_text(strip=True)
            link = a_tag.get("href", "#")

            # 기사 요약 텍스트: semi_news (원본 기사의 일부 내용을 사용)
            semi_div = article.select_one("div.mt-3.xl\\:text-lg")
            semi_news = semi_div.get_text(strip=True) if semi_div else ""

            time_tag = article.find("time")
            date = time_tag.get_text(strip=True) if time_tag else ""

            news_items.append({
                "title": title,
                "link": link,
                "semi_news": semi_news,
                "date": date
            })
        except Exception as inner_e:
            print("Error parsing an article:", inner_e)
            continue

    # 각 뉴스 항목에 순위(rank) 부여 (필요 시)
    for index, item in enumerate(news_items, start=1):
        item["rank"] = index

    # AI에게 각 뉴스 기사에 대해 간단한 코멘트를 한 줄씩 출력하도록 요청
    # JSON 구조를 사용하지 않고, 각 기사별 코멘트를 줄바꿈으로 구분한다고 가정합니다.
    # (예: "기사1에 대한 코멘트\n기사2에 대한 코멘트\n...")
    prompt = "다음 뉴스 기사들에 대해, 각 기사 제목과 요약을 참고하여 한 줄짜리 간단한 코멘트를 한국어로만 작성해 주세요.\n\n"
    for item in news_items:
        prompt += f"제목: {item['title']}\n요약: {item['semi_news']}\n\n"

    # 환경 변수에서 API 키와 모델 가져오기
    api_key = os.getenv("OPENAI_API_KEY")
    default_model = os.getenv("OPENAI_DEFAULT_MODEL")
    if not api_key or not default_model:
        print("API key or default model not configured properly.")
        return

    # OpenAI 클라이언트 초기화 및 API 호출 (단순 텍스트 응답 기대)
    client = OpenAI(api_key=api_key)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    
    try:
        response = client.chat.completions.create(
            model=default_model,
            messages=messages,
            temperature=0.7,
        )
        ai_response = response.choices[0].message.content.strip()
        
        if not ai_response:
            print("No content returned from GPT API.")
            return

        # AI가 각 뉴스 기사에 대해 한 줄씩 코멘트를 반환했다고 가정하고,
        # 줄바꿈(\n)으로 나누어 리스트로 변환합니다.
        ai_comments = [line.strip() for line in ai_response.split("\n") if line.strip()]
        
        # news_items 리스트와 AI 코멘트 리스트를 매칭합니다.
        # (만약 AI 응답의 기사 수와 news_items의 수가 다를 경우 주의해야 합니다.)
        for idx, item in enumerate(news_items):
            if idx < len(ai_comments):
                item["ai_comment"] = ai_comments[idx]
            else:
                item["ai_comment"] = "코멘트 없음"

        cached_news_result = news_items
        last_update_time = datetime.now()
        print(f"News result updated at {last_update_time}")
    except Exception as e:
        print("Error with GPT API:", e)

@bp.route("/")
def get_news():
    global cached_news_result, last_update_time

    now = datetime.now()
    # 캐시가 없거나 24시간 이상 지난 경우 새로 업데이트
    if last_update_time is None or (now - last_update_time) > timedelta(hours=24):
        fetch_and_update_news()

    if cached_news_result is None:
        error = "News result not available."
        news_items = []
    else:
        error = None
        news_items = cached_news_result

    # news.html 템플릿에 error와 news_items 변수를 전달하여 렌더링
    return render_template("news.html", error=error, news_items=news_items)
