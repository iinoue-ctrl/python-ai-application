import streamlit as st
from gemini_client import stream_generate


TONES = ["カジュアル", "丁寧・ですます", "プロフェッショナル", "ユーモラス", "硬め・である調"]
LENGTHS = {"短め (約500字)": 500, "標準 (約1500字)": 1500, "長文 (約3000字)": 3000}


def render():
    st.header("📝 ブログ記事執筆")
    st.caption("テーマとキーワードを指定して、ブログ記事を自動生成します。")

    topic = st.text_input("テーマ・タイトル", placeholder="例: Pythonで始めるデータ分析入門")
    keywords = st.text_input("キーワード (カンマ区切り)", placeholder="例: pandas, 可視化, 初心者")
    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("文体・トーン", TONES, index=1)
    with col2:
        length_label = st.selectbox("文字数の目安", list(LENGTHS.keys()), index=1)
    target = st.text_input("想定読者 (任意)", placeholder="例: プログラミング初心者")
    outline_only = st.checkbox("まずアウトラインだけ生成する", value=False)

    if st.button("生成する", type="primary", disabled=not topic):
        length = LENGTHS[length_label]
        if outline_only:
            prompt = f"""あなたはプロのブログ編集者です。以下の条件でブログ記事のアウトライン（見出し構成）を作成してください。

# テーマ
{topic}

# キーワード
{keywords or '指定なし'}

# 想定読者
{target or '一般読者'}

# 文体
{tone}

H2・H3レベルの見出しを階層的に提案し、各セクションで触れる要点を箇条書きで添えてください。"""
        else:
            prompt = f"""あなたはプロのブロガーです。以下の条件で読みやすいブログ記事を執筆してください。

# テーマ
{topic}

# キーワード
{keywords or '指定なし'}

# 想定読者
{target or '一般読者'}

# 文体
{tone}

# 文字数の目安
約{length}字

# 出力要件
- Markdown形式で出力
- 導入・本文（複数のH2見出し）・まとめ の構成
- 具体例や箇条書きを適度に活用
- SEOを意識したタイトル案を冒頭に1つ提示"""

        with st.spinner("生成中..."):
            placeholder = st.empty()
            text = ""
            for chunk in stream_generate(prompt, temperature=0.8):
                text += chunk
                placeholder.markdown(text)
            st.download_button("Markdownでダウンロード", text, file_name="blog.md")
