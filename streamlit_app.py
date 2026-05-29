import streamlit as st

# 1. 앱 페이지 설정
st.set_page_config(page_title="디지털 자판기", page_icon="💳")

# 2. 데이터 초기화 (세션 상태 관리)
# 앱이 새로고침되어도 돈과 재고가 초기화되지 않게 보호합니다.
if 'balance' not in st.session_state:
    st.session_state.balance = 0
if 'inventory' not in st.session_state:
    st.session_state.inventory = {
        "콜라": {"price": 1500, "stock": 5, "icon": "🥤"},
        "사이다": {"price": 1200, "stock": 3, "icon": "🍹"},
        "생수": {"price": 800, "stock": 10, "icon": "💧"},
        "커피": {"price": 2000, "stock": 2, "icon": "☕"}
    }
if 'log' not in st.session_state:
    st.session_state.log = []

# --- UI 레이아웃 시작 ---

st.title("🤖 파이썬 스마트 자판기")
st.markdown("---")

# 3. 사이드바: 돈 넣기 및 관리자 기능
with st.sidebar:
    st.header("💰 금액 투입")
    insert_amount = st.number_input("금액을 입력하세요 (원)", min_value=0, step=100)
    if st.button("현금 넣기"):
        st.session_state.balance += insert_amount
        st.success(f"{insert_amount}원이 충전되었습니다!")
    
    st.divider()
    if st.button("💳 카드 결제 (1,000원)"):
        st.session_state.balance += 1000
        st.info("카드로 1,000원이 충전되었습니다.")
    
    if st.button("🔄 재고 초기화"):
        del st.session_state.inventory
        st.rerun()

# 4. 메인 화면: 현황판
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.metric(label="현재 잔액", value=f"{st.session_state.balance:,} 원")
with col_info2:
    st.write(f"📢 **상태:** {'주문 가능' if st.session_state.balance > 0 else '금액을 투입해주세요'}")

st.divider()

# 5. 상품 진열대 (4개의 컬럼으로 구성)
cols = st.columns(4)
for i, (name, info) in enumerate(st.session_state.inventory.items()):
    with cols[i]:
        st.markdown(f"### {info['icon']}")
        st.write(f"**{name}**")
        st.write(f"{info['price']:,}원")
        
        # 재고 수량에 따른 색상 표시
        if info['stock'] > 0:
            st.caption(f"재고: {info['stock']}개")
            if st.button(f"구매", key=name):
                # 구매 로직
                if st.session_state.balance >= info['price']:
                    st.session_state.balance -= info['price']
                    st.session_state.inventory[name]['stock'] -= 1
                    st.session_state.log.insert(0, f"✅ {name} 구매 완료!")
                    st.toast(f"{name}이(가) 나왔습니다! 🥤")
                    st.rerun()
                else:
                    st.error("잔액 부족!")
        else:
            st.error("품절")
            st.button("품절", key=name, disabled=True)

# 6. 하단 로그 및 잔돈 반환
st.divider()
if st.button("💸 잔돈 반환 및 종료"):
    change = st.session_state.balance
    st.session_state.balance = 0
    st.session_state.log = []
    st.warning(f"잔돈 {change:,}원이 반환되었습니다. 이용해 주셔서 감사합니다!")
    st.balloons()

# 최근 활동 기록 표시
if st.session_state.log:
    with st.expander("최근 구매 기록 보기"):
        for record in st.session_state.log:
            st.write(record)