"""
ui/sidebar.py
侧边栏组件，用于 Shopping Agent Streamlit 应用程序。
"""
import streamlit as st
from config import Config


def render_sidebar() -> None:
    """渲染完整的左侧边栏，包括品牌、状态、配置信息和提示。"""
    with st.sidebar:
        # ── App 标题 ────────────────────────────────────────────
        st.markdown(
            """
            <div class="ag-app-title">
              <span class="ag-logo">🛍️</span>
              <h1>Shop<span class="ag-accent">Agent</span></h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── 状态指示器 ─────────────────────────────────────────
        st.markdown(
            """
            <div class="ag-status-badge">
              <span class="ag-status-dot"></span>
              ONLINE
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<hr class="ag-divider">', unsafe_allow_html=True)

        # ── 模型信息 ───────────────────────────────────────────
        st.markdown('<p class="ag-section-header">配置</p>', unsafe_allow_html=True)

        model_display = Config.MODEL or "未设置"
        # 缩短长模型 ID 以便显示
        if len(model_display) > 22:
            model_display = model_display[:20] + "…"

        st.markdown(
            f"""
            <div class="ag-info-row">
              <span class="ag-info-label">Model</span>
              <span class="ag-info-value">{model_display}</span>
            </div>
            <div class="ag-info-row">
              <span class="ag-info-label">Temperature</span>
              <span class="ag-info-value">{Config.TEMPERATURE}</span>
            </div>
            <div class="ag-info-row">
              <span class="ag-info-label">Max Tokens</span>
              <span class="ag-info-value">{Config.MAX_TOKENS}</span>
            </div>
            <div class="ag-info-row">
              <span class="ag-info-label">Memory</span>
              <span class="ag-info-value">{Config.MEMORY_TURNS} 轮对话</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<hr class="ag-divider">', unsafe_allow_html=True)

        # ── 统计 ────────────────────────────────────────────────
        st.markdown('<p class="ag-section-header">Session</p>', unsafe_allow_html=True)

        history = st.session_state.get("messages", [])
        user_turns = sum(1 for m in history if m["role"] == "user")
        tool_calls = sum(
            sum(1 for s in m.get("steps", []) if s.get("type") == "tool")
            for m in history if m["role"] == "assistant"
        )
        input_tokens = st.session_state.get("total_input_tokens", 0)
        output_tokens = st.session_state.get("total_output_tokens", 0)

        st.markdown(
            f"""
            <div class="ag-info-row">
              <span class="ag-info-label">查询</span>
              <span class="ag-info-value">{user_turns}</span>
            </div>
            <div class="ag-info-row">
              <span class="ag-info-label">工具调用</span>
              <span class="ag-info-value">{tool_calls}</span>
            </div>
            <div class="ag-info-row">
              <span class="ag-info-label">输入 Token</span>
              <span class="ag-info-value">{input_tokens}</span>
            </div>
            <div class="ag-info-row">
              <span class="ag-info-label">输出 Token</span>
              <span class="ag-info-value">{output_tokens}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<hr class="ag-divider">', unsafe_allow_html=True)

        # ── 对话操作 ───────────────────────────────────
        from utils.db import delete_session, get_all_sessions

        st.markdown('<p class="ag-section-header">Actions</p>', unsafe_allow_html=True)

        # ✨ 新的对话
        st.markdown('<div class="ag-action-btn">', unsafe_allow_html=True)
        if st.button("✨  新的对话", use_container_width=True, key="btn_new"):
            import uuid
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.session_state.agent = None
            st.session_state.total_input_tokens = 0
            st.session_state.total_output_tokens = 0
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # 🕒 历史对话弹窗
        @st.dialog("历史对话", width="large")
        def history_dialog():
            sessions = get_all_sessions()
            if not sessions:
                st.markdown("<p style='text-align:center;color:var(--text-muted);'>暂无历史对话</p>", unsafe_allow_html=True)
                return
            
            st.markdown('<div class="ag-history-grid">', unsafe_allow_html=True)
            for s in sessions:
                sid = s["session_id"]
                title = s.get("title", "对话")
                updated = s.get("updated_at")
                updated_str = updated.strftime("%Y-%m-%d %H:%M:%S") if updated else "未知时间"

                # 使用容器块通过 CSS 样式化，并将透明按钮置于其上
                # 原生的 streamline 按钮不能包含丰富的 HTML 文本，所以我们使用列或标准按钮
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{title}**<br/><span style='font-size:0.7rem;color:var(--text-muted);'>更新时间: {updated_str}</span>", unsafe_allow_html=True)
                with col2:
                    if st.button("恢复", key=f"restore_{sid}", use_container_width=True):
                        st.session_state.session_id = sid
                        # 让 main.py 在重新运行时从数据库重新加载，因为状态已被清除
                        del st.session_state["messages"]
                        del st.session_state["total_input_tokens"]
                        del st.session_state["total_output_tokens"]
                        st.session_state.agent = None
                        st.rerun()
                st.markdown("<hr style='margin: 0.5rem 0; border-color: var(--border);'>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ag-action-btn">', unsafe_allow_html=True)
        if st.button("🕒  历史对话", use_container_width=True, key="btn_history"):
            history_dialog()
        st.markdown("</div>", unsafe_allow_html=True)

        # 🗑️ 清空对话弹窗
        @st.dialog("清空当前对话？", width="small")
        def clear_confirmation_dialog():
            st.markdown("确定要清空本回合对话吗？此操作将同时从数据库中永久删除该回合数据，**无法撤销**。")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("取消", use_container_width=True):
                    st.rerun()
            with col2:
                if st.button("⚠️ 确认删除", use_container_width=True, type="primary"):
                    delete_session(st.session_state.session_id)
                    import uuid
                    st.session_state.session_id = str(uuid.uuid4())
                    st.session_state.messages = []
                    st.session_state.agent = None
                    st.session_state.total_input_tokens = 0
                    st.session_state.total_output_tokens = 0
                    st.rerun()

        st.markdown('<div class="ag-clear-btn">', unsafe_allow_html=True)
        if st.button("🗑️  清空当前对话", use_container_width=True, key="btn_clear"):
            clear_confirmation_dialog()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<hr class="ag-divider">', unsafe_allow_html=True)

        # ── 提示 ─────────────────────────────────────────────────
        st.markdown('<p class="ag-section-header">Tips</p>', unsafe_allow_html=True)

        tips = [
            ("💡", "请告知您的预算，以便我们给出更精准的建议。"),
            ("🌐", "Agent 搜索 Google Shopping, Amazon, eBay"),
            ("⭐", "询问评论以获取情感分析"),
            ("🔄", "如果您想购买新产品类别，请重新开始"),
        ]

        for icon, text in tips:
            st.markdown(
                f"""
                <div class="ag-tip">
                  <span class="ag-tip-icon">{icon}</span>
                  <span>{text}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ── 页脚 ───────────────────────────────────────────────
        st.markdown('<hr class="ag-divider">', unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:0.7rem;color:var(--text-muted);text-align:center;">'
            "Powered by LangChain · ReAct</p>",
            unsafe_allow_html=True,
        )
