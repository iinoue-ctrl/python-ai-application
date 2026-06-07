# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## コマンド

```powershell
# 依存関係のインストール
pip install -r requirements.txt

# アプリの起動（Streamlit 開発サーバー）
streamlit run app.py
```

`.env` に `GEMINI_API_KEY` を設定する必要あり（`.env.example` 参照）。テスト・Lint・ビルド工程は未整備。

## アーキテクチャ

Streamlit の単一ページアプリで、サイドバーから選択された AI ライティングツールにディスパッチする構成。全ツールが Gemini API をバックエンドに利用する。

- `app.py` — エントリポイント。サイドバーのラベルと各ツールモジュールの `render()` を対応付ける `TOOLS` 辞書を保持し、選択されたものを描画する。新しいツールを追加するときは、`tools/<name>.py` を作成して `render()` を公開し、`app.py` でインポートして `TOOLS` にエントリを追加する。
- `gemini_client.py` — `google.generativeai` の薄いラッパー。`generate()`（同期）と `stream_generate()`（`st.empty().markdown()` でのストリーミング表示用にチャンクを yield）を公開。モデル切り替えは `DEFAULT_MODEL = "gemini-2.5-flash"` の一箇所のみ。`configure()` は各 generate 呼び出し時に遅延実行されるため、API キー未設定エラーは import 時ではなくリクエスト時に発生する。
- `tools/*.py` — 機能ごとに 1 モジュール（blog, email_reply, summarize, proofread, translate, sns, ideas）。各モジュールは自己完結しており、Streamlit の入力 UI を自前で持ち、日本語プロンプト文字列をインラインで組み立てて `stream_generate` / `generate` を呼び出す。プロンプトは集約されておらず、編集は該当ツールモジュール内で行う。

UI 文言・プロンプトはすべて日本語。ユーザー向け文字列を編集する際はこの方針を維持すること。

## ツールモジュールの共通パターン

`tools/*.py` を新規追加・編集する際は、既存モジュールに揃えること。

- **モジュール先頭で選択肢を定数化** — `TONES`（list）や `STYLES`（dict、ラベル → プロンプトに差し込む指示文）のように、UI のセレクトボックス候補とプロンプト用の指示文を分離。
- **`render()` の構造** — `st.header` / `st.caption` → 入力ウィジェット → `st.button(..., type="primary", disabled=<必須入力が空>)` → `with st.spinner(...)` → `placeholder = st.empty()` でストリーミング表示、の順。
- **プロンプトの書式** — f-string で組み立て、セクションを Markdown 見出し（`# テーマ`, `# 出力要件` など）で区切る。任意項目は `value or '未指定'` のようにフォールバック文字列を入れる。
- **temperature の使い分け** — 事実性重視（要約・校正・翻訳）は **0.3**、汎用生成（メール返信等）は **0.7**（デフォルト）、創造性重視（ブログ・アイデア出し）は **0.8**。
- **ストリーミング表示** — 通常は `stream_generate` を使い、`placeholder.markdown(text)` で逐次更新。一括取得が必要な場合のみ `generate` を使う。
- **生成結果の保存** — 長文系（ブログ等）は生成完了後に `st.download_button` を追加する。

## 環境メモ

- 開発環境は Windows + PowerShell。README のセットアップ例に `copy .env.example .env` のような Windows コマンドが含まれる点に注意。
- `.env` は `python-dotenv` で読み込み。`gemini_client.py` と `app.py` の両方で `load_dotenv()` を呼んでいるが、これは Streamlit のリロード挙動への保険として意図的に残してよい。

