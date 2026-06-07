import streamlit as st
from gemini_client import stream_generate


STYLES = {
    "3行サマリ": "重要ポイントを3行（各60字以内）にまとめる",
    "箇条書き": "重要ポイントを5〜8個の箇条書きにまとめる",
    "段落要約": "1〜2段落の自然な文章で要約する",
    "TL;DR + 詳細": "冒頭にTL;DR（1〜2行）を提示し、その後に詳細な要約を箇条書きで続ける",
}


def render():
    st.header("📄 文書要約")
    st.caption("長い文章を指定形式で要約します。")

    text = st.text_area("要約したい文章", height=300, placeholder="ここに本文を貼り付け")
    style_label = st.selectbox("要約スタイル", list(STYLES.keys()), index=3)
    language = st.selectbox("出力言語", ["元の言語に合わせる", "日本語", "English"], index=0)
    extract_keywords = st.checkbox("キーワード・固有名詞も抽出する", value=True)

    if st.button("要約する", type="primary", disabled=not text.strip()):
        lang_inst = "" if language == "元の言語に合わせる" else f"\n# 出力言語\n{language}"
        kw_inst = "\n- 末尾に「## 重要キーワード」セクションを設け、固有名詞・専門用語を箇条書きで列挙する" if extract_keywords else ""

        prompt = f"""あなたは優秀な編集者です。以下の文章を要約してください。

# 要約スタイル
{STYLES[style_label]}
{lang_inst}

# 出力要件
- 原文の重要な事実・数値・固有名詞を漏らさない
- 推測や原文にない情報を加えない{kw_inst}

# 原文
{text}"""

        with st.spinner("要約中..."):
            placeholder = st.empty()
            output = ""
            for chunk in stream_generate(prompt, temperature=0.3):
                output += chunk
                placeholder.markdown(output)
