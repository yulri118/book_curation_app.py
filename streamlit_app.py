import streamlit as st
import random

# --- 노래 데이터베이스 ---
# 실제 앱에서는 이 부분을 더 크고 다양한 데이터로 채울 수 있습니다.
# 외부 API 없이 작동하도록 미리 간단한 노래 목록을 만들어 둡니다.
MUSIC_DB = {
    "K-POP": [
        {"artist": "BTS", "title": "Dynamite", "mood": "신남", "energy": "높음"},
        {"artist": "아이유", "title": "밤편지", "mood": "차분", "energy": "낮음"},
        {"artist": "IVE (아이브)", "title": "LOVE DIVE", "mood": "신남", "energy": "중간"},
        {"artist": "AKMU (악뮤)", "title": "오랜 날 오랜 밤", "mood": "차분", "energy": "낮음"},
    ],
    "J-POP": [
        {"artist": "米津玄師 (요네즈 켄시)", "title": "Lemon", "mood": "슬픔", "energy": "중간"},
        {"artist": "YOASOBI", "title": "アイドル (Idol)", "mood": "신남", "energy": "높음"},
        {"artist": "Official髭男dism", "title": "Pretender", "mood": "슬픔", "energy": "중간"},
    ],
    "한국 발라드": [
        {"artist": "성시경", "title": "내게 오는 길", "mood": "차분", "energy": "중간"},
        {"artist": "박효신", "title": "눈의 꽃", "mood": "슬픔", "energy": "낮음"},
        {"artist": "임영웅", "title": "사랑은 늘 도망가", "mood": "슬픔", "energy": "낮음"},
    ],
    "팝송": [
        {"artist": "Taylor Swift", "title": "Shake It Off", "mood": "신남", "energy": "높음"},
        {"artist": "Ed Sheeran", "title": "Perfect", "mood": "차분", "energy": "낮음"},
        {"artist": "Coldplay", "title": "Viva La Vida", "mood": "신남", "energy": "중간"},
    ],
    "재즈": [
        {"artist": "Frank Sinatra", "title": "Fly Me To The Moon", "mood": "차분", "energy": "중간"},
        {"artist": "Louis Armstrong", "title": "What A Wonderful World", "mood": "차분", "energy": "낮음"},
    ],
    "시티팝": [
        {"artist": "김현철", "title": "오랜만에", "mood": "차분", "energy": "중간"},
        {"artist": "Mariya Takeuchi", "title": "Plastic Love", "mood": "차분", "energy": "중간"},
    ]
    # 여기에 다른 장르(힙합, 트로트, 뮤지컬 등)도 추가할 수 있습니다.
}

# --- Streamlit 앱 인터페이스 ---

# 앱 제목 설정
st.title("🎵 내 성격/기분 기반 노래 추천")
st.write("간단한 질문에 답하고 오늘의 노래를 추천받아 보세요!")

# --- 세션 상태(Session State) 초기화 ---
# 추천 결과를 저장할 공간을 만듭니다.
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []


# --- 1. 사용자 입력 받기 ---
st.header("1. 오늘의 당신은 어떤가요?")

# 질문 1: 오늘의 기분 (라디오 버튼)
mood_options = ["신남", "차분", "슬픔"]
user_mood = st.radio(
    "오늘의 기분을 선택해주세요.",
    options=mood_options,
    horizontal=True, # 버튼을 가로로 배열
)

# 질문 2: 에너지 수준 (라디오 버튼)
energy_options = ["높음", "중간", "낮음"]
user_energy = st.radio(
    "현재 에너지 수준은 어떤가요?",
    options=energy_options,
    horizontal=True,
)

# 질문 3: 선호 장르 (여러 개 선택 가능)
genre_options = list(MUSIC_DB.keys()) # 데이터베이스에 있는 장르 목록을 가져옴
user_genres = st.multiselect(
    "좋아하는 음악 장르를 모두 골라주세요. (복수 선택 가능)",
    options=genre_options,
    default=genre_options[0] if genre_options else None # 첫 번째 장르를 기본값으로 선택
)

# --- 2. 노래 추천 로직 실행 ---

# '노래 추천받기' 버튼
if st.button("🎶 나만을 위한 노래 추천받기"):
    # 이전 추천 결과 초기화
    st.session_state.recommendations = []
    
    if not user_genres:
        st.warning("좋아하는 장르를 하나 이상 선택해주세요!")
    else:
        recommended_songs = []
        # 사용자가 선택한 모든 장르에 대해 반복
        for genre in user_genres:
            # 해당 장르의 모든 노래를 확인
            for song in MUSIC_DB[genre]:
                # 노래의 분위기와 에너지가 사용자의 선택과 일치하는지 확인
                if song["mood"] == user_mood and song["energy"] == user_energy:
                    recommended_songs.append(f"**{song['artist']}** - {song['title']} ({genre})")
        
        # 추천된 노래가 있다면 세션 상태에 저장
        if recommended_songs:
            # 노래 목록을 무작위로 섞어서 추천의 재미를 더함
            random.shuffle(recommended_songs)
            st.session_state.recommendations = recommended_songs
        else:
            # 추천 노래가 없다면 빈 리스트를 저장
            st.session_state.recommendations = []

# --- 3. 추천 결과 출력 ---
if st.session_state.recommendations:
    st.header("🎉 당신을 위한 오늘의 추천곡!")
    # 추천곡 목록을 예쁘게 출력
    for song in st.session_state.recommendations:
        st.success(song) # 초록색 박스로 강조
elif 'recommendations' in st.session_state and not st.session_state.recommendations:
    # 버튼을 눌렀지만 결과가 없는 경우
    st.header("😥 아쉬워요!")
    st.warning("아쉽지만 현재 조건에 딱 맞는 노래를 찾지 못했어요. 기분이나 장르를 바꿔서 다시 시도해보세요!")