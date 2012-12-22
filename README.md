aozoraxhtml2mobi
================

- 青空文庫の XHTML 形式のファイルを Kindle で読める .mobi 形式に変換す
  る python スクリプトです
- amazon.com が無料で配布している kindlegen が必要です
- Linux で実行することを想定しています
- 出力サンプルは[[こちら]](http://yasuoka.net/~yasuoka/aozora.html)


インストールに必要なもの
------------------------

- インストール、実行する Linux
- kindlegen をインストールしておく
  - http://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211


インストール
------------

1. インストールするディレクトリを作成し、移動します:

        % mkdir aozoraxhtml2mobi
        % cd aozoraxhtml2mobi

2. aozoraxhtml2mobi.py をダウンロードします

        % https://github.com/yasuoka/aozoraxhtml2mobi/raw/master/aozoraxhtml2mobi.py
3. kindlegen を配置します

        % ln -fs (kindlegen のディレクトリ)/kindlegen ./

4. 青空文庫の外字の画像を配置します

        % wget http://www.sumomo.sakura.ne.jp/~aozora/gaiji/gaiji.zip
        % unzip -x gaiji.zip 


実行方法
--------

インストールしたディレクトリに移動し、python aozoraxhtml2mobi.py を実
行します。引数には、青空文庫からダウンロードした XHTML のファイル名を
与えます。

変換が成功すると、mobi 形式のファイルが outout.mobi として生成されます。


技術的なこと
------------

青空文庫で配布されている XHTML は、そのまま kindle で表示することがで
きます。しかし、そのままでは、横書きで、左綴じです。このスクリプトは、
縦書き、右綴じにするために必要な最小限の変換を行います。


参考文献
--------

- Amazon Kindle Publishing Guidelines
  http://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf
