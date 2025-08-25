
---

### [book_curation_app.py 전체 코드]
이제 가장 중요한 앱 코드입니다. 아래 전체 코드를 복사해서 `book_curation_app.py` 라는 이름의 파일로 저장하세요. 코드 각 부분에는 한국어 주석으로 상세한 설명을 달아두었습니다.

```python
import streamlit as st
import requests

# --- 함수 정의 ---

def search_books(query):
    """
    Google Books API를 사용해 도서를 검색하는 함수
    API 키 없이 공개된 엔드포인트를 사용합니다.
    """
    # Google Books API URL
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=10"
    try:
        # API 요청 보내기
        response = requests.get(url)
        response.raise_for_status()  # 오류가 발생하면 예외를 발생시킴
        # JSON 응답을 파이썬 딕셔너리로 변환
        data = response.json()
        return data.get("items", []) # 'items' 키가 없는 경우 빈 리스트 반환
    except requests.exceptions.RequestException as e:
        st.error(f"API 요청 중 오류가 발생했습니다: {e}")
        return []


def get_recommendations(book):
    """
    '내 서재'에 있는 책을 기반으로 추천 도서를 가져오는 함수
    여기서는 첫 번째 책의 저자를 기준으로 간단하게 추천합니다.
    """
    # 책 정보에서 저자 추출, 저자가 없으면 빈 문자열 사용
    authors = book['volumeInfo'].get('authors', [])
    if not authors:
        return [] # 저자 정보가 없으면 추천 불가
    
    # 저자 이름으로 검색 쿼리 생성
    author_query = f"inauthor:{authors[0]}"
    
    # 저자 기반으로 도서 검색
    recommended_books = search_books(author_query)
    return recommended_books

# --- Streamlit 앱 인터페이스 ---

# 앱 제목 설정
st.title("📚 나만의 서재 + 맞춤형 도서 큐레이션")

# --- 세션 상태(Session State) 초기화 ---
# '내 서재' 목록을 저장할 공간을 만듭니다.
# 앱이 재실행되어도 이 값은 유지됩니다.
if 'my_library' not in st.session_state:
    st.session_state.my_library = []
# 검색 결과를 저장할 공간
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
# 이미 추가된 책인지 확인하기 위한 ID 세트
if 'library_ids' not in st.session_state:
    st.session_state.library_ids = set()


# --- 1. 도서 검색 기능 ---
st.header("1. 새로운 도서 검색하기")

# 검색어 입력 필드
search_query = st.text_input("책 제목 또는 저자를 입력하세요:", placeholder="예: 어린왕자")

# 검색 버튼
if st.button("검색"):
    if search_query:
        # 도서 검색 함수 호출
        st.session_state.search_results = search_books(search_query)
        if not st.session_state.search_results:
            st.warning("검색 결과가 없습니다. 다른 검색어로 시도해보세요.")
    else:
        st.warning("검색어를 입력해주세요.")

# 검색 결과 출력
if st.session_state.search_results:
    st.subheader("🔍 검색 결과")
    # 검색된 각 도서에 대해 정보 표시
    for book in st.session_state.search_results:
        book_id = book.get('id')
        info = book.get('volumeInfo', {})
        title = info.get('title', '제목 정보 없음')
        authors = ", ".join(info.get('authors', ['저자 정보 없음']))
        
        # 책 정보를 가로로 정렬하기 위해 컬럼 사용
        col1, col2 = st.columns([1, 4])
        
        # 썸네일 이미지 가져오기
        image_url = info.get('imageLinks', {}).get('thumbnail')
        if image_url:
            with col1:
                st.image(image_url)
        
        with col2:
            st.write(f"**{title}**")
            st.write(f"_{authors}_")
            
            # '내 서재에 추가' 버튼
            # 책 ID가 아직 서재에 없다면 추가 버튼을 보여줌
            if book_id not in st.session_state.library_ids:
                # 각 버튼에 고유한 key를 부여하여 독립적으로 작동하게 함
                if st.button("내 서재에 추가", key=f"add_{book_id}"):
                    st.session_state.my_library.append(book)
                    st.session_state.library_ids.add(book_id)
                    st.success(f"'{title}'을(를) 내 서재에 추가했습니다!")
                    # 버튼 클릭 시 리렌더링하여 버튼이 사라지게 함
                    st.experimental_rerun()
            else:
                st.info("이미 서재에 있는 책입니다.")
        st.divider()

# --- 2. 내 서재 보기 ---
st.header("2. 내 서재")

if not st.session_state.my_library:
    st.info("아직 서재에 추가된 책이 없습니다. 위에서 검색하여 추가해보세요!")
else:
    st.write(f"총 {len(st.session_state.my_library)}권의 책이 있습니다.")
    
    # 서재에 있는 각 도서 정보 출력
    for i, book in enumerate(st.session_state.my_library):
        book_id = book.get('id')
        info = book.get('volumeInfo', {})
        title = info.get('title', '제목 정보 없음')
        authors = ", ".join(info.get('authors', ['저자 정보 없음']))
        publisher = info.get('publisher', '출판사 정보 없음')
        published_date = info.get('publishedDate', '출판일 정보 없음')
        description = info.get('description', '줄거리 정보가 없습니다.')
        
        st.subheader(f"📖 {title}")
        
        col1, col2 = st.columns([1, 2])
        
        # 썸네일 이미지 표시
        image_url = info.get('imageLinks', {}).get('thumbnail')
        if image_url:
            with col1:
                st.image(image_url, caption=title)

        with col2:
            st.markdown(f"**저자:** {authors}")
            st.markdown(f"**출판사:** {publisher}")
            st.markdown(f"**출판일:** {published_date}")
        
        # 줄거리(설명)는 확장/축소 가능하게 표시
        with st.expander("줄거리 보기"):
            st.write(description)
            
        # '서재에서 삭제' 버튼
        if st.button("서재에서 삭제", key=f"del_{book_id}"):
            # 리스트에서 해당 책 제거
            st.session_state.my_library.pop(i)
            st.session_state.library_ids.remove(book_id)
            st.success(f"'{title}'을(를) 서재에서 삭제했습니다.")
            # 페이지 새로고침하여 목록 업데이트
            st.experimental_rerun()
            
        st.divider()

# --- 3. 맞춤형 도서 큐레이션 ---
st.header("3. 맞춤형 도서 추천")

if not st.session_state.my_library:
    st.info("내 서재에 책을 추가하면, 맞춤 도서를 추천해 드립니다.")
else:
    # 내 서재의 첫 번째 책을 기준으로 추천
    first_book = st.session_state.my_library[0]
    first_book_title = first_book['volumeInfo'].get('title', '알 수 없음')
    
    st.write(f"**'{first_book_title}'**의 저자 또는 장르를 기반으로 추천된 도서입니다.")
    
    # 추천 도서 목록 가져오기
    recommendations = get_recommendations(first_book)
    
    if not recommendations:
        st.warning("추천 도서를 찾을 수 없습니다.")
    else:
        # 추천 도서 목록 출력 (최대 5권, 이미 서재에 없는 책만)
        count = 0
        for rec_book in recommendations:
            if count >= 5:
                break
            
            rec_book_id = rec_book.get('id')
            # 추천된 책이 내 서재에 이미 있는지 확인
            if rec_book_id not in st.session_state.library_ids:
                info = rec_book.get('volumeInfo', {})
                title = info.get('title', '제목 정보 없음')
                authors = ", ".join(info.get('authors', ['저자 정보 없음']))
                
                st.markdown(f"- **{title}** ({authors})")
                count += 1