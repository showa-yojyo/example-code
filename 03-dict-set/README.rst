Sample code for Chapter 3 - "Dictionaries and sets"

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do

dialcodes.py
============

``dict`` オブジェクトの生成方法いろいろ。特に項目の順序指定について。

* いずれの生成方法でも ``==`` が成立する。

index.py vs index0.py vs index_default.py
=========================================

* ``dict.setdefault()`` あるいは ``collections.defaultdict()`` の指南。
* 正規表現マッチオブジェクトの ``.finditer()``

strkeydict.py vs strkeydict0.py
===============================

組み込み ``dict`` と ``collections.UserDict`` の継承を比較する。
テーマは辞書オブジェクトの初期値か要素の勘定だろう。

* ``__missing__()`` のオーバーロードで何か不吉なことをしている気がする。
* ``__contains__()``, ``__setitem__()`` はこのように実装する。
* ダメなほうは ``dict`` の継承で ``get()`` をオーバーライドすること。
  こうする代わりに ``__setitem__()`` で key を文字列に変換するようにした。

``UserDict`` は最近はあまり使われていないと聞く。

transformdict.py
================

これは長いサンプルだ。後回し。

support/
========

使えそうなコード・調べたいコードを重点的にチェックする。

* ``array.array('d')``
* ``1/random.random()``: NumPy などが使えればもっと良い浮動小数点数乱数生成関数があるだろうが、こういう手もある。
* ``timeit.repeat()`` 再び。``number`` と ``repeat`` の違いを理解すること。
* ``sys.argv.remove()`` か。モジュール ``argparse`` 未使用時ならではの技法だ。
* TODO: ``hash_diff()`` で何をしているか

以上
