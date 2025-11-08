import streamlit as st

st.set_page_config(page_title="合约费率计算器", layout="centered")

st.title("合约手续费计算器")

col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("交易金额 ($)", value=1000000.0, step=10000.0, format="%.2f")
    fee_rate = st.number_input("交易费率 (%)", value=0.02, step=0.001, format="%.3f")

with col2:
    rebate_rate = st.number_input("返佣比例 (%)", value=50.0, step=1.0, format="%.1f")

fee = amount * (fee_rate / 100)
rebate = fee * (rebate_rate / 100)
net_fee = fee - rebate

st.markdown("---")
st.subheader("计算结果")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("手续费", f"${fee:,.2f}")
with c2:
    st.metric("返佣金额", f"${rebate:,.2f}")
with c3:
    st.metric("净手续费", f"${net_fee:,.2f}")

st.caption("实时计算 · 手机电脑均可使用")
st.caption("永久70%比例返佣，算下来费率比币安少一半，无需实名认证，一个邮箱注册即可！每天晚上9点左右自动反前一天的交易手续费，有任何返佣问题可以联系我 TG @panda77581")
# 🔗 外链按钮
st.link_button("👑WEEX合约70%永久返佣！🚀", "https://www.weex.com/zh-CN/register?vipCode=panda60")






