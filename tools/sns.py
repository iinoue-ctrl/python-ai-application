import streamlit as st
from gemini_client import stream_generate


PLATFORMS = {
    "X (Twitter)": {"limit": 140, "hint": "簡潔・インパクト重視、絵文字や改行を活用"},
    "Threads": {"limit": 500, "hint": "やや長め、会話的なトーン"},
    "Instagram": {"limit": 2200, "hint": "ハッシュタグを多めに、視覚的・感情的な表現"},
    "LinkedIn": {"limit": 3000, "hint": "プロフェッショナル、価値提供を意識した構成"},
    "Facebook": {"limit": 2000, "hint": "親しみやすく、ストーリー仕立て"},
}


def render():
    st.header("📱 SNS投稿文生成")
    st.caption("プラットフォームに最適化した投稿文を生成します。")

    topic = st.text_area("投稿のテーマ・伝えたい内容", height=120)
    platform = st.selectbox("プラットフォーム", list(PLATFORMS.keys()))
    info = PLATFORMS[platform]
    col1, col2 = st.columns(2)
    with col1:
        variants = st.slider("案の数", 1, 5, 3)
    with col2:
        include_hashtags = st.checkbox("ハッシュタグを含める", value=True)
    include_emoji = st.checkbox("絵文字を使う", value=True)

    if st.button("生成する", type="primary", disabled=not topic.strip()):
        hashtag_inst = "\n- 適切なハッシュタグを末尾に付ける" if include_hashtags else "\n- ハッシュタグは付けない"
        emoji_inst = "\n- 絵文字を効果的に使う" if include_emoji else "\n- 絵文字は使わない"

        prompt = f"""あなたはSNSマーケティングの専門家です。以下の内容で {platform} 向けの投稿文を {variants} 案作成してください。

# 投稿テーマ
{topic}

# プラットフォーム特性
- 文字数上限: {info['limit']}文字
- スタイル: {info['hint']}

# 出力要件
- 各案を「## 案 1」「## 案 2」のように見出しで区切る
- 文字数上限を厳守{hashtag_inst}{emoji_inst}
- 案ごとに切り口（フック、共感、宣言、質問など）を変える"""

        with st.spinner("生成中..."):
            placeholder = st.empty()
            output = ""
            for chunk in stream_generate(prompt, temperature=0.9):
                output += chunk
                placeholder.markdown(output)
