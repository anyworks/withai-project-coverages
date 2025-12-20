# withai-project-coverages

このリポジトリは、外部リポジトリのテストカバレッジ結果を一元管理し、ユーザーが確認できるようにするためのものです。

**📊 [カバレッジレポートを見る](https://anyworks.github.io/withai-project-coverages/)**

## 概要

- 各プロジェクトのカバレッジレポートは `withai-*` という名前のディレクトリに保存されます
- ルートの `index.html` は、すべてのプロジェクトのカバレッジレポートへのリンクを提供します
- GitHub Actions により、新しいカバレッジレポートが追加されると自動的に `index.html` が更新されます

## 自動更新の仕組み

### ワークフロー

`.github/workflows/update-index.yml` ファイルにより、以下のタイミングで自動的にインデックスが更新されます：

- `main` ブランチに `withai-*` ディレクトリ配下の変更がプッシュされたとき
- 手動でワークフローをトリガーしたとき

### 更新処理

1. `generate_index.py` スクリプトがすべての `withai-*` ディレクトリをスキャン
2. 各プロジェクトのメタデータ（名前、最終更新日時）を取得
3. すべてのプロジェクトを含む新しい `index.html` を生成
4. 変更があれば自動的にコミット＆プッシュ

## カバレッジレポートの追加方法

外部リポジトリから新しいカバレッジレポートを追加する場合：

1. プロジェクト名のディレクトリ（`withai-project-name` 形式）を作成
2. そのディレクトリにカバレッジレポートのHTML等をコピー
3. （オプション）`status.json` ファイルを作成して更新日時を記録：
   ```json
   {
     "timestamp": "2025-12-11 12:00:00 UTC"
   }
   ```
4. `main` ブランチにプッシュすると、自動的に `index.html` が更新されます

## ディレクトリ構造

```
.
├── index.html                    # ルートインデックス（自動生成）
├── generate_index.py             # インデックス生成スクリプト
├── .github/
│   └── workflows/
│       └── update-index.yml      # 自動更新ワークフロー
├── withai-api-mcp-template/      # プロジェクト1のカバレッジ
│   ├── index.html
│   └── ...
├── withai-mcp-kokkai-api/        # プロジェクト2のカバレッジ
│   ├── index.html
│   └── ...
└── withai-mcp-youtube-api-.../   # プロジェクト3のカバレッジ
    ├── index.html
    └── ...
```

## ローカルでのテスト

インデックスを手動で再生成したい場合：

```bash
python3 generate_index.py
```

## 技術詳細

- **言語**: Python 3.x
- **CI/CD**: GitHub Actions
- **ホスティング**: GitHub Pages（推奨）
