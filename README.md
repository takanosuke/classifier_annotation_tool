# classifier_annotation_tool
## 概要
Pythonのtkinterで開発したクラス分類器用のアノテーションツールです。
## 環境
* python 3.x
* pillow 5.x
## 起動までの準備
1. リポジトリをクローンする（`git clone https://github.com/takanosuke/classifier_annotation_tool.git`)
2. `annotation_tool.py`を開き、設定項目を設定する。
3. 指定したフォルダに画像を入れる
4. アノテーションツールを起動する。（`python annnotation_tool.py`）
## ショートカットキーについて
* 「→」：次の画像へ
* 「←」：前の画像へ
* 「数字キー」：指定したクラスを選択
## 出力ファイル
* json形式で出力
	* キー： 画像ファイル名
	* 値： 選択したクラスに対応する番号
## 注意
* クラス数によってはボタン位置にズレが発生します。ショートカットキーを活用してください。
* クラス数が9個を超えるとショートカットキーが対応できなくなります。