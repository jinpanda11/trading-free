import streamlit as st

# ---------------------------------------------------
# 页面配置
# ---------------------------------------------------
st.set_page_config(page_title="合约费率计算器", layout="centered")

# 🚫 隐藏 Streamlit 页脚、菜单、GitHub 信息
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ---------------------------------------------------
# 🌗 夜间模式开关
# ---------------------------------------------------
dark_mode = st.toggle("🌙 夜间模式", value=True)

if dark_mode:
    st.markdown(
        """
        <style>
        body, .stApp {
            background-color: #0e1117 !important;
            color: #e5e5e5 !important;
        }
        h1, h2, h3, h4, h5, h6, p, label, span, div, .stMarkdown, .stCaption {
            color: #e5e5e5 !important;
        }
        .stNumberInput input {
            background-color: #1a1d29 !important;
            color: #ffffff !important;
            border: 1px solid #333 !important;
            border-radius: 8px !important;
        }
        [data-testid="stMetricValue"] {
            color: #ffffff !important;
        }
        [data-testid="stMetricLabel"] {
            color: #bbbbbb !important;
        }
        .stMetric {
            background: rgba(255,255,255,0.05);
            padding: 12px;
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(0,0,0,0.5);
        }
        .stButton>button {
            background: linear-gradient(90deg, #1e88e5, #42a5f5);
            color: white !important;
            border: none;
            border-radius: 10px;
            padding: 10px 24px;
            font-size: 16px;
            transition: 0.3s ease-in-out;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #42a5f5, #64b5f6);
        }
        .stCaption, .stToggle label {
            color: #cccccc !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body, .stApp {
            background-color: #fafafa !important;
            color: #000000 !important;
        }
        h1, h2, h3, h4, h5, h6, p, label, span, div, .stMarkdown, .stCaption {
            color: #111111 !important;
        }
        .stNumberInput input {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #ccc !important;
            border-radius: 8px !important;
        }
        [data-testid="stMetricValue"] {
            color: #000000 !important;
        }
        [data-testid="stMetricLabel"] {
            color: #555555 !important;
        }
        .stMetric {
            background: rgba(0,0,0,0.05);
            padding: 12px;
            border-radius: 12px;
            box-shadow: 0 0 8px rgba(0,0,0,0.1);
        }
        .stButton>button {
            background: linear-gradient(90deg, #4caf50, #81c784);
            color: white !important;
            border: none;
            border-radius: 10px;
            padding: 10px 24px;
            font-size: 16px;
            transition: 0.3s ease-in-out;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #66bb6a, #a5d6a7);
        }
        .stCaption, .stToggle label {
            color: #333333 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# 主体内容
# ---------------------------------------------------
st.title("💹 合约手续费计算器")

col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("💰 交易金额 ($)", value=1000000.0, step=10000.0, format="%.2f")
    fee_rate = st.number_input("📈 交易费率 (%)", value=0.02, step=0.001, format="%.3f")

with col2:
    rebate_rate = st.number_input("🎁 返佣比例 (%)", value=70.0, step=1.0, format="%.1f")

fee = amount * (fee_rate / 100)
rebate = fee * (rebate_rate / 100)
net_fee = fee - rebate

st.markdown("---")
st.subheader("📊 计算结果")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("手续费", f"${fee:,.2f}")
with c2:
    st.metric("返佣金额", f"${rebate:,.2f}")
with c3:
    st.metric("净手续费", f"${net_fee:,.2f}")

st.markdown("---")

st.caption("⚡ 实时计算 · 适配手机与桌面端")
st.caption("💎 永久70%比例返佣，算下来费率比币安少一半，无需实名认证，一个邮箱注册即可！每天晚上9点自动返前一日手续费，有问题可联系 TG：@panda77581")

# ---------------------------------------------------
# 🔗 外链按钮
# ---------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; margin-top: 20px;">
        <a href="https://www.weex.com/zh-CN/register?vipCode=panda60" target="_blank" style="text-decoration:none;">
            <button style="
                background: linear-gradient(90deg, #ffb300, #ffca28);
                color: black;
                font-weight: bold;
                border: none;
                border-radius: 12px;
                padding: 12px 30px;
                font-size: 17px;
                cursor: pointer;
                box-shadow: 0 0 15px rgba(255,193,7,0.4);
                transition: 0.3s ease-in-out;
            ">
                👑 WEEX合约 70% 永久返佣！🚀
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
