"""
ui/stop_injection.py
注入一个自定义的 Stop 按钮覆盖在 Streamlit 聊天输入框的上方，用于中止生成。
"""
import streamlit as st

def inject_stop_button_js():
    """
    注入 JS 代码，用于找到 stChatInputSubmitButton，隐藏它，并在上方放置一个红色的 Stop Square 按钮。
    当点击时，它会找到原生 Streamlit stop 按钮来中断后端。
    """
    st.components.v1.html("""
    <script>
    const parentDoc = window.parent.document;
    let overlay = null;
    let origSubmit = null;

    const interval = setInterval(() => {
        const chatInput = parentDoc.querySelector('[data-testid="stChatInput"]');
        if (!chatInput) return;
        
        origSubmit = chatInput.querySelector('[data-testid="stChatInputSubmitButton"]');
        if (origSubmit) {
             origSubmit.style.opacity = '0';
             origSubmit.style.pointerEvents = 'none';
        }
        
        overlay = parentDoc.getElementById("ag-custom-stop-btn");
        if (!overlay) {
            overlay = parentDoc.createElement("div");
            overlay.id = "ag-custom-stop-btn";
            // Red stop square icon
            overlay.innerHTML = '<svg viewBox="0 0 24 24" width="20" height="20" fill="#f87171"><rect x="6" y="6" width="12" height="12" rx="2"></rect></svg>';
            
            // Positioning it exactly where the submit button usually sits
            Object.assign(overlay.style, {
                position: 'absolute',
                right: '12px',
                bottom: '12px',
                width: '32px',
                height: '32px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                zIndex: '9999',
                background: 'rgba(248,113,113,0.1)',
                borderRadius: '8px',
                border: '1px solid rgba(248,113,113,0.3)',
                transition: 'all 0.2s',
            });
            
            overlay.onmouseenter = () => { overlay.style.background = 'rgba(248,113,113,0.2)'; };
            overlay.onmouseleave = () => { overlay.style.background = 'rgba(248,113,113,0.1)'; };
            
            overlay.onclick = function(e) {
                e.preventDefault();
                e.stopPropagation();
                // Visual feedback
                overlay.style.opacity = '0.5';
                overlay.style.pointerEvents = 'none';
                
                // Click the native Streamlit stop button to abort background thread
                let statusStop = parentDoc.querySelector('[data-testid="stStatusWidget"] button');
                if (!statusStop) {
                    // Fallback for older Streamlit versions where stop button is in header
                    const headers = parentDoc.querySelectorAll('header button');
                    for (let b of headers) {
                        if (b.innerText === 'Stop' || b.innerText.includes('Stop')) {
                            statusStop = b;
                            break;
                        }
                    }
                }
                if (statusStop) {
                    statusStop.click();
                } else {
                    console.log("[ShopAgent] Could not find native Streamlit stop button!");
                }
            };
            
            chatInput.style.position = 'relative';
            chatInput.appendChild(overlay);
        }
    }, 200);

    // Cleanup when component unmounts (generation finished / stopped)
    window.addEventListener('unload', () => {
        clearInterval(interval);
        if (overlay && overlay.parentNode) {
            overlay.parentNode.removeChild(overlay);
        }
        if (origSubmit) {
             origSubmit.style.opacity = '';
             origSubmit.style.pointerEvents = '';
        }
    });
    </script>
    """, height=0)

def remove_stop_button_js():
    """
    注入 JS 代码，用于主动移除之前注入的 Stop 按钮，并恢复发送按钮。
    """
    st.components.v1.html("""
    <script>
    const parentDoc = window.parent.document;
    const overlay = parentDoc.getElementById("ag-custom-stop-btn");
    if (overlay && overlay.parentNode) {
        overlay.parentNode.removeChild(overlay);
    }
    const chatInput = parentDoc.querySelector('[data-testid="stChatInput"]');
    if (chatInput) {
        const origSubmit = chatInput.querySelector('[data-testid="stChatInputSubmitButton"]');
        if (origSubmit) {
             origSubmit.style.opacity = '';
             origSubmit.style.pointerEvents = '';
        }
    }
    </script>
    """, height=0, width=0)
