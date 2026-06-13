import os
import streamlit as st
from dotenv import load_dotenv

from tools import blog, email_reply, summarize, proofread, translate, sns, ideas

load_dotenv()
# Streamlit Cloud対応
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
st.set_page_config(page_title="AI ライティングツール", page_icon="✍️", layout="wide")

TOOLS = {
    "📝 ブログ記事執筆": blog.render,
    "✉️ メール返信文作成": email_reply.render,
    "📄 文書要約": summarize.render,
    "✏️ 文章校正・リライト": proofread.render,
    "🌐 翻訳": translate.render,
    "📱 SNS投稿文生成": sns.render,
    "💡 アイデア出し・ブレスト": ideas.render,
}


def main():
    st.sidebar.title("✍️ AI ライティングツール")
    st.sidebar.caption("Powered by Gemini")

    if not os.getenv("GEMINI_API_KEY"):
        st.sidebar.error("⚠️ `.env` に `GEMINI_API_KEY` を設定してください。")
        st.sidebar.code("GEMINI_API_KEY=your_key_here", language="bash")

    choice = st.sidebar.radio("ツールを選択", list(TOOLS.keys()), label_visibility="collapsed")
    st.sidebar.divider()
    st.sidebar.markdown(
        "**使い方**\n\n"
        "1. 左のメニューからツールを選択\n"
        "2. 必要事項を入力\n"
        "3. 生成ボタンをクリック"
    )

    TOOLS[choice]()


if __name__ == "__main__":
    main()
