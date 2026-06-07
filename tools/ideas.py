import streamlit as st
from gemini_client import stream_generate


TYPES = {
    "ブログ記事のネタ": "ブログ記事のテーマ案",
    "キャッチコピー": "商品・サービスのキャッチコピー案",
    "タイトル案": "記事・動画タイトル案",
    "切り口・フック": "同じテーマを違う切り口で展開するアイデア",
    "自由ブレスト": "発想を広げる自由なアイデア出し",
}


def render():
    st.header("💡 アイデア出し・ブレスト")
    st.caption("企画・タイトル・キャッチコピーなどのアイデアを大量に生成します。")

    topic = st.text_area("テーマ・対象", height=100, placeholder="例: 30代向けのオンライン英会話サービス")
    idea_type = st.selectbox("アイデアの種類", list(TYPES.keys()))
    target = st.text_input("ターゲット (任意)", placeholder="例: 忙しい社会人")
    count = st.slider("生成数", 5, 30, 15)
    constraint = st.text_input("制約・条件 (任意)", placeholder="例: 30文字以内、数字を含める")

    if st.button("アイデアを出す", type="primary", disabled=not topic.strip()):
        target_inst = f"\n# ターゲット\n{target}" if target else ""
        constraint_inst = f"\n# 制約\n{constraint}" if constraint else ""

        prompt = f"""あなたは優秀なクリエイティブディレクターです。以下のテーマで「{TYPES[idea_type]}」を {count} 個生成してください。

# テーマ
{topic}{target_inst}{constraint_inst}

# 出力要件
- 番号付きリストで {count} 個出力
- 各案は短く、コピペで使える具体的な形にする
- 似たような案を避け、切り口を多様にする
- 解説や前置きは書かない"""

        with st.spinner("生成中..."):
            placeholder = st.empty()
            output = ""
            for chunk in stream_generate(prompt, temperature=1.0):
                output += chunk
                placeholder.markdown(output)
