======================================================================
Sample code for Chapter 19 - "Dynamic attributes and properties"
======================================================================

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do

bulkfood/
======================================================================

* bulkfood_v1.py: よくあるクラス ``LineItem`` の実装だ。
  ``description``, ``weight``, ``price`` をメンバーデータに持ち
  メソッド ``.subtotal()`` は重さと単価の積を返す。

  ほぼ構造体に等しい。

* bulkfood_v2: v1 を調整したもの。``weight`` 周りを修正。

  * ``.__init__()``, ``.subtotal()`` は見かけ上は変更されていない。
  * ``.weight()`` が property 化された。この書き方をよく憶えること。

    * ``self.__weight`` の形で「本体」を保持ように変更。
    * ``@weight.setter`` 側に値テストを追加することで奇妙な値をとらないようにする。
      右辺値が正の数とみなされない値ならば ``ValueError`` を送出するように変更。

急所はアクセス方法が ``item.set_weight(value)`` のようにはせずに
``item.weight = value`` のまま上述のチェックを遂行できることだ。

* bulkfood_v2b: v2 の property 周りを変更したもの。

  * せっかくの ``@property`` を旧式の ``.get_weight()``, ``.set_weight()``
    に変更。ただし次の行をクラス内に追加する：

    .. code:: python

       weight = property(get_weight, set_weight)

* bulkfood_v2prop.py: 属性を外付けする。

  * まず関数 ``quantity()`` だ。メンバーデータ名を入力引数とする。
    返り値は get/set を含む ``property`` オブジェクトだ。

  * ``obj.name`` と ``obj.__dict__[name]`` は同値らしい。
  * ローカル関数の ``qty_getter()``, ``qty_setter()`` の signature が
    修正前の ``LineItem`` の対応物に同じであることを注意する。

oscon/
======================================================================

demo_schedule2.py
----------------------------------------------------------------------

後述 schedule2.py のクラスや関数を使う実演コード。ポイントは
``event.venue.name`` のようにして JSON の深い項目に（読み取り専用）アクセスするところだ。

.. code:: console

   bash$ ./demo_schedule2.py
   <Event 'There *Will* Be Bugs'>
   <DbRecord serial='venue.1449'>
   Portland 251
   speaker.3471: Anna Martelli Ravenscroft
   speaker.5199: Alex Martelli
   <property object at 0x00000254DA684B38>
   <Event 'Migrating to the Web Using Dart and Polymer - A Guide for Legacy OOP Developers'>
   <bound method DbRecord.fetch of <class 'schedule2.Event'>>
   <DbRecord serial='venue.1458'>

explore[0-2].py
----------------------------------------------------------------------

クラス ``FrozenJSON`` の実装だ。

* ``__init__()``: ``self.__data`` に引数とほぼ同じ ``dict`` を作る。

  * ただしキー名が Python の予約後と等しい場合は文字列を適宜修飾する。
    その際に関数 ``keyword.iskeyword()`` を利用する。

* ``__new__()`` をオーバーロードして引数の型によっては
  ``FrozenJSON`` オブジェクトを生成しないようにする。

  * 引数が is-a ``abc.Mapping`` のときはふつうに ``__init__()`` へ進む。
  * 引数が is-a ``abc.MutableSequence`` のときは、列の各要素を
    ``FrozenJSON`` オブジェクト化した列を新たに生成して返し、
    これは ``FrozenJSON`` オブジェクトにはならない。
  * それ以外のときには引数をそのまま返す。
    ``FrozenJSON`` オブジェクトにはならない。

* ``__getattr__()`` でおそらくドット演算子の振る舞いを実装している。
  指定された属性がほんとうに存在しない場合にのみ呼び出される。
  このクラスの use case では基本的にはその場合しかない。

  * 関数 ``hasattr()`` が ``True`` ならば既定の処理を行い、
    そうでなければ新たに ``FrozenJSON`` オブジェクトを生成して返す。
    この仕様が frozen をクラス名に冠する所以だ。

  * このメソッドが呼び出されているということは ``hasattr()`` が
    ``False`` ということだから、この中でこの関数を呼ぶ意味はないことにならないか。

osconfeed.py
----------------------------------------------------------------------

O'reilly のサイトから特定のファイルを必要ならばダウンロードして
``data/osconfeed.json`` の名前で保存するスクリプトだ。

* ``warnings.warn()`` はこういうところで使える。
* ``with`` 文は一行に複数の manager オープンコードを書ける。
* ファイルから JSON オブジェクトを生成するには
  関数 ``json.load()`` を利用する。

Python では JSON オブジェクトを取り扱うときには
このスクリプトの docstring にあるように、角括弧だらけのコードが増産される。

schedule[12].py
----------------------------------------------------------------------

上述の JSON データから Schedules 項目を加工して ``shelve`` オブジェクトにロードする。

* Python 標準の ``shelve`` に馴染みがない。データベースらしい。
* クラス ``Record`` は ``self.__dict__`` をそのまま流用するのが基本方針だ。

  * ``__eq__()`` をオーバーロードする必要があるのはなぜか。

* クラス ``DbRecord`` は ``Record`` を特殊化したものだ。

  * メソッド群を見ると singleton 指向？
  * メソッド ``fetch()`` の例外処理が奇妙に見える。
    ``KeyError`` を捕捉するのが第一感だが。
  * ``__repr__()`` をオーバーロードしてデバッグ用出力文字列を決める。
    この際 ``'serial'`` があれば特別扱いをする。

* クラス ``Event`` はさらに ``DbRecord`` を特殊化したものだ。

  * JSON データの venue と speakers に特に興味があるので、これらを
    property として扱う。

* 関数 ``load_db()`` の最終版は面倒なことになる。
  入力として JSON ファイルの中身を使い、

  * 文字列を基に今から生成するオブジェクトの型、クラスを決定する。
    ``globals()`` にその名前があればそれを、そうでなければ
    ``DbRecord`` を採用したい。
  * それが ``DbRecord`` のサブクラスならば本採用。
    関数 ``issubclass()`` を呼び出すためには ``inspect.isclass()``
    で最低限クラスであることを確認しておく。
  * オブジェクト ``db`` にコンストラクターで生成したオブジェクトを格納する。

blackknight.py
======================================================================

``@.deleter`` の実演コード。
オブジェクトの特定の property を ``del`` するときの振る舞いを書けるらしい。

実演方法：

.. code:: console

   $bash python -m doctest -v blackknight.py

doc_property.py
======================================================================

``.__doc__``, ``.__dict__``, ``@property`` の実演コード。

* わざわざ ``@property``, ``@.setter`` を使って属性値のアクセスをカスタマイズする。
* ``self.__dict__`` にオブジェクトの属性がまとめてあると読める。
* ``__doc__`` はオブジェクトに対する help 用の文字列を表す。

このコードで興味深いのは

* ``f.bar = 77`` の行を削っても動作するということ。
* ``Foo.bar.__doc__`` と ``f.__doc__`` は異なるということ。

pseudo_construction.py
======================================================================

これは擬似コードだ。
`__new__()` と `__init__()` の意味を明らかにするためのものらしい。

これによるとコンストラクターは最初に指定クラスのクラスメソッドである `__new__()` を指定の引数で呼び出す。
返り値が指定クラスの型 (is-a) であるならば、そのまま指定クラスの `__init__()` を指定の引数で呼び出す。

* `isinstance()` が `False` のときはどのクラスの `__init__()` も呼び出されないことになる。

以上
