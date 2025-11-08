import streamlit as st

# ==================== 1. 缓存计算函数 ====================
@st.cache_data(ttl=600)          # 缓存 10 分钟，防止频繁刷新
def calculate_fee(amount: float, fee_rate: float, rebate_rate: float):
    fee = amount * (fee_rate / 100)
    rebate = fee * (rebate_rate / 100)
    net_fee = fee - rebate
    return fee, rebate, net_fee


# ==================== 2. 页面配置（宽屏+隐藏侧边栏） ====================
st.set_page_config(
    page_title="合约手续费计算器",
    layout="wide",               # 宽屏，渲染更快
    initial_sidebar_state="collapsed"
)

# ==================== 3. 标题 ====================
st.markdown("# 合约手续费计算器")

# ==================== 4. 输入区（可折叠） ====================
with st.expander("输入参数（点击展开/收起）", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("交易金额 ($)", value=1000000.0, step=10000.0, format="%.2f", key="amt")
        fee_rate = st.number_input("交易费率 (%)", value=0.02, step=0.001, format="%.3f", key="fr")
    with col2:
        rebate_rate = st.number_input("返佣比例 (%)", value=50.0, step=1.0, format="%.1f", key="rr")

# ==================== 5. 计算按钮（可选） ====================
if st.button("立即计算", type="primary", use_container_width=True):
    fee, rebate, net_fee = calculate_fee(amount, fee_rate, rebate_rate)
    st.session_state["results"] = (fee, rebate, net_fee)
else:
    # 默认也算一次（首次打开）
    fee, rebate, net_fee = calculate_fee(amount, fee_rate, rebate_rate)
    if "results" not in st.session_state:
        st.session_state["results"] = (fee, rebate, net_fee)

# ==================== 6. 结果展示 ====================
st.markdown("---")
st.subheader("计算结果")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("手续费", f"${fee:,.2f}")
with c2:
    st.metric("返佣金额", f"${rebate:,.2f}")
with c3:
    st.metric("净手续费", f"${net_fee:,.2f}")

# ==================== 7. 宣传 & 外链 ====================
st.caption("实时计算 · 手机电脑均可使用")
st.caption(
    "永久70%比例返佣，算下来费率比币安少一半，**无需实名认证**，一个邮箱注册即可！"
    "每天晚上9点左右自动返前一天的交易手续费，有任何返佣问题可以联系我 **TG @panda77581**"
)

st.link_button(
    "WEEX合约70%永久返佣！",
    "https://www.weex.com/zh-CN/register?vipCode=panda60",
    use_container_width=True
)
