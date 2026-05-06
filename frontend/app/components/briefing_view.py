"""브리핑 응답을 화면에 렌더한다."""
import streamlit as st

from app.schemas import BriefingResponse, NewsResult, WeatherData

_DEGRADED_LABEL = {
    "weather": "날씨",
    "news": "뉴스",
    "llm": "AI 요약",
}


def render_briefing(briefing: BriefingResponse) -> None:
    _render_degraded_banner(briefing.degraded)
    _render_integrated_card(briefing.action_tip, briefing.integrated_summary)

    st.divider()

    col_weather, col_news = st.columns([1, 2])
    with col_weather:
        st.subheader("오늘의 날씨")
        if briefing.weather is None:
            st.caption("날씨 정보를 일시적으로 가져오지 못했습니다.")
        else:
            _render_weather(briefing.weather)

    with col_news:
        st.subheader("오늘의 뉴스")
        if not briefing.news:
            st.caption("뉴스 정보를 일시적으로 가져오지 못했습니다.")
        else:
            _render_news(briefing.news)

    st.divider()
    local_time = briefing.generated_at.astimezone().strftime("%Y-%m-%d %H:%M:%S")
    st.caption(f"생성 시각: {local_time}")


def _render_degraded_banner(degraded: list[str]) -> None:
    if not degraded:
        return
    labels = [_DEGRADED_LABEL.get(k, k) for k in degraded]
    st.warning(f"일부 정보를 일시적으로 가져오지 못했습니다: {', '.join(labels)}")


def _render_integrated_card(action_tip: str, integrated_summary: str) -> None:
    if action_tip:
        st.info(f"**오늘의 한 줄** — {action_tip}")
    if integrated_summary:
        st.markdown(f"#### {integrated_summary}")


def _render_weather(weather: WeatherData) -> None:
    c1, c2 = st.columns(2)
    c1.metric("최고 기온", f"{weather.temperature_max:.1f}°C")
    c2.metric("최저 기온", f"{weather.temperature_min:.1f}°C")

    c3, c4 = st.columns(2)
    c3.metric("강수 확률", f"{weather.precipitation_probability}%")
    if weather.pm25 is not None:
        c4.metric("초미세먼지", f"{weather.pm25} ㎍/㎥")
    elif weather.pm10 is not None:
        c4.metric("미세먼지", f"{weather.pm10} ㎍/㎥")

    if weather.summary:
        st.caption(weather.summary)


def _render_news(news_results: list[NewsResult]) -> None:
    tabs = st.tabs([r.category for r in news_results])
    for tab, result in zip(tabs, news_results, strict=True):
        with tab:
            if not result.items:
                st.caption("이 카테고리에는 표시할 뉴스가 없습니다.")
                continue
            for idx, item in enumerate(result.items):
                st.markdown(f"**[{item.title}]({item.url})**")
                st.write(item.summary)
                st.caption(
                    item.published_at.astimezone().strftime("%Y-%m-%d %H:%M")
                )
                if idx < len(result.items) - 1:
                    st.divider()
