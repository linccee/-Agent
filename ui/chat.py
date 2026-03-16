"""
ui/chat.py
Chat display components for the Shopping Agent Streamlit app.
All HTML/CSS classes are defined in assets/style.css.
"""
import html
import streamlit as st


# ── Example Prompts ───────────────────────────────────────────────────────────
EXAMPLE_PROMPTS = [
    "想买一副通勤降噪耳机，预算 ¥2000",
    "帮我比较适合游戏和办公的 27 寸显示器",
    "我想挑一台适合拍视频的手机，预算 ¥5000",
    "现在买 PS5，哪个平台更划算？",
]


def render_welcome() -> str | None:
    """
    渲染带有示例提示的空白欢迎界面。

    如果点击了提示，则返回示例提示字符串；否则返回 None。
    """
    st.markdown(
        """
        <section class="ag-empty-state glass-panel">
          <div class="ag-empty-state-copy">
            <p class="ag-empty-kicker">CURATED SHOPPING ASSISTANT</p>
            <h3>从“想买点什么”到“应该买哪一个”，只差一次更清晰的对话。</h3>
            <p>告诉我预算、使用场景或偏好，我会整理平台价格、评论信号与最终建议。</p>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<p class="ag-prompt-label">你可以这样开始</p>', unsafe_allow_html=True)

    for row_index in range(0, len(EXAMPLE_PROMPTS), 2):
        cols = st.columns(2)
        for col, prompt in zip(cols, EXAMPLE_PROMPTS[row_index: row_index + 2]):
            with col:
                if st.button(prompt, key=f"example_{prompt[:10]}", use_container_width=True):
                    return prompt
    return None


def _timeline_item_html(label: str, title: str, badge: str, item_class: str, status: str = "") -> str:
    status_html = f'<span class="ag-step-status">{html.escape(status)}</span>' if status else ""
    return (
        f'<div class="ag-timeline-item {item_class}">'
        f'  <div class="ag-timeline-dot"></div>'
        f'  <div class="ag-timeline-card glass-panel">'
        f'    <div class="ag-step-header">'
        f'      <span class="ag-step-badge">{badge}</span>'
        f'      <div class="ag-step-meta">'
        f'        <span class="ag-step-kicker">{html.escape(label)}</span>'
        f'        <span class="ag-step-tool">{html.escape(title)}</span>'
        f'      </div>'
        f'      {status_html}'
        f'    </div>'
        f'  </div>'
        f'</div>'
    )


def render_timeline(steps: list[dict], current_thought: str = None, is_complete: bool = False) -> str:
    """
    将思考和工具调用步骤渲染为浅色玻璃风格的垂直时间线。

    返回 HTML 字符串，以便在流式传输期间使用。
    """
    if not steps and not current_thought:
        return ""

    open_attr = "" if is_complete else " open"
    step_count = len(steps) + (1 if current_thought else 0)
    html_out = [f'<details class="ag-timeline-details"{open_attr}>']
    html_out.append(
        '<summary class="ag-timeline-summary">'
        f'  <span class="ag-timeline-summary-label">轨迹回放</span>'
        f'  <span class="ag-timeline-summary-count">{step_count} 步</span>'
        '</summary>'
    )
    html_out.append('<div class="ag-timeline">')

    idx = 1
    for step in steps:
        badge = f"{idx:02d}"
        if step.get("type") == "thought":
            html_out.append(
                _timeline_item_html(
                    label="思考整理",
                    title=step.get("content", ""),
                    badge=badge,
                    item_class="ag-timeline-item-thought",
                )
            )
        else:
            output = step.get("output", "")
            html_out.append(
                _timeline_item_html(
                    label="工具调用",
                    title=f"调用 {step.get('tool', 'unknown')}",
                    badge=badge,
                    item_class="ag-timeline-item-tool is-complete" if output else "ag-timeline-item-tool is-running",
                    status="已完成" if output else "处理中",
                )
            )
        idx += 1

    if current_thought:
        html_out.append(
            _timeline_item_html(
                label="当前思路",
                title=current_thought,
                badge=f"{idx:02d}",
                item_class="ag-timeline-item-current is-running",
                status="生成中",
            )
        )

    html_out.append("</div></details>")
    return "".join(html_out)


def render_history(messages: list[dict]) -> None:
    """
    使用 st.chat_message 重新显示所有存储的消息，使其与新流式消息的外观完全匹配。

    每个消息字典：{ role: 'user'|'assistant', content: str, steps?: list }
    """
    for msg in messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="🧑"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🪞"):
                if msg.get("steps"):
                    st.markdown(render_timeline(msg["steps"], is_complete=True), unsafe_allow_html=True)
                st.markdown(msg["content"])
