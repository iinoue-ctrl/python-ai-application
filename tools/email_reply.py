import streamlit as st
from gemini_client import stream_generate


TONES = ["丁寧・ビジネス", "ややフォーマル", "カジュアル・親しみやすい", "簡潔・短文"]


def render():
    st.header("✉️ メール返信文作成")
    st.caption("受信したメールに対する返信文をAIが作成します。")

    received = st.text_area("受信したメール本文", height=200, placeholder="ここに受信メールを貼り付け")
    intent = st.text_area(
        "返信で伝えたい内容（要点・箇条書きOK）",
        height=120,
        placeholder="例:\n- 提案ありがとう\n- 来週火曜午後なら可能\n- 資料を事前に送ってほしい",
    )
    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("文体", TONES, index=0)
    with col2:
        language = st.selectbox("言語", ["日本語", "English"], index=0)
    sender_name = st.text_input("自分の署名 (任意)", placeholder="例: 井上")
    variants = st.slider("案の数", 1, 3, 1)

    if st.button("返信文を生成", type="primary", disabled=not received or not intent):
        prompt = f"""あなたは優秀なビジネスアシスタントです。以下の受信メールに対する返信を、指定された要点と文体で {variants} 案作成してください。

# 受信メール
{received}

# 返信で伝えたい内容
{intent}

# 文体
{tone}

# 言語
{language}

# 署名
{sender_name or '（未指定 — 適切なプレースホルダで）'}

# 出力要件
- 各案を「## 案 1」「## 案 2」のように見出しで区切る
- 件名(Re:)・本文（宛名・本文・結び・署名）を含める
- 不要な前置きや解説は書かない"""

        with st.spinner("生成中..."):
            placeholder = st.empty()
            text = ""
            for chunk in stream_generate(prompt, temperature=0.7):
                text += chunk
                placeholder.markdown(text)
