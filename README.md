# slack_getChannel

## 1. ABSTRUCT(概要)
本レポジトリは、Slack の conversations.history API を使ってチャネルデータをダウンロードするアプリになります。
2022年9月1日よりSlackの規約変更に伴い、フリープランユーザは過去90日間のデータのみしか保管されないため過去データをバックアップするために開発しています。
ダイレクトメッセージでは無いチャンネル(#が先頭についたもの)は、Slackのバックアップ機能でバックアップされますが、ダイレクトメッセージは対象外となっています。

因みに、Slackでバックアップしたjsonファイルは、thayakawa-gh氏作成のSlackLogViewerで対応できます。但しWindows専用アプリです。

[Slackの消えてしまった過去ログの閲覧ツールを作った。](https://kenkyu-note.hatenablog.com/entry/2020/09/28/045232)<br>
[Github:SlackLogViewer](https://github.com/thayakawa-gh/SlackLogViewer)
<br><br>

## 2. アプリの使い方
### 2-1. Slack側への設定方法
Yoshitaka KOITABASHI氏が提供されている[Slackの特定チャンネルのメッセージをクロールする方法](https://qiita.com/yoshii0110/items/2a7ea29ca8a40a9e42f4)に方法が記載されています。

・Create New Appでアプリを作成する。これはSlack側と通信するためのパイプ役として作成します。<br>
・Permissionを設定します。channels:history, groups:history, im:history, mpim:historyの４つ。特にim系がダイレクトメッセージに該当するようです。<br>
・User OAuth Tokenの取得。これがPython側に設定する内容です。

### 2-2. アプリの使用方法
・ソース中のtoken部分の内容をUser OAuth Tokenの値の書き換えます。
```python
    token = "xxxx-xxxxxxxxxxx-xxxxxxxxxxx-xxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

・実行パラメタ
```bash
python3 slack_getChannel.py --out out.json --channel A1234B56
```
・--channel: バックアップしたいチャンネルIDを指定します。チャンネルIDは各Slackのチャンネルの右側最上部のアイコンの右隣に下向きボタンがあります。この中の最下部にチャンネルIDが表示されています。<br>
・--out: 出力するファイル名（拡張子は固定で.jsonが自動的に付与されます）

### 2-3. 実行後の確認内容について
"client_msg_id"タグが１メッセージの括りになっていると思われます。

ファイル中には、各メッセージの中に"blocks"タグがあり、同じテキストが入っているかと思います。恐らくはスレッド化した際の内容が入るのだろうと勝手に推測はしていますが、検証していません。

時間は"ts"タグの値になります。下記例でts値を入れて実行することで変換することが可能です。pythonの実行環境が無いという方は、Google Colabを実行すると直ぐにpythonの実行ができます。

```python
import datetime

tzinfo=datetime.timezone(datetime.timedelta(hours=9))
ts = datetime.datetime.fromtimestamp(1552455404.000800, tz=tzinfo)
```
