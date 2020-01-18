Sample code for Chapter 1 - "The Python Data Model"

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do

frenchdeck.py
=============
* collections.namedtuple で簡易的にクラスを定義できる。
* 文字列を一文字ずつばらしたリストの作り方は ``list(text)``
* ``__len__()``, ``__getitem__()`` のオーバーロード例

vector2d.py
===========
* ``__repr__()`` の実装方針がよくわかる。
* ``__abs__(), __bool__(), __add__(), __mul__()`` のオーバーロード例
* 標準の ``math.hypot()`` は知っておくと良さそうだ。

doctest
=======
* 基本的だがリストのスライス。例：各色のエースだけを抽出できる
* ``deck`` に対して ``for`` ループ、``reversed()``, ``enumerate()`` が効くこと
* ``deck`` をランクに基づき ``sorted()`` できる。
  ``key`` 引数にランクを返す関数を与えればよい。

以上
