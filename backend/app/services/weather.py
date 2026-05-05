"""배영빈 영역 — 날씨 모듈.

이 파일은 BE 코어가 정의한 시그니처와 스텁만 들어 있다. 영빈은 본문을
실제 OpenWeatherMap(또는 동등한 API) 호출로 교체한다.

규칙:
- 반환 타입은 반드시 `WeatherData`(`app.schemas.weather`).
- 실패 시 `WeatherError`(`app.core.errors`)를 raise. HTTPException 던지지 말 것.
- LLM 한 줄 요약이 필요하면 `app.core.llm.get_llm()`을 import해서 사용.
"""

from datetime import UTC, datetime

from app.core.errors import WeatherError
from app.schemas.weather import WeatherData


async def fetch_weather(location: str) -> WeatherData:
    """위치 문자열을 받아 오늘 날씨 데이터를 반환한다.

    Args:
        location: 한국 주요 도시명 (예: "서울", "강남").

    Returns:
        정규화된 `WeatherData`. summary 필드는 영빈이 LLM 또는 폴백으로 채운다.

    Raises:
        WeatherError: 외부 API 실패, 응답 파싱 실패, 위치 미지원 등.
    """
    # TODO(영빈): OpenWeatherMap 호출 + 미세먼지(에어코리아 등) + summary 생성으로 교체.
    # 정상 흐름에서는 정규화된 WeatherData 객체를 return.
    # 외부 API 실패·파싱 실패·위치 미지원 등에서만 raise WeatherError(...).
    raise WeatherError(
        "weather module not implemented yet — 영빈이 fetch_weather 본문을 채워야 함"
    )


def _stub_weather(location: str) -> WeatherData:
    """개발/테스트용 더미 데이터. 영빈 모듈 완성 전 BE 검증에만 사용."""
    return WeatherData(
        location=location,
        temperature_min=10.0,
        temperature_max=18.0,
        precipitation_probability=70,
        pm25=35,
        pm10=55,
        summary=f"{location} 오늘 10~18°C, 오후 강수 확률 70%, 미세먼지 보통",
        fetched_at=datetime.now(UTC),
    )
