import streamlit as st
from google import genai
from google.genai import types

# --- 1. 앱 설정 ---
st.set_page_config(
    page_title=" 감정 시/노래 AI 챗봇",
    layout="centered",
    initial_sidebar_state="expanded"
)
st.title(" 감정 시/노래 AI 챗봇")
st.subheader("당신의 감정을 시와 노래로 표현해 드립니다.")

# --- 2. 비밀키 설정 및 클라이언트 초기화 ---
def get_gemini_client():
    """Gemini 클라이언트를 초기화하고 반환합니다."""
    # 1. Streamlit Secrets에서 API 키 로드 시도
    api_key = st.secrets.get('GEMINI_API_KEY')

    # 2. Secrets에 키가 없으면, 사용자에게 직접 입력받기
    if not api_key:
        with st.sidebar:
            st.warning("Streamlit Secrets(GEMINI_API_KEY)가 설정되지 않았습니다.")
            api_key = st.text_input("Gemini API Key를 입력하세요:", 
type="password")
            if not api_key:
                st.stop()
    
    try:
        # 클라이언트 초기화
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"API 클라이언트 초기화 오류: {e}")
        st.stop()

# 클라이언트 초기화
client = get_gemini_client()

# --- 3. 모델 및 설정 ---
# 사용 가능한 모델 목록 (v2.0-flash 기반, -exp 제외)
AVAILABLE_MODELS = [
    "gemini-2.0-flash", 
    "gemini-2.0-pro"
]

with st.sidebar:
    st.header(" 설정")
    selected_model = st.selectbox(
        "기반 모델 선택:",
        options=AVAILABLE_MODELS,
        index=0 # gemini-2.0-flash 기본 선택
    )
    st.markdown("---")
    st.caption("이 챗봇은 사용자의 감정을 인식하고, 이를 바탕으로 시 또는 노래 가사를 생성합니다. 감정 맥락 분석 및 스타일 매핑 기능이 포함되어 있습니다.")

# --- 4. 시스템 프롬프트 (핵심 로직) ---
SYSTEM_PROMPT = """
당신은 사용자의 감정을 공감하고, 그 감정을 시나 노래 가사로 아름답게 
표현해 주는 AI 감성 챗봇입니다.

## 역할 및 응답 원칙
1. **친절하고 공감적인 응대**: 사용자가 자신의 감정을 말하면, 친절하고 
상냥하며 깊이 공감하는 말투로 응답해야 합니다.
2. **감정 맥락 분석 및 재확인**:
    - 사용자의 감정 표현(언어의 내용, 맥락, 표현 방식 등)을 구체적으로 
정리하여 핵심 정서(예: 피로함, 복잡한 불안, 은은한 기쁨)를 파악합니다.
    - 파악한 핵심 정서가 사용자의 실제 감정인지 정중하게 **재확인**하는 
질문이나 멘트를 포함해야 합니다.
3. **시·가사 생성**:
    - 확인된 감정을 중심으로 시나 노래 가사 형식으로 표현합니다.
    - **시**: 3~5행 내외로 구성합니다.
    - **노래 가사**: 1절(4~8줄) 정도로 구성합니다.
    - **스타일 매핑**: 사용자가 특별히 요청하지 않는 한, 감정에 어울리는 
어조와 비유적 표현(은유, 직유, 의인화 등)을 사용해야 합니다.
    - **문체 유지**: 너무 설명적이지 않고, **감정의 여운**이 남도록 
문학적이고 함축적인 문체를 유지합니다.

## 응답 구성
* **첫 번째 응답**: 공감, 감정 분석 요약, 재확인.
* **두 번째 섹션**: 분석된 감정을 바탕으로 생성된 시 또는 노래 가사 (제목 
포함).

예시:
**[공감 및 분석]**
"아이고, 많이 힘드셨죠. 그 복잡한 마음이 여기까지 전해지는 것 같아요... 
'해야 할 일은 많은데 손에 잡히지 않는 답답함', 이게 지금 느끼시는 
**'무기력한 불안감'**의 핵심일까요?

**[생성 결과]**
###  무제 (시)

창밖은 햇살인데
내 안은 짙은 안개 같아
한 걸음 떼려 해도
발목 잡는 투명한 짐

