# app.py

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="크리스마스는 정말 추운가?",
    layout="wide"
)

st.title("🎄 크리스마스는 정말 추운가? 눈이 내리는가?")
st.subheader("기온 데이터를 이용한 통계적 탐구")

# ---------------------------
# 데이터 불러오기
# ---------------------------

FILE_NAME = "ta_20260601093156.csv"

df = pd.read_csv(FILE_NAME)

df["날짜"] = pd.to_datetime(df["날짜"].astype(str).str.strip())

df["연도"] = df["날짜"].dt.year
df["월"] = df["날짜"].dt.month
df["일"] = df["날짜"].dt.day
df["월일"] = df["날짜"].dt.strftime("%m-%d")

# ---------------------------
# 전체 데이터 요약
# ---------------------------

st.header("1. 데이터 개요")

col1, col2, col3 = st.columns(3)

col1.metric("전체 관측 수", f"{len(df):,}")
col2.metric("시작 연도", int(df["연도"].min()))
col3.metric("마지막 연도", int(df["연도"].max()))

# ---------------------------
# 크리스마스 데이터
# ---------------------------

christmas = df[df["월일"] == "12-25"]

st.header("2. 크리스마스 기온 분석")

avg_xmas = christmas["평균기온(℃)"].mean()
min_xmas = christmas["최저기온(℃)"].mean()
max_xmas = christmas["최고기온(℃)"].mean()

c1, c2, c3 = st.columns(3)

c1.metric("크리스마스 평균기온", f"{avg_xmas:.2f}℃")
c2.metric("크리스마스 평균 최저기온", f"{min_xmas:.2f}℃")
c3.metric("크리스마스 평균 최고기온", f"{max_xmas:.2f}℃")

# ---------------------------
# 전체 평균과 비교
# ---------------------------

st.header("3. 크리스마스는 정말 추운가?")

overall_temp = df["평균기온(℃)"].mean()

comparison = pd.DataFrame({
    "구분": ["전체 평균", "크리스마스 평균"],
    "평균기온": [overall_temp, avg_xmas]
})

st.bar_chart(
    comparison.set_index("구분")
)

difference = overall_temp - avg_xmas

st.write(f"""
### 결과

- 전체 평균기온 : **{overall_temp:.2f}℃**
- 크리스마스 평균기온 : **{avg_xmas:.2f}℃**
- 차이 : **{difference:.2f}℃**

따라서 크리스마스는 연중 평균보다 약 **{difference:.2f}℃ 더 춥다**고 볼 수 있다.
""")

# ---------------------------
# 연도별 크리스마스 기온
# ---------------------------

st.header("4. 연도별 크리스마스 기온 변화")

yearly_xmas = christmas[["연도", "평균기온(℃)"]].set_index("연도")

st.line_chart(yearly_xmas)

# ---------------------------
# 눈 가능성 분석
# ---------------------------

st.header("5. 눈이 내릴 가능성 분석")

# 기온 기반 추정
# 최고기온 0도 이하인 날
snow_condition = christmas["최고기온(℃)"] <= 0

snow_probability = snow_condition.mean() * 100

st.metric(
    "눈이 내리기 쉬운 한파 조건 비율",
    f"{snow_probability:.1f}%"
)

st.write("""
※ 실제 적설량 데이터가 없으므로

'최고기온이 0℃ 이하인 경우'를
눈이 내릴 가능성이 높은 조건으로 정의하였다.
""")

# ---------------------------
# 월별 평균기온
# ---------------------------

st.header("6. 월별 평균기온 비교")

monthly = (
    df.groupby("월")["평균기온(℃)"]
    .mean()
    .reset_index()
    .set_index("월")
)

st.line_chart(monthly)

# ---------------------------
# 탐구 결론
# ---------------------------

st.header("7. 탐구 결론")

if avg_xmas < overall_temp:
    conclusion1 = "크리스마스는 통계적으로 추운 날에 속한다."
else:
    conclusion1 = "크리스마스가 특별히 춥다고 보기 어렵다."

if snow_probability > 20:
    conclusion2 = "눈이 올 수 있는 한파 조건이 자주 나타난다."
else:
    conclusion2 = "눈이 올 가능성은 상대적으로 높지 않다."

st.success(f"""
① {conclusion1}

② {conclusion2}

③ 장기간의 기온 관측 자료를 이용하여
크리스마스의 기온 특성을 객관적으로 분석하였다.

④ 실제 적설량 자료를 추가하면
'크리스마스에 눈이 오는가?'를 더욱 정확하게 검증할 수 있다.
""")
