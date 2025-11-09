import streamlit as st
import json

# ---------------------------------------------------
# 页面配置
# ---------------------------------------------------
st.set_page_config(page_title="合约费率计算器", layout="centered")

# 隐藏 Streamlit 默认元素
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ---------------------------------------------------
# 自动检测系统主题 + 手动开关
# ---------------------------------------------------
auto_dark_mode_js = """
<script>
let prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
if (prefersDark) {
    window.parent.postMessage({theme: 'dark'}, '*');
} else {
    window.parent.postMessage({theme: 'light'}, '*');
}
</script>
"""
st.markdown(auto_dark_mode_js, unsafe_allow_html=True)

if "theme" not in st.session_state:
    st.session_state.theme = "light"

theme_placeholder = st.empty()
theme_placeholder.markdown(
    """
    <script>
    window.addEventListener("message", (event) => {
        if (event.data.theme) {
            window.parent.postMessage({setTheme: event.data.theme}, "*");
        }
    });
    </script>
    """,
    unsafe_allow_html=True,
)

dark_mode = st.toggle("夜间模式", value=False if st.session_state.theme == "light" else True)

# ---------------------------------------------------
# 动态主题样式
# ---------------------------------------------------
if dark_mode:
    st.session_state.theme = "dark"
    st.markdown(
        """
        <style>
        body, .stApp {background-color:#0e1117!important;color:#e5e5e5!important;}
        h1,h2,h3,h4,h5,h6,label,p,span,div,.stMarkdown,.stCaption{color:#f0f0f0!important;}
        .stNumberInput input{background:#1a1d29!important;color:#fff!important;border:1px solid #333!important;border-radius:8px!important;}
        [data-testid="stMetricValue"]{color:#fff!important;}
        [data-testid="stMetricLabel"]{color:#bbb!important;}
        .stMetric{background:rgba(255,255,255,.05);padding:12px;border-radius:12px;box-shadow:0 0 15px rgba(0,0,0,.5);}
        .stButton>button{background:linear-gradient(90deg,#1e88e5,#42a5f5);color:#fff!important;border:none;border-radius:10px;padding:10px 24px;font-size:16px;transition:.3s;}
        .stButton>button:hover{transform:scale(1.05);background:linear-gradient(90deg,#42a5f5,#64b5f6);}
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.session_state.theme = "light"
    st.markdown(
        """
        <style>
        body, .stApp {background-color:#fafafa!important;color:#000!important;}
        h1,h2,h3,h4,h5,h6,label,p,span,div,.stMarkdown,.stCaption{color:#111!important;}
        .stNumberInput input{background:#fff!important;color:#000!important;border:1px solid #ccc!important;border-radius:8px!important;}
        [data-testid="stMetricValue"]{color:#000!important;}
        [data-testid="stMetricLabel"]{color:#555!important;}
        .stMetric{background:rgba(0,0,0,.05);padding:12px;border-radius:12px;box-shadow:0 0 8px rgba(0,0,0,.1);}
        .stButton>button{background:linear-gradient(90deg,#4caf50,#81c784);color:#fff!important;border:none;border-radius:10px;padding:10px 24px;font-size:16px;transition:.3s;}
        .stButton>button:hover{transform:scale(1.05);background:linear-gradient(90deg,#66bb6a,#a5d6a7);}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------
# 主体内容
# ---------------------------------------------------
st.title("合约手续费计算器")

col1, col2 = st.columns(2)
with col1:
    amount = st.number_input("交易金额 ($)", value=1000000.0, step=10000.0, format="%.2f")
    fee_rate = st.number_input("交易费率 (%)", value=0.02, step=0.001, format="%.3f")
with col2:
    rebate_rate = st.number_input("返佣比例 (%)", value=70.0, step=1.0, format="%.1f")

fee = amount * (fee_rate / 100)
rebate = fee * (rebate_rate / 100)
net_fee = fee - rebate

# ---------------------------------------------------
# 可拖拽卡片 + favicon 外链
# ---------------------------------------------------
# 初始化卡片位置（session_state 保存拖拽后的坐标）
if "card_positions" not in st.session_state:
    st.session_state.card_positions = {
        "fee": {"top": 0, "left": 0},
        "rebate": {"top": 0, "left": 140},
        "net": {"top": 0, "left": 280},
    }

# 用于接收前端拖拽数据的隐藏组件
drag_data = st.experimental_get_query_params().get("drag", [None])[0]
if drag_data:
    data = json.loads(drag_data)
    st.session_state.card_positions[data["id"]] = {"top": data["top"], "left": data["left"]}

# 卡片容器（相对定位）
st.markdown(
    """
    <div id="drag-container" style="position:relative; height:180px; margin:20px 0;">
    </div>
    """,
    unsafe_allow_html=True,
)

# 注入拖拽 + favicon 脚本
drag_js = f"""
<script>
function makeDraggable(card, id) {{
    let pos = {{ x: {st.session_state.card_positions['fee']['left']}, y: {st.session_state.card_positions['fee']['top']} }};
    if (id === 'rebate') pos = {{ x: {st.session_state.card_positions['rebate']['left']}, y: {st.session_state.card_positions['rebate']['top']} }};
    if (id === 'net') pos = {{ x: {st.session_state.card_positions['net']['left']}, y: {st.session_state.card_positions['net']['top']} }};

    card.style.position = 'absolute';
    card.style.left = pos.x + 'px';
    card.style.top = pos.y + 'px';
    card.style.cursor = 'move';
    card.style.userSelect = 'none';

    let isDragging = false, startX, startY;

    const dragStart = (e) => {{
        if (e.type === 'touchstart') e.clientX = e.touches[0].clientX, e.clientY = e.touches[0].clientY;
        isDragging = true;
        startX = e.clientX - pos.x;
        startY = e.clientY - pos.y;
        card.style.transition = 'none';
    }};

    const drag = (e) => {{
        if (!isDragging) return;
        if (e.type === 'touchmove') e.clientX = e.touches[0].clientX, e.clientY = e.touches[0].clientY;
        pos.x = e.clientX - startX;
        pos.y = e.clientY - startY;
        card.style.left = pos.x + 'px';
        card.style.top = pos.y + 'px';
    }};

    const dragEnd = () => {{
        if (!isDragging) return;
        isDragging = false;
        card.style.transition = 'transform 0.2s';
        // 把位置发回 Streamlit
        const url = new URL(window.location);
        url.searchParams.set('drag', JSON.stringify({{id, top: pos.y, left: pos.x}}));
        window.history.replaceState({{}}, '', url);
        // 触发 reruns
        Streamlit.setComponentValue('drag');
    }};

    card.addEventListener('mousedown', dragStart);
    card.addEventListener('touchstart', dragStart);
    window.addEventListener('mousemove', drag);
    window.addEventListener('touchmove', drag);
    window.addEventListener('mouseup', dragEnd);
    window.addEventListener('touchend', dragEnd);
}}

// 创建卡片
const container = document.getElementById('drag-container');

const cards = [
    {{id:'fee', title:'手续费', value:'${fee:,.2f}'}},
    {{id:'rebate', title:'返佣金额', value:'${rebate:,.2f}'}},
    {{id:'net', title:'净手续费', value:'${net_fee:,.2f}'}}
];

cards.forEach(c => {{
    const div = document.createElement('div');
    div.id = c.id;
    div.className = 'stMetric';
    div.style.width = '120px';
    div.style.padding = '12px';
    div.style.textAlign = 'center';
    div.style.borderRadius = '12px';
    div.style.boxShadow = '0 0 8px rgba(0,0,0,.1)';
    div.innerHTML = `
        <div style="font-weight:bold;font-size:14px;color:#888;">${{c.title}}</div>
        <div style="font-size:18px;font-weight:bold;margin-top:4px;">${{c.value}}</div>
    `;
    container.appendChild(div);
    makeDraggable(div, c.id);
}});

// 外链按钮 + favicon
const linkHtml = `
<div style="text-align:center;margin-top:30px;">
    <a href="https://www.weex.com/zh-CN/register?vipCode=panda60" target="_blank" style="text-decoration:none;display:inline-flex;align-items:center;">
        <img src="https://www.google.com/s2/favicons?domain=weex.com&sz=32" width="20" height="20" style="margin-right:8px;">
        <button style="
            background:linear-gradient(90deg,#ffb300,#ffca28);
            color:black;font-weight:bold;border:none;border-radius:12px;
            padding:12px 30px;font-size:17px;cursor:pointer;
            box-shadow:0 0 15px rgba(255,193,7,.4);transition:.3s;
        " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
            WEEX合约 70% 永久返佣！🚀
        </button>
    </a>
</div>
`;
document.body.insertAdjacentHTML('beforeend', linkHtml);
</script>
"""
st.markdown(drag_js, unsafe_allow_html=True)

# ---------------------------------------------------
# 页脚说明
# ---------------------------------------------------
st.markdown("---")
st.caption("实时计算 · 自动检测系统主题 · 卡片可拖拽")
st.caption("永久70%比例返佣，算下来费率比币安少一半，无需实名认证，一个邮箱注册即可！每天晚上9点自动返前一日手续费，有问题可联系 TG：@panda77581")
