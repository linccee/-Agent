"""
ui/chat.py
Chat display components for the Shopping Agent Streamlit app.
All HTML/CSS classes are defined in assets/style.css.
"""
import html
import json
import streamlit as st


# ── Example Prompts ───────────────────────────────────────────────────────────
EXAMPLE_PROMPTS = [
    "帮我推荐一款预算¥5000以内的机械键盘",
    "我想买一副降噪耳机，预算$200以内",
    "给我找最好的4K电视，预算¥8000",
    "PS5现在哪里买最便宜？",
]


def render_welcome() -> str | None:
    """
    渲染带有示例提示的空白欢迎界面。

    如果点击了提示，则返回示例提示字符串；否则返回 None。
    """
    st.markdown(
        """
        <div class="ag-empty-state">
          <div class="ag-empty-icon">🛍️</div>
          <h3>你的智能购物顾问已就绪</h3>
          <p>告诉我你想买什么，我会搜索最佳选择、比较价格并分析评论。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(len(EXAMPLE_PROMPTS))
    for col, prompt in zip(cols, EXAMPLE_PROMPTS):
        with col:
            if st.button(prompt, key=f"example_{prompt[:10]}"):
                return prompt
    return None


def render_timeline(steps: list[dict], current_thought: str = None, is_complete: bool = False) -> str:
    """
    将思考和工具调用步骤渲染为 Liquid Glass 风格的垂直时间线。

    返回 HTML 字符串，以便在流式传输期间使用。
    """
    if not steps and not current_thought:
        return ""

    open_attr = "" if is_complete else " open"
    
    # 时间线 container 包装器使用details标签
    html_out = [f'<details class="ag-timeline-details"{open_attr}>']
    
    step_count = len(steps) + (1 if current_thought else 0)
    html_out.append(f'<summary class="ag-timeline-summary"><span>⚡ <b>{step_count}</b> 步思考与行动过程</span></summary>')
    html_out.append('<div class="ag-timeline">')

    idx = 1
    for step in steps:
        is_last = (idx == step_count)
        last_class = " ag-timeline-item-last" if is_last else ""
        
        if step.get("type") == "thought":
            thought_text = html.escape(step.get("content", ""))
            html_out.append(
f"""<div class="ag-timeline-item{last_class}" style="animation: fadeInUp 0.4s ease forwards;">
  <div class="ag-timeline-dot"></div>
  <div class="ag-timeline-content glass-panel" style="background: rgba(26, 26, 36, 0.2);">
    <div class="ag-step-header" style="margin-bottom: 0;">
      <span class="ag-step-badge">{idx}</span>
      <span class="ag-step-tool" style="font-family: 'Space Grotesk', sans-serif; font-weight: 500; font-size: 0.85rem; color: var(--text-primary);">{thought_text}</span>
    </div>
  </div>
</div>"""
            )
        else:
            # Tool step
            tool_name = step.get("tool", "unknown")
            output = step.get("output", "")
            # Determine status based on if output exists
            status_html = '<span style="color: var(--success); font-weight: normal; font-size: 0.75rem; margin-left: auto;">已完成</span>' if output else '<span style="color: var(--accent); font-weight: normal; font-size: 0.75rem; margin-left: auto;">进行中...</span>'
            html_out.append(
f"""<div class="ag-timeline-item{last_class}" style="animation: fadeInUp 0.4s ease forwards;">
  <div class="ag-timeline-dot"></div>
  <div class="ag-timeline-content glass-panel">
    <div class="ag-step-header" style="margin-bottom: 0;">
      <span class="ag-step-badge" style="background: var(--text-muted); color: #fff;">{idx}</span>
      <span class="ag-step-tool">调用工具: {html.escape(tool_name)}</span>
      {status_html}
    </div>
  </div>
</div>"""
            )
        idx += 1

    if current_thought:
        html_out.append(
f"""<div class="ag-timeline-item ag-timeline-item-last" style="animation: fadeInUp 0.4s ease forwards;">
  <div class="ag-timeline-dot" style="box-shadow: 0 0 12px var(--accent);"></div>
  <div class="ag-timeline-content glass-panel" style="background: rgba(245, 166, 35, 0.05); border-color: rgba(245, 166, 35, 0.2);">
    <div class="ag-step-header" style="margin-bottom: 0;">
      <span class="ag-step-badge" style="background: var(--accent); box-shadow: 0 0 8px var(--accent-glow);">{idx}</span>
      <span class="ag-step-tool" style="font-family: 'Space Grotesk', sans-serif; font-weight: 500; font-size: 0.85rem; color: var(--accent);">{html.escape(current_thought)}<span class="ag-thinking-dots" style="display:inline-flex; margin-left:8px;"><span></span><span></span><span></span></span></span>
    </div>
  </div>
</div>"""
        )

    html_out.append('</div></details>')
    return "".join(html_out)



def render_history(messages: list[dict]) -> None:
    """
    使用 st.chat_message 重新显示所有存储的消息，使其与新流式消息的外观完全匹配。

    每个消息字典：{ role: 'user'|'assistant', content: str, steps?: list }
    """
    for msg in messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                if msg.get("steps"):
                    st.markdown(render_timeline(msg["steps"], is_complete=True), unsafe_allow_html=True)
                st.markdown(msg["content"])
