"""전예준 영역 — 뉴스 모듈.

이 파일은 BE 코어가 정의한 시그니처와 스텁만 들어 있다. 예준은 본문을
NewsAPI(또는 네이버 뉴스 검색 API) 호출 + 중복 제거 + LLM 한 줄 요약으로 교체한다.

규칙:
- 반환 타입은 반드시 `list[NewsResult]`(`app.schemas.news`).
- 실패 시 `NewsError`(`app.core.errors`)를 raise. HTTPException 던지지 말 것.
- LLM 한 줄 요약이 필요하면 `app.core.llm.get_llm()`을 import해서 사용.
"""

from datetime import UTC, datetime

from app.core.errors import NewsError
from app.schemas.news import NewsItem, NewsResult


async def fetch_news(categories: list[str], limit: int = 5) -> list[NewsResult]:
    """카테고리 목록을 받아 카테고리별 뉴스를 반환한다.

    Args:
        categories: 관심 카테고리. 예: ["IT", "경제", "사회"].
        limit: 카테고리당 최대 기사 수 (기본 5).

    Returns:
        `categories` 순서대로 정렬된 `NewsResult` 리스트. 카테고리당 3~5건.

    Raises:
        NewsError: 외부 API 실패, 파싱 실패, 모든 카테고리에서 결과 없음 등.
    """
    # TODO(예준): NewsAPI 또는 네이버 뉴스 검색 API 호출 + 중복 제거 + LLM 요약으로 교체.
    # 정상 흐름에서는 카테고리별로 정규화된 list[NewsResult]를 return.
    # 외부 API 실패·파싱 실패·결과 0건 등에서만 raise NewsError(...).
    raise NewsError(
        "news module not implemented yet — 예준이 fetch_news 본문을 채워야 함"
    )


def _stub_news(categories: list[str], limit: int = 5) -> list[NewsResult]:
    """개발/테스트용 더미 데이터. 예준 모듈 완성 전 BE 검증에만 사용."""
    now = datetime.now(UTC)
    return [
        NewsResult(
            category=category,
            items=[
                NewsItem(
                    title=f"[{category}] 더미 헤드라인 {i + 1}",
                    summary=f"{category} 관련 한 줄 요약 {i + 1}",
                    url=f"https://example.com/{category.lower()}/{i + 1}",
                    published_at=now,
                )
                for i in range(min(3, limit))
            ],
        )
        for category in categories
    ]
