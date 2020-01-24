======================================================================
Sample code for Chapter 11 - "Interfaces, protocols and ABCs"
======================================================================

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do

bingo.py
======================================================================

クラス ``BingoCage`` のコード。基底クラスが ``Tombola`` なのでそちらを先に見る。

* ``load()`` と ``pick()`` がオーバーライド。
  基底クラスの ``inspect()`` のためだけにあるメソッドか？

  * ``list.pop()`` の例外を ``IndexError`` から ``LookupError`` に変更

* ``random.SystemRandom.shuffle()`` とは
* ``__call__()`` で ``pick()`` に転送。丸括弧一発で呼び出せる便宜を図る。

drum.py
======================================================================

クラス ``TumblingDrum`` のコードで、基底クラスが同じく ``Tombola`` だ。
こちらはそれほど見るものはない。

frenchdeck2.py
======================================================================

``collections.MutableSequence`` ベースのクラス ``FrenchDeck2`` のコード。
以前見た内容と同じはず。

lotto.py
======================================================================

クラス ``LotteryBlower`` のコードで、基底クラスが同じく ``Tombola`` だ。

* ここでは ``ValueError`` から ``LookupError`` に変換。

tombola_runner.py
======================================================================

スクリプトコード。たいへん興味深い。

* ``Tombola.__subclasses()__`` でこのクラスの派生クラスをすべて得られる。これは使ったことがある。
* ``Tombola._abc_registry`` で仮想派生クラスなるものを得られるようだ。
* 関数 ``test()`` でクラスに対するテストを行う。

  * テストの内容は ``doctest.testfile()`` による。ドキュメント参照。

    https://docs.python.org/ja/3/library/doctest.html

tombola_subhook.py
======================================================================

クラス ``Tombola`` のコード。

* 基底クラスが ``abc.ABC``
* ``load()`` と ``pick()`` を抽象メソッドとするため ``@abc.abstractmethod`` で修飾。
* クラスメソッドとして ``__subclasshook__()`` を定義。引数がこのクラスのサブクラスかどうかを決定する。
  これと ``__mro__`` についてはドキュメント参照。

  https://docs.python.org/ja/3/library/abc.html

* 関数 ``function_names()`` でオブジェクトの関数を返すようだ。
  ``inspect.getmembers()``, ``inspect.isfunction()``

  https://docs.python.org/ja/3/library/inspect.html

tombola_test.rst
======================================================================

コンソールで ``bash$ python -m doctest tombola_test.rst`` とすればテストできる。

tombola.py
======================================================================

``tombola_subhook.py`` のほうが上等なので読まなくていい。

tombolist.py
======================================================================

クラス ``TomboList`` のコード。クラスデコレーター ``Tombola.register`` を使いたい。

* このクラスの基底クラスは ``list`` になっている。それを動的に ``Tombola`` にするということか。
* コード的な理解は問題ないが、Python の場合は動的サブクラス化の利点がよくわからない。

以上
