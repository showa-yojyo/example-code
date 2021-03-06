======================================================================
Sample code for Chapter 2 - "An array of sequences"
======================================================================

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do

bisect_demo.py
======================================================================
標準 ``bisect.bisect_left()`` などの実例。

* ソート済みリストのどこに指定値を挿入するかを表す添字を返す。
* アスキーアート的出力が面白い。

.. code:: text

   >>> %run bisect_demo left
   DEMO: bisect_left
   haystack ->  1  4  5  6  8 12 15 20 21 23 23 26 29 30
   31 @ 14      |  |  |  |  |  |  |  |  |  |  |  |  |  |31
   30 @ 13      |  |  |  |  |  |  |  |  |  |  |  |  |30
   29 @ 12      |  |  |  |  |  |  |  |  |  |  |  |29
   23 @  9      |  |  |  |  |  |  |  |  |23
   22 @  9      |  |  |  |  |  |  |  |  |22
   10 @  5      |  |  |  |  |10
    8 @  4      |  |  |  |8
    5 @  2      |  |5
    2 @  1      |2
    1 @  0    1
    0 @  0    0

   >>> %run bisect_demo right
   DEMO: bisect_right
   haystack ->  1  4  5  6  8 12 15 20 21 23 23 26 29 30
   31 @ 14      |  |  |  |  |  |  |  |  |  |  |  |  |  |31
   30 @ 14      |  |  |  |  |  |  |  |  |  |  |  |  |  |30
   29 @ 13      |  |  |  |  |  |  |  |  |  |  |  |  |29
   23 @ 11      |  |  |  |  |  |  |  |  |  |  |23
   22 @  9      |  |  |  |  |  |  |  |  |22
   10 @  5      |  |  |  |  |10
    8 @  5      |  |  |  |  |8
    5 @  3      |  |  |5
    2 @  1      |2
    1 @  1      |1
    0 @  0    0

bisect_insort.py
======================================================================
標準 ``bisect.insort()`` 関数の使い方。

* ソート済みリストに指定要素をソート順を保ちつつ追加する関数だ。
* ``random.seed()`` をいつも同じ値で指定することで、乱数生成の再現性が担保される。
* 終端値の扱いが直感に反する ``random.randint()`` ではなく ``random.randrange()`` を使うこと。

listcomp_speed.py
======================================================================
リスト生成の最効率は何か。もちろん comprehension だ。

* ``timeit.repeat()`` をパフォーマンス測定に使う。文字列を引数としてとることに注意。
* 組み込み関数 ``map()`` は comprehension に完全に置き換えられる。
* 組み込み関数 ``filter()`` は comprehension に完全に置き換えられる。
* ``ord()`` で文字コードを得る。

metro_lat_long.py
======================================================================
おそらく ``format()`` の演習。

* tuple の list をループで回すときの一時変数への収納方法に注目したい。
* ``{:^9}`` の caret は中央寄せを意味する。

以上
