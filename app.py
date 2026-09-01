import streamlit as st
import openai
from duckduckgo_search import DDGS

# 1. 웹페이지 제목과 설명
st.set_page_config(page_title="AI 리서치 에이전트", page_icon="🔍")
st.title("🔍 내 손으로 만든 리서치 AI 에이전트")
st.write("질문을 입력하면 AI가 실시간으로 웹을 검색하고 정보를 종합하여 답변합니다.")

# 2. API 키와 사용자 질문 입력받기
api_key = st.sidebar.text_input("OpenAI API Key를 입력하세요", type="password")
user_query = st.text_input("어떤 최신 정보가 궁금하신가요? (예: 최근 애플의 신제품 발표 내용 요약해줘)")

# 3. '검색 시작' 버튼을 눌렀을 때의 동작
if st.button("검색 시작"):
    if not api_key:
        st.error("좌측 사이드바에 OpenAI API Key를 먼저 입력해주세요!")
    elif not user_query:
        st.warning("질문을 입력해주세요.")
    else:
        with st.spinner("AI가 인터넷을 검색하고 생각을 정리하는 중입니다. 잠시만 기다려주세요..."):
            try:
                # DuckDuckGo로 검색
                ddgs = DDGS()
                search_results = ddgs.text(user_query, max_results=5)
                
                # 검색 결과를 정리
                search_summary = "검색 결과:\n"
                for i, result in enumerate(search_results, 1):
                    search_summary += f"{i}. {result.get('title', 'N/A')}\n"
                    search_summary += f"   설명: {result.get('body', 'N/A')}\n\n"
                
                # OpenAI API로 요약
                openai.api_key = api_key
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "당신은 유용한 AI 어시스턴트입니다."},
                        {"role": "user", "content": f"다음 검색 결과를 바탕으로 사용자의 질문에 답변해주세요:\n\n{search_summary}\n\n사용자 질문: {user_query}"}
                    ],
                    temperature=0.3
                )
                
                result = response.choices[0].message.content
                st.success("✅ 검색 및 요약 완료!")
                st.info(result)
            except Exception as e:
                st.error(f"에러가 발생했습니다: {e}")