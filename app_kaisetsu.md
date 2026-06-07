# `app.py` を読み解く ― AIライティングツールの司令塔

このアプリの `app.py` は全部で **40行ほど**ととても短いです。これは「実際の機能は `tools/` 以下の各モジュールに任せて、`app.py` はメニュー画面と振り分けだけを担当する」設計だからです。順番に見ていきましょう。

## 1. import と初期設定（1〜9行目）

```python
import os
import streamlit as st
from dotenv import load_dotenv

from tools import blog, email_reply, summarize, proofread, translate, sns, ideas

load_dotenv()

st.set_page_config(page_title="AI ライティングツール", page_icon="✍️", layout="wide")
```

- **`streamlit`**: ブラウザで動くWeb UIを、Pythonコードだけで作れるライブラリ。
- **`load_dotenv()`**: 同じフォルダにある `.env` ファイルを読み込んで、`GEMINI_API_KEY` を環境変数として使えるようにします。
- **`from tools import ...`**: `tools/` フォルダにある7つのツール（ブログ、メール返信、要約…）を一括で読み込みます。各ファイルは `render()` という関数を持っていて、それが「そのツールの画面を描く」役割をします。
- **`st.set_page_config(...)`**: ブラウザのタブに出るタイトル・アイコン、レイアウトを「ワイド」に設定。**この関数は必ずStreamlitの最初の命令として書く必要があります**。

## 2. ツール一覧の辞書（11〜19行目）

```python
TOOLS = {
    "📝 ブログ記事執筆": blog.render,
    "✉️ メール返信文作成": email_reply.render,
    ...
}
```

ここがこのアプリの**心臓部**です。「メニューに表示するラベル」と「対応する関数」をペアで持つ辞書です。

ポイントは `blog.render` のように **関数を呼び出さずに**書いていること（`()`が付いていない）。つまり「関数そのもの」を値として保存しています。後で `TOOLS[choice]()` と書いたときに、選ばれたツールの関数を実行します。

> 💡 **新しいツールを追加したいときは**、`tools/新ツール.py` を作って `render()` 関数を定義し、上の `import` に追加し、この `TOOLS` に1行足すだけ。これがこの設計の最大のメリットです。

## 3. `main()` ― 画面を組み立てる（22〜39行目）

### サイドバー（左側のメニュー）

```python
st.sidebar.title("✍️ AI ライティングツール")
st.sidebar.caption("Powered by Gemini")
```

`st.sidebar.◯◯` と書くと、その要素は画面左のサイドバーに出ます。

### APIキーのチェック

```python
if not os.getenv("GEMINI_API_KEY"):
    st.sidebar.error("⚠️ `.env` に `GEMINI_API_KEY` を設定してください。")
    st.sidebar.code("GEMINI_API_KEY=your_key_here", language="bash")
```

APIキーが設定されていなければ、赤いエラーメッセージと設定例を表示。**親切ガイド**ですね。

### ツール選択ラジオボタン

```python
choice = st.sidebar.radio("ツールを選択", list(TOOLS.keys()), label_visibility="collapsed")
```

`TOOLS.keys()`（=ツール名のリスト）をラジオボタンとして表示し、ユーザーが選んだ文字列を `choice` に入れます。`label_visibility="collapsed"` でラベル文字を非表示にしてスッキリ見せています。

### 使い方ガイド

```python
st.sidebar.divider()
st.sidebar.markdown("**使い方**\n\n1. 左のメニュー...")
```

区切り線を引いて、Markdown形式で使い方を表示。

### 最後の1行 ― 振り分け実行

```python
TOOLS[choice]()
```

**この1行が全体の動きを決めています**。

- `TOOLS[choice]` で、選ばれたラベルに対応する `render` 関数を取り出し
- `()` で実行 → そのツールの画面が右側に描画される

## 4. 起動部分（42〜43行目）

```python
if __name__ == "__main__":
    main()
```

「このファイルが直接実行されたときだけ `main()` を動かす」という、Pythonでおなじみの定型文です。

---

## まとめ ― この設計の良いところ

| 役割 | 担当ファイル |
|------|------------|
| メニュー表示・振り分け | `app.py`（今回のファイル） |
| 各ツールの中身（UI＋プロンプト） | `tools/*.py` |
| Gemini APIとの通信 | `gemini_client.py` |

責任がきれいに分かれているので、たとえば「翻訳ツールの動きを直したい」なら `tools/translate.py` だけを見ればOK。`app.py` を触る必要はありません。

次に読むなら、**実際にAIを呼び出している `gemini_client.py`** か、**お好きなツール（例：`tools/blog.py`）** がおすすめです。
