======================================================================
Sample code for Chapter 14 - "Iterables, iterators and generators"
======================================================================

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do

aritprog 系統
======================================================================

* aritprog_runner.py ではテストコードの一例が学べる。

  * ``glob.glob()`` を使って対象モジュールを決定する。
  * ``importlib.import_module()`` で動的にモジュールを import する。
    ただしあらかじめファイル名の拡張子をカットする必要がある。
  * ``getattr()`` で欲しい何かを動的に得る。今欲しいのは

    * ``ArithmeticProgression``
    * ``aritprog_gen``

  * ``doctest.testfile()`` は前述のとおり。

* artiprog_v*.py 系は NumPy の ``linspace()`` みたいなものを実装したいらしい。

  * ``ArithmeticProgression`` は iterator クラス

    * ``__init__()``, ``__iter__()`` のみ提供
    * ``_v1`` の ``__iter__()`` で数の増え方が変わる。

  * ``aritprog_gen()`` は関数スタイルの generator だ。

    * ``_v2`` の実装は ``_v1`` ベース。
    * ``_v3`` で非 iterator/generator 化。
      ``itertools.count()`` と ``itertools.takewhile()`` を導入。
      コードに少し癖がある。

* ``aritprog.rst`` で意図を確認。
  このファイルを ``doctest.testfile()`` することはできない。

fibo_by_hand.py
======================================================================

Fibonacci 数を返す関数やジェネレーターの典型的な実装が確認できる。

* 関数版もクラス版もコードをよく頭に叩き込んでおくこと。
* 呼び出し方も理解すること。
* クラス ``FibonacciGenrator`` と ``Fibonacci`` がなぜ分かれているのか。

  * この実装だとクラス ``Fibonacci`` を何重にも入れ子にできる。無意味だが。

sentence 系統
======================================================================

TBW

yield_delegate 系統
======================================================================

不思議な例だ。呼び出し側がジェネレーターを意識しないといけない例。
一時変数に戻り値を代入させないと無限ループに入る。

isis2json/
======================================================================

TBW

以上
