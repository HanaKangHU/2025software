# app.py
import streamlit as st

st.set_page_config(page_title="베스킨라빈스 키오스크 🍨", page_icon="🍦", layout="centered")

# ----- 데이터 정의 -----
FLAVORS = {
    "컵 (1스쿱)": ["바닐라", "초콜릿", "스트로베리", "민트초코", "쿠키앤크림", "녹차"],
    "컵 (2스쿱)": ["바닐라", "초콜릿", "스트로베리", "민트초코", "쿠키앤크림", "녹차", "치즈케이크"],
    "컵 (3스쿱)": ["바닐라", "초콜릿", "스트로베리", "민트초코", "쿠키앤크림", "녹차", "치즈케이크", "솔티카라멜"],
    "콘 (2스쿱)": ["바닐라", "초콜릿", "민트초코", "코튼캔디"],
    "파인트 (가정용, 473ml)": ["바닐라", "초콜릿", "스트로베리", "쿠키앤크림", "녹차", "치즈케이크", "솔티카라멜", "망고"],
}

PRICES = {
    "컵 (1스쿱)": 3000,
    "컵 (2스쿱)": 5200,
    "컵 (3스쿱)": 7200,
    "콘 (2스쿱)": 5500,
    "파인트 (가정용, 473ml)": 12000,
}

TAX_RATE = 0.1  # 부가세 표시 용 (예시: 10%)

# ----- UI 시작 -----
st.title("🍦 베스킨라빈스 키오스크")
st.write("안녕하세요! 달콤한 아이스크림 선택을 도와드릴게요 😊")

# 1) 매장/포장
dine_option = st.radio(
    "1) 매장에서 드실래요, 포장해 가실래요?",
    options=["매장(먹고가기) 🪑", "포장(테이크아웃) 🛍️"],
    horizontal=True
)

# 2) 용기 선택
st.markdown("### 2) 용기/메뉴 선택")
container = st.selectbox("원하시는 용기를 선택해주세요:", options=list(PRICES.keys()))
st.info(f"선택한 용기: {container} — 가격: {PRICES[container]:,}원")

# 스쿱 수 계산
if "1스쿱" in container:
    scoops = 1
elif "2스쿱" in container:
    scoops = 2
elif "3스쿱" in container:
    scoops = 3
else:
    # 파인트 등은 최대 3가지 맛까지 고를 수 있게 처리
    scoops = 3

# 3) 맛 선택
st.markdown(f"### 3) 맛 선택 🍨 (최대 {scoops}개)")
available = FLAVORS.get(container, [])

selected_flavors = []
for i in range(1, scoops + 1):
    flavor = st.selectbox(
        f"{i}번째 스쿱:",
        ["(선택 안함)"] + available,
        key=f"flavor_{i}"
    )
    if flavor != "(선택 안함)":
        selected_flavors.append(flavor)

st.caption("중복 맛 선택도 가능하니 마음껏 골라보세요 😋")

# 4) 가격 계산
base_price = PRICES[container]
tax = int(base_price * TAX_RATE)
total = base_price + tax

st.markdown("### 4) 결제 안내")
st.write(f"- 선택된 맛: {', '.join(selected_flavors) if selected_flavors else '선택 없음'}")
st.write(f"- 소계: {base_price:,}원")
st.write(f"- 부가세(예시 10%): {tax:,}원")
st.write(f"**총 결제금액: {total:,}원** 🧾")

# 4-1) 결제 방식 선택 (기프티콘 추가)
payment = st.radio(
    "결제 방법을 선택해주세요:",
    options=["현금 결제 💵", "카드 결제 💳", "기프티콘 결제 🎁"],
    horizontal=True
)

# 기프티콘 번호 입력 필드 (선택 시 활성화)
gift_number = ""
if payment == "기프티콘 결제 🎁":
    gift_number = st.text_input("기프티콘 번호를 입력해주세요 (예: 1234-5678-ABCD)")

# 결제 버튼
if st.button("결제 진행하기 ✅"):
    if not selected_flavors:
        st.warning("맛을 최소 1개 이상 선택해주세요 🍨")
    else:
        # 기프티콘 검증 로직(간단한 예시)
        if payment == "기프티콘 결제 🎁":
            if not gift_number or len(gift_number.strip()) < 5:
                st.error("기프티콘 번호가 올바르지 않아요 😢 다시 입력해주세요.")
            else:
                st.success("기프티콘 인증이 완료되었습니다! 결제가 진행되었어요 🎉")
                st.balloons()
        elif payment == "현금 결제 💵":
            st.success(f"현금결제 선택 완료! 총 {total:,}원입니다 🙏")
            st.balloons()
        else:  # 카드 결제
            st.success(f"카드결제가 정상적으로 완료되었습니다! {total:,}원 결제 🎉")
            st.balloons()

        # 영수증 출력
        st.markdown("---")
        st.header("영수증 🧾")
        # dine_option은 "매장(먹고가기) 🪑" 같은 형태 -> 사람이 읽기 좋게 그대로 출력
        st.write(f"- 이용 방식: {dine_option}")
        st.write(f"- 용기: {container}")
        st.write(f"- 맛: {', '.join(selected_flavors)}")
        st.write(f"- 결제 방법: {payment}")
        st.write(f"- 총액: {total:,}원")
        if payment == "기프티콘 결제 🎁":
            st.write(f"- 기프티콘 번호: {gift_number}")
        st.caption("주문해 주셔서 감사합니다! 맛있게 드세요 😊")

# 하단 안내
st.markdown("---")
st.write("도움이 필요하시면 직원에게 언제든지 말씀해주세요 🍦")
