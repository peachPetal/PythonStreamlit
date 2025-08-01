import streamlit as st
from datetime import datetime
import pandas as pd
import re

# 페이지의 레이아웃 설정
st.set_page_config(
    layout="wide"  # "wide"로 설정하면, 화면을 넓게 활용할 수 있습니다.
)

# SQL 연결 주석 처리
# conn = st.connection('mysql', type='sql')

# 로그인 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_alias' not in st.session_state:
    st.session_state.user_alias = ""

# 사이드바 UI
with st.sidebar:
    st.header("음악 스트리밍")
    
    # 로그인 상태 메시지
    if not st.session_state.logged_in:
        st.error("로그인이 필요합니다")
    else:
        st.success(f"🟢{st.session_state.user_alias}님으로 로그인됨")

    # 로그인 탭, 회원가입 탭
    tab1, tab2 = st.tabs(['로그인', '회원가입'])

    # 로그인 탭
    with tab1:
        # 사용자 선택 select box
        # DB 연결 없이 임시 데이터 사용
        alias_data = ['gemini', 'user1', 'user2']
        selected_alias = st.selectbox("사용자 선택", alias_data)

        # 로그인 버튼
        if st.button('로그인', key="login_button"):
            if selected_alias:
                # 로그인 상태로 변경
                st.session_state.logged_in = True
                st.session_state.user_alias = selected_alias            
                # 최상단 메시지 업데이트를 위해 rerun 호출
                st.rerun()

    # 회원가입 탭
    with tab2:
        name = st.text_input("이름")  
        alias = st.text_input("별칭") 
        email = st.text_input("이메일") 
        address = st.text_input("주소") 
        created_at = st.date_input("날짜를 선택하세요", value=datetime.today()) 
        
        if st.button('가입하기', key="sign_button"):
            # SQL 쿼리 주석 처리
            # query = text('''INSERT INTO users (name, alias, email, address, join_date) 
            #                 VALUES (:name, :alias, :email, :address, :join_date)''')
            # conn.session.execute(query, {
            #     "name": name,
            #     "alias": alias,
            #     "email": email,
            #     "address": address,
            #     "join_date": created_at
            # })
            # conn.session.commit()
            st.success("회원가입이 완료되었습니다!")

# 플레이리스트에 선택한 트랙을 추가하는 함수
# SQL 연결 주석 처리
# def add_playlist_query(playlist_id, track_ids):
#     with conn.session as session:
#         try:
#             session.execute(
#                 text("""
#                 INSERT INTO playlists_tracks(playlist_id, track_id)
#                 VALUES (:playlist_id, :track_id)
#                 """),
#                 [{"playlist_id": playlist_id, "track_id": track_id} for track_id in track_ids]
#             )
#             session.commit()
#         except Exception as e:
#             raise Exception(f"저장 중 오류가 발생하였습니다: {str(e)}")

# 플레이리스트에 트랙을 추가하는 팝업창을 띄우는 다이얼로그
@st.dialog("플레이리스트에 추가")
def add_playlist(title):
    # SQL 쿼리 주석 처리 및 임시 데이터 사용
    playlists = [(1, '나의 첫 플레이리스트'), (2, '드라이브할 때'), (3, '새벽 감성')]
    options = [re.sub(r"['\"]", '', item[1]) for item in playlists]
    playlist_ids = [item[0] for item in playlists]
    
    # 임시 트랙 데이터프레임 생성
    df_t = pd.DataFrame([
        {'track_id': 101, 'track_title': 'Track A', 'duration': '3:45', 'total_play': 123456},
        {'track_id': 102, 'track_title': 'Track B', 'duration': '4:10', 'total_play': 234567},
        {'track_id': 103, 'track_title': 'Track C', 'duration': '3:20', 'total_play': 345678}
    ])
    
    with st.container():
        st.subheader(f"💿 {title}")  # 앨범 제목 출력
        selected_option = st.selectbox("플레이리스트를 선택하세요", options)  # 플레이리스트 선택
        selected_playlist_id = playlist_ids[options.index(selected_option)]  # 선택된 playlist_id 가져오기

        st.write("추가할 곡을 선택하세요:")
        track_ids = []  # 체크된 track_id들을 저장할 리스트
        for idx, row in enumerate(df_t.itertuples(index=True), start=1):
            col1, col2, col3, col4 = st.columns([0.5, 1, 1, 1])
            with col1:
                checked = st.checkbox(label=' ', key=f"track_{row.track_id}")
                if checked:
                    track_ids.append(row.track_id)
            with col2:
                st.write(f"**{idx}. {row.track_title}**")
            with col3:
                st.markdown(f"<span style='color:black;'>{row.duration}</span>", unsafe_allow_html=True)
            with col4:
                st.markdown(f"재생수: <span style='color:black;'>{row.total_play:,}</span>", unsafe_allow_html=True)

    st.divider()

    if st.button("선택한 곡들을 플레이리스트에 추가", type="primary"):
        if track_ids:
            try:
                # SQL 함수 호출 주석 처리
                # add_playlist_query(selected_playlist_id, track_ids)
                st.success(f"{len(track_ids)}곡이 플레이리스트에 추가되었습니다!")
            except Exception as e:
                st.error(str(e))
        else:
            st.warning("추가할 곡을 선택하세요!")

# 앨범 상세정보를 띄우는 다이얼로그
@st.dialog("앨범 상세정보")
def show_album(name, title):
    # SQL 쿼리 주석 처리 및 임시 데이터 사용
    df_a = pd.DataFrame([
        {'name': name, 'artist_desc': '매력적인 목소리를 가진 아티스트입니다.', 'subscriber_count': 100000, 
         'title': title, 'release_year': 2024, 'album_type': 'EP', 'total_tracks': 5}
    ])
    df_t = pd.DataFrame([
        {'track_title': 'Track 1', 'duration': '3:30', 'total_play': 50000},
        {'track_title': 'Track 2', 'duration': '4:05', 'total_play': 60000},
        {'track_title': 'Track 3', 'duration': '3:50', 'total_play': 70000}
    ])

    with st.container():
        col1, col2 = st.columns([1, 1])
        with col1:
            for row in df_a.itertuples():
                st.subheader("**👤 아티스트 정보**")
                st.markdown(f"**{row.name}**")
                st.write(row.artist_desc)
                st.markdown(f"구독자 수: <span style='color:black;'>{row.subscriber_count:,}</span>명", unsafe_allow_html=True)
                st.divider()
                st.subheader("**💿 앨범 정보**")
                st.write("**앨범명:**", row.title)
                st.markdown(f"**발매년도:** <span style='color:black;'>{ row.release_year}</span>", unsafe_allow_html=True) 
                st.write("**앨범 유형:**", row.album_type)
                st.markdown(f"**총 곡 수:** <span style='color:black;'>{ row.total_tracks}</span>곡", unsafe_allow_html=True)
        with col2:
            st.subheader("**🎵 수록곡**") 
            col1, col2 = st.columns([1, 1])
            for idx, row in enumerate(df_t.itertuples(index=True), start=1):
                st.write(f"**{idx}.{row.track_title}**")
                st.markdown(f"*<span style='color:black;'>{row.duration}</span>*", unsafe_allow_html=True) 
                st.markdown(f"재생수: <span style='color:black;'>{row.total_play:,}</span>", unsafe_allow_html=True)
                st.divider()

#플레이리스트의 수록곡 정보
@st.dialog("수록곡")
def show_playlist_tracks(playlist_title):
    # SQL 쿼리 주석 처리 및 임시 데이터 사용
    df_t = pd.DataFrame([
        {'track_title': '수록곡 A', 'duration': '3:30', 'total_play': 15000, 'artist_name': '아티스트 X'},
        {'track_title': '수록곡 B', 'duration': '4:15', 'total_play': 25000, 'artist_name': '아티스트 Y'}
    ])

    with st.container():
        st.subheader(f"**🎵 {playlist_title} 수록곡**") 
        for idx, row in enumerate(df_t.itertuples(index=True), start=1):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.write(f"**{idx}. {row.track_title}**")
                st.markdown(f"*<span style='color:black;'>{row.duration}</span>* | 재생수: <span style='color:black;'>{row.total_play:,}</span>", unsafe_allow_html=True)
                st.write(f"아티스트: {row.artist_name}")
            
            with col2:
                pass
            
            st.divider()

# 메인 화면 UI
tab1, tab2 = st.tabs(['음악 목록', '플레이리스트'])

with tab1:
    st.header("음악 목록")

    # 음악 목록 불러오기 (임시 데이터 사용)
    df = pd.DataFrame({
        'name': ['BTS', 'IU', 'NewJeans', 'BTS'],
        'title': ['Map of the Soul: 7', 'LILAC', 'Ditto', 'Dynamite'],
        'release_year': [2020, 2021, 2022, 2020],
        'album_type': ['album', 'album', 'single', 'single']
    })
    
    # 가수 목록 출력
    for row in df.itertuples():
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 4, 2, 2])
            with col1:
                st.markdown(f"**{row.title}**")
                st.write(f"아티스트: {row.name}")
            with col2:
                pass
            with col3:
                st.write(f"발매: {row.release_year}")
                st.markdown(f"*{row.album_type}*")
            with col4:
                if st.button(f"앨범보기", key=f"view_album_button_{row.Index}"):
                    show_album(row.name, row.title)
                if st.button("플레이리스트에 추가", type="primary", key=f"add_playlist_button_{row.Index}"):
                    add_playlist(row.title)
            st.divider()

with tab2:
    st.header("내 플레이리스트")

    with st.expander("새 플레이리스트 만들기"):
        playlist_input = st.text_input("플레이리스트 제목", placeholder="플레이리스트 제목을 입력하세요")
        memo_input = st.text_area("메모", placeholder="플레이리스트에 대한 메모를 입력하세요")

        st.markdown(
            """
            <style>
            .stButton > button {
                width: 100%;  
                height: 40px; 
                font-size: 16px;  
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # 로그인 유저 ID 가져오는 부분 주석 처리
        user_id = None
        if st.session_state.logged_in:
            user_alias = st.session_state.user_alias
            # SQL 쿼리 주석 처리
            # with conn.session as session:
            #     result = session.execute(
            #         text("""SELECT user_id FROM users WHERE alias = :alias"""),
            #         {"alias": user_alias}
            #     )
            #     user_id = result.scalar()
            user_id = 1 # 임시 user_id 설정
        
        if st.button("생성하기"):
            if not playlist_input.strip():
                st.warning("플레이리스트 제목을 입력하세요!")
            else:
                # SQL 쿼리 주석 처리
                # with conn.session as session:
                #     try:
                #         session.execute(
                #             text("""
                #             INSERT INTO playlists (user_id, title, memo, created_date)
                #             VALUES (:user_id, :title, :memo, NOW())
                #             """),
                #             {"user_id": user_id, "title": playlist_input.strip(), "memo": memo_input.strip()}
                #         )
                #         session.commit()
                #         st.success(f"'{playlist_input}' 플레이리스트가 생성되었습니다!")
                #     except Exception as e:
                #         st.error(f"플레이리스트 생성 중 오류가 발생하였습니다: {str(e)}")
                st.success(f"'{playlist_input}' 플레이리스트가 생성되었습니다!")


    st.divider()

    st.subheader("🎵 저장된 플레이리스트 목록")
    
    # SQL 쿼리 주석 처리 및 임시 데이터 사용
    playlists = [
        {'playlist_title': '나의 첫 플레이리스트', 'created_date': datetime.now(), 'memo': '좋아하는 곡들 모음', 'track_count': 5},
        {'playlist_title': '퇴근길 듣는 노래', 'created_date': datetime.now(), 'memo': '', 'track_count': 3},
        {'playlist_title': '새로 만든 플레이리스트', 'created_date': datetime.now(), 'memo': '최신곡 위주', 'track_count': 0}
    ]

    if not playlists:
        st.info("저장된 플레이리스트가 없습니다. 새 플레이리스트를 만들어 보세요!")
    else:
        for playlist in playlists:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**🎶 {playlist['playlist_title']}**")
                    st.markdown(f"📅 생성일: {playlist['created_date'].strftime('%Y-%m-%d')}")
                    if playlist['memo']:
                        st.markdown(f"📝 메모: {playlist['memo']}")
                    st.markdown(f"🎵 수록곡 개수: {playlist['track_count']}곡")
                with col2:
                    if st.button("삭제", key=f"delete_{playlist['playlist_title']}"):
                        st.success(f"'{playlist['playlist_title']}'이 삭제되었습니다!")

                    if st.button("수록곡 보기", key=f"view_{playlist['playlist_title']}"):
                        show_playlist_tracks(playlist['playlist_title'])

            st.divider()