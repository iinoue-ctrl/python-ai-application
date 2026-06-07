# AI ライティングツール

Streamlit + Gemini API で作る個人用 AI ライティング集約ツール。

## 機能

- 📝 **ブログ記事執筆** — テーマ・キーワード・文体を指定して記事生成
- ✉️ **メール返信文作成** — 受信メールと要点から返信案を複数生成
- 📄 **文書要約** — 3行/箇条書き/段落/TL;DRなど形式選択可
- ✏️ **文章校正・リライト** — 誤字脱字〜全面リライトまで段階指定
- 🌐 **翻訳** — 多言語間翻訳、用語集対応
- 📱 **SNS投稿文生成** — X/Threads/Instagram/LinkedIn/Facebook向け最適化
- 💡 **アイデア出し・ブレスト** — タイトル案・キャッチコピー等を一括生成

## セットアップ

```bash
# 1. 依存関係をインストール
pip install -r requirements.txt

# 2. .env を作成して Gemini API キーを設定
copy .env.example .env
# → .env を編集して GEMINI_API_KEY=実際のキー を記入

# 3. 起動
streamlit run app.py
```

Gemini API キーは [Google AI Studio](https://aistudio.google.com/app/apikey) から無料で取得できます。

## モデル

デフォルトで `gemini-2.5-flash` を使用しています。変更する場合は `gemini_client.py` の `DEFAULT_MODEL` を編集してください。
