Sample code for Chapter 6 - "Design patterns with first class functions"

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do

この章では Python 流の Strategy パターンを考察しているようだ。

classic_strategy.py
===================

GoF 式 Strategy パターンの実装例。

* ``Customer``: 顧客クラス
* ``LineItem``: 品物クラス
* ``Order``: 注文クラス
* ``Promotion``: 抽象メソッド ``discount()`` しかない抽象基底クラス。

  * ``FidelityPromo``: 値引きロジックその 1
  * ``BulkItemPromo``: 値引きロジックその 2
  * ``LargeOrderPromo``: 値引きロジックその 3

``Order`` が ``Promotion`` を持っている。
* ``Order.total()`` は ``ListItem.total()`` の和を単に計算するだけ。
* ``Order.due()`` で値引き後の金額を計算する。
  ``Promotion.discount(order)`` で上記総額から値引きする。
  値引きロジックは具象クラスの ``discount()`` が呼び出される。

実装の要点：

* ``Order.__repr__()`` を実装しておくことで ``print()`` で総額と値引き後総額が確認できる。
* 金額は浮動小数点数で扱っている。
* Python における抽象基底クラスの宣言方法： ``abc.ABC`` および ``@abc.abstractmethod``

strategy.py
===========

classic_strategy の内容のうち、``Promotion`` 以下はシンプルに関数で実装することができる
（それは ``Promotion`` が内部状態を持たないことが前提だ）。

``Promotion`` 以外のクラスの内容には変更が一切ないことに注意。

strategy_best.py
================

以下、戦略選択について議論する。
与えられた ``Order`` に対して値引き額が最大となるものを返せばよい。

最初のバージョンは関数 ``max()`` で ``promo(order)`` の最大値をとる ``promo`` を得る。
ただし対象となる集合はハードコードで与えられる。

strategy_best2.py
=================

さきほどのものは ``max()`` の引数となるリストが決め打ちだった。
これを ``globals()`` からなんとか ``_promo`` という名前のものを選択してそれを与えるように変更してある。

strategy_best3.py
=================

値引き関数がモジュール ``promotions`` に一括して定義されていると仮定する。
このときは標準モジュール ``inspect`` の機能が応用できる：

..code:: Python

  import inspect
  import promotions

  promos = [func for name, func in inspect.getmembers(promotions, inspect.isfunction)]

この利点は二つはある。一つはモジュール ``promotions`` で戦術を増減していいということだ。
もう一つは関数名についての制約が消えたことだ。

以上
