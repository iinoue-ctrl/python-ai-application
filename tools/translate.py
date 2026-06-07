import streamlit as st
from gemini_client import stream_generate


LANGUAGES = ["日本語", "English", "中文 (簡体)", "中文 (繁體)", "한국어", "Français", "Deutsch", "Español", "Português", "Italiano", "Русский", "Tiếng Việt"]
STYLES = ["自然な翻訳", "直訳に近い", "ビジネス向け（フォーマル）", "カジュアル・口語", "技術文書向け"]


def render():
    st.header("🌐 翻訳")
    st.caption("多言語間で翻訳します。文体の指定も可能です。")

    text = st.text_area("翻訳したい文章", height=200)
    col1, col2 = st.columns(2)
    with col1:
        src = st.selectbox("翻訳元の言語", ["自動検出"] + LANGUAGES, index=0)
    with col2:
        dst = st.selectbox("翻訳先の言語", LANGUAGES, index=1)
    style = st.selectbox("翻訳スタイル", STYLES, index=0)
    glossary = st.text_area("用語集 (任意・1行1組: 原語=訳語)", height=80, placeholder="例:\nAgent=エージェント\nprompt=プロンプト")

    if st.button("翻訳する", type="primary", disabled=not text.strip()):
        src_inst = "原文の言語を自動判別してください。" if src == "自動検出" else f"原文の言語: {src}"
        glossary_inst = f"\n\n# 用語集 (必ず従うこと)\n{glossary}" if glossary.strip() else ""

        prompt = f"""あなたはプロの翻訳者です。以下の文章を翻訳してください。

# 指示
- {src_inst}
- 翻訳先の言語: {dst}
- スタイル: {style}
- 訳文のみを出力し、解説や前置きは書かない
- 改行・段落構成は原文に合わせる{glossary_inst}

# 原文
{text}"""

        with st.spinner("翻訳中..."):
            placeholder = st.empty()
            output = ""
            for chunk in stream_generate(prompt, temperature=0.3):
                output += chunk
                placeholder.markdown(output)
