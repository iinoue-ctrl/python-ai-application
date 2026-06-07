import streamlit as st
from gemini_client import stream_generate


MODES = {
    "誤字脱字チェックのみ": "誤字脱字・タイポ・送り仮名の誤りのみを修正",
    "文法・表現も改善": "誤字脱字に加え、文法ミス・冗長表現・不自然な言い回しを改善",
    "全面リライト": "意味を変えずに、より読みやすく洗練された文章に書き直す",
}


def render():
    st.header("✏️ 文章校正・リライト")
    st.caption("誤字脱字チェックから全面リライトまで対応します。")

    text = st.text_area("校正したい文章", height=300)
    mode_label = st.selectbox("校正レベル", list(MODES.keys()), index=1)
    keep_tone = st.checkbox("元の文体・トーンを維持する", value=True)
    show_diff = st.checkbox("修正箇所の説明も表示する", value=True)

    if st.button("校正する", type="primary", disabled=not text.strip()):
        diff_inst = """
- まず「## 修正後の文章」を出力する
- その後「## 主な修正点」セクションで、修正した箇所と理由を箇条書きで列挙する""" if show_diff else "\n- 修正後の文章のみを出力（説明は不要）"
        tone_inst = "\n- 元の文体・トーン・敬体/常体は維持する" if keep_tone else ""

        prompt = f"""あなたはプロの校正者です。以下の文章を校正してください。

# 校正方針
{MODES[mode_label]}

# 出力要件{tone_inst}{diff_inst}

# 原文
{text}"""

        with st.spinner("校正中..."):
            placeholder = st.empty()
            output = ""
            for chunk in stream_generate(prompt, temperature=0.3):
                output += chunk
                placeholder.markdown(output)
