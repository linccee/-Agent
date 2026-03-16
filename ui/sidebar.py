"""Sidebar components for the 镜澜导购 Streamlit app."""

import html

import streamlit as st

from config import Config


def render_sidebar() -> None:
    """Render the full sidebar with brand, session stats, and actions."""
    with st.sidebar:
        st.markdown(
            """
            <section class="ag-sidebar-brand glass-panel">
              <p class="ag-sidebar-kicker">MIRROR CURATION</p>
              <div class="ag-sidebar-title-row">
                <span class="ag-logo">◌</span>
                <div>
                  <h1>镜澜导购</h1>
                  <p>把价格、评论与购买判断，整理成更清晰的结论。</p>
                </div>
              </div>
              <div class="ag-status-badge">
                <span class="ag-status-dot"></span>
                在线分析中
              </div>
            </section>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<hr class="ag-divider">', unsafe_allow_html=True)
        st.markdown('<p class="ag-section-header">当前配置</p>', unsafe_allow_html=True)

        model_display = Config.MODEL or "未设置"
        if len(model_display) > 22:
            model_display = model_display[:20] + "…"

        st.markdown(
            f"""
            <section class="ag-panel glass-panel">
              <div class="ag-info-row">
                <span class="ag-info-label">模型</span>
                <span class="ag-info-value">{html.escape(model_display)}</span>
              </div>
              <div class="ag-info-row">
                <span class="ag-info-label">温度</span>
                <span class="ag-info-value">{Config.TEMPERATURE}</span>
              </div>
              <div class="ag-info-row">
                <span class="ag-info-label">Max Tokens</span>
                <span class="ag-info-value">{Config.MAX_TOKENS}</span>
              </div>
              <div class="ag-info-row">
                <span class="ag-info-label">记忆轮次</span>
                <span class="ag-info-value">{Config.MEMORY_TURNS} 轮</span>
              </div>
            </section>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<hr class="ag-divider">', unsafe_allow_html=True)
        st.markdown('<p class="ag-section-header">本轮概览</p>', unsafe_allow_html=True)

        history = st.session_state.get("messages", [])
        user_turns = sum(1 for message in history if message["role"] == "user")
        tool_calls = sum(
            sum(1 for step in message.get("steps", []) if step.get("type") == "tool")
            for message in history
            if message["role"] == "assistant"
        )
        input_tokens = st.session_state.get("total_input_tokens", 0)
        output_tokens = st.session_state.get("total_output_tokens", 0)

        st.markdown(
            f"""
            <section class="ag-panel glass-panel">
              <div class="ag-info-row">
                <span class="ag-info-label">提问次数</span>
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
            </section>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<hr class="ag-divider">', unsafe_allow_html=True)
        st.markdown('<p class="ag-section-header">对话操作</p>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="ag-action-intro">
              <p>开始一轮新的比较，或从历史会话里继续上一次购买判断。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        from utils.db import delete_session, get_all_sessions

        if st.button("开启新对话", use_container_width=True, key="btn_new"):
            import uuid

            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.session_state.agent = None
            st.session_state.total_input_tokens = 0
            st.session_state.total_output_tokens = 0
            st.rerun()

        @st.dialog("历史会话", width="large")
        def history_dialog():
            sessions = get_all_sessions()
            if not sessions:
                st.markdown('<p class="ag-history-empty">还没有可恢复的历史会话。</p>', unsafe_allow_html=True)
                return

            st.markdown(
                """
                <div class="ag-dialog-copy">
                  回到之前的比较过程，继续整理价格、评论与最终建议。
                </div>
                """,
                unsafe_allow_html=True,
            )

            for session in sessions:
                sid = session["session_id"]
                title = html.escape(session.get("title", "未命名对话"))
                updated = session.get("updated_at")
                updated_str = updated.strftime("%Y-%m-%d %H:%M:%S") if updated else "未知时间"

                st.markdown(
                    f"""
                    <div class="ag-history-item glass-panel">
                      <p class="ag-history-title">{title}</p>
                      <p class="ag-history-meta">最近更新 · {updated_str}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                col1, col2 = st.columns([4, 1.2])
                with col1:
                    st.markdown('<div class="ag-history-hint">恢复后将继续沿用该会话的消息与统计。</div>', unsafe_allow_html=True)
                with col2:
                    if st.button("恢复", key=f"restore_{sid}", use_container_width=True):
                        st.session_state.session_id = sid
                        del st.session_state["messages"]
                        del st.session_state["total_input_tokens"]
                        del st.session_state["total_output_tokens"]
                        st.session_state.agent = None
                        st.rerun()
                st.markdown('<div class="ag-history-divider"></div>', unsafe_allow_html=True)

        if st.button("查看历史会话", use_container_width=True, key="btn_history"):
            history_dialog()

        @st.dialog("清空当前对话？", width="small")
        def clear_confirmation_dialog():
            st.markdown(
                """
                <div class="ag-dialog-copy ag-dialog-danger">
                  这会删除当前回合的本地会话记录和数据库内容，操作无法撤销。
                </div>
                """,
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("取消", use_container_width=True):
                    st.rerun()
            with col2:
                if st.button("确认删除", use_container_width=True, type="primary"):
                    delete_session(st.session_state.session_id)
                    import uuid

                    st.session_state.session_id = str(uuid.uuid4())
                    st.session_state.messages = []
                    st.session_state.agent = None
                    st.session_state.total_input_tokens = 0
                    st.session_state.total_output_tokens = 0
                    st.rerun()

        if st.button("清空当前对话", use_container_width=True, key="btn_clear"):
            clear_confirmation_dialog()

        st.markdown('<hr class="ag-divider">', unsafe_allow_html=True)
        st.markdown('<p class="ag-section-header">使用提示</p>', unsafe_allow_html=True)

        tips = [
            ("预算", "尽量告诉我预算区间，我会给出更聚焦的推荐。"),
            ("场景", "补充通勤、游戏、办公等场景，答案会更准确。"),
            ("对比", "可以直接要求我比较两个型号或两个平台的差异。"),
            ("切换", "如果想换到全新品类，建议开启新对话重新整理。"),
        ]
        tips_html = "".join(
            (
                f'<div class="ag-tip">'
                f'<span class="ag-tip-icon">{html.escape(label)}</span>'
                f'<span>{html.escape(text)}</span>'
                f'</div>'
            )
            for label, text in tips
        )
        st.markdown(f'<section class="ag-panel glass-panel">{tips_html}</section>', unsafe_allow_html=True)

        st.markdown('<hr class="ag-divider">', unsafe_allow_html=True)
        st.markdown(
            """
            <p class="ag-sidebar-footer">
              镜澜导购以对话方式整理价格、评论与购买判断。<br/>
              Powered by LangChain · ReAct
            </p>
            """,
            unsafe_allow_html=True,
        )
