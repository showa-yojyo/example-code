Sample code for Chapter 7 - "Closures and decorators"

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do

average.py, etc.
================

算術平均を計算する関数オブジェクト。

* クラス ``Averager`` と関数 ``make_averager()`` としてそれぞれ比較。内容は同じ。
* どちらも ``sum()`` し過ぎ。``total`` も記憶するべきなのだがこの際それはいい。
* 関数版のほうは ``.__code__`` や ``.__closure__`` といった特殊属性から情報を搾り取れる。
  * ``__closure__`` は関数の自由変数の情報を持っている。
  * ``__code__`` は関数のコードオブジェクトを表す。``.co_varnames`` や ``.co_freevars`` で細かい情報を得る。

clockdeco.py, etc
=================

* 関数 ``clock()`` は典型的な実行時間計測用デコレーター。
  * clockdeco.py のように既存関数の定義直前に ``@clock`` と書く。

* クラス ``clock`` は単にクラス版。``__init__()`` でちょっとした状態が持てるようになる。
  * ``__call__()`` の中身がデコレーターでの処理になる。
  * ``repr()`` や ``**locals()`` の使い方も参考になる。

* clockdeco_param.py は関数デコレーターに引数を付ける方法を示す。
  デコレーター関連の関数定義が深い入れ子になっていて驚く。

fibo.py, etc.
=============

見るべきは fibo_demo_lru.py のダブルデコレーター。

* ``@functools.lru_cache()`` でキャッシュが効くようになる。
  かつて同じ実引数で呼び出されたことがあれば、そのときの戻り値を返すだけで終わる。
  この実演内容は Fibonacci 数の計算だから効果は絶大だろう。

.. code:: text

   >>> %run fibo_demo_lru.py
   [0.00000000s] fibonacci(0) -> 0
   [0.00000000s] fibonacci(1) -> 1
   [0.00199962s] fibonacci(2) -> 1
   [0.00000000s] fibonacci(3) -> 2
   [0.02598715s] fibonacci(4) -> 3
   [0.00000000s] fibonacci(5) -> 5
   [0.02798557s] fibonacci(6) -> 8
   8

generic.py
==========

``functools.singledispatch`` の実演。実引数の型により処理を振り分ける。
これを活かせば ``if isinstance(...)`` みたいなコードを書かずに済む。

* 基本 (generic) な関数定義をまず書き、それを ``@singledispatch`` で修飾する。
  この例では ``htmlize()`` という関数で、引数は ``object`` 型を意図している。
* それから対応したい型ごとに個別に ``@htmilize.register(...)`` で修飾された関数定義を与える。
  * 関数名はやっつけ命名で同じでいい。
  * 複数の ``@htmilize.register(...)`` を付けてもいい。

registration.py, etc.
=====================

デコレーターでグローバルなコレクションオブジェクトに関数を格納する。

``registration_param.py`` がいちばん凝った実装だ。

strategy_best4.py
=================

前章の続き。各 strategy 関数を上述の技法でグローバルなリストに格納する。
関数 ``best_promo()`` はそのリストから ``max()`` を計算する。

以上
