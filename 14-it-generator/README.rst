======================================================================
Sample code for Chapter 14 - "Iterables, iterators and generators"
======================================================================

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do

おさらい
======================================================================

* 大前提として Python には iterable という概念がある。

  * ``__iter()__`` を備えていることが条件だ。例えば次は iterable だ：

    * ``list()``
    * ``tuple()``
    * ``dict()``
    * ``set()``, ``frozenset()``
    * ``str()``, ``bytes()``, ``bytearray()``
    * ``range()`` などのそれらしいもの

  * Iterable の真の定義は ``isinstance(X, collections.abc.Iterable)`` なる
    ``X`` のことだ。

* Iterator とは ``__iter__()`` と ``__next__()`` を備えたクラスのオブジェクトだ。
  したがって iterator is-an iterable が成り立つ。

  .. code:: pycon

     >>> from collections.abc import (Iterable, Iterator)
     >>> issubclass(Iterator, Iterable)
     True

  * 真の定義は ``isinstance(X, collections.abc.Iterator)`` なる
    ``X`` のことだ。
  * 任意の iterable ``X`` から iterator を得ることができる。
    それには ``iter(X)`` とする。
  * このときの ``__iter()__`` はふつうは ``return self`` しかしない。
    ``__next()__`` で何かを ``return`` するか ``StopIteration`` を送出するかする。
  * しかしこういうクラスは実装するのがたいへんだ。

* Generator とは Iterator の一種であり Iterator オブジェクトを「返す」何か。

  * ``type(X)`` が ``generator`` を返すような ``X`` は generator だ。
  * ``(g(i) for i in S)`` の形をとるものも generator だ。
  * ``yield`` を含む callable の形をしているものが generator だ。

以上を踏まえてコードを読み解いていく。

aritprog 系統
======================================================================

* aritprog_float_error.py

  * 組み込み関数 ``iter()`` でコレクションから iterator を得る。
    ``iter()`` はふつう iterable を受け取って対応する iterator を返す。

* aritprog_runner.py ではテストコードの一例が学べる。

  * ``glob.glob()`` を使って対象モジュールを決定する。
  * ``importlib.import_module()`` で動的にモジュールを import する。
    ただしあらかじめファイル名の拡張子をカットする必要がある。
  * ``getattr()`` で欲しい何かを動的に得る。今欲しいのは

    * ``ArithmeticProgression``
    * ``aritprog_gen``

  * ``doctest.testfile()`` は前述のとおり。

* artiprog_v*.py 系は浮動小数点数の誤差を見せるためのコード。

  * v0 の ``ArithmeticProgression`` は iterable どまり。

  * v1 の ``ArithmeticProgression`` は iterator といえる。

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

* ``FibonacciGenrator`` は iterator だが
  ``Fibonacci`` は単なる iterable に過ぎない。
* 関数 ``fibonacci()`` の戻り値が generator だ。

sentence 系統
======================================================================

クラス ``Sentence`` の意図は文字列の形で文章を受け取り、その単語ごとに iterate するというものだ。
この仕様からこのクラスが Iterator であることがわかる。

* sentence.py

  * ``__getitem__()``, ``__len()__`` を提供しているので ``s[index]`` と ``len(s)`` が許される。
  * ``__repr__()`` の実装に ``reprlib.repr()`` を利用。
  * テキストを単語列に変換するのに単純に正規表現を利用。

    .. code:: python

       words = r'\w+'.findall(text)

* sentence_gen*.py

  * ``Sentence`` が ``yield`` を含む ``__iter__()`` を実装している。
  * 単語列をループで回して ``yield`` する実装
  * ``finditer()`` の各オブジェクトの ``.group()`` を ``yield`` する実装
  * 丸括弧記法による上記と同じものを ``return`` する実装

* sentence_iter*.py

  * ``Sentence`` と ``SentenceIterator`` の二本柱で行く場合には
    前者に ``__iter__()`` を提供して単に ``SentenceIterator(words)`` を返す。
    後者に ``__iter__()`` と ``__next()__`` を実装して iterator とする。
    それぞれの実装内容は aritprog で述べたのと同様。
  * ``SentenceIterator.__next__()`` の実装が泥臭いことに注意。

* sentence_runner.py については aritprog_runner.py のメモ参照。

yield_delegate 系統
======================================================================

不思議な例だ。呼び出し側がジェネレーターを意識しないといけない例。
一時変数に戻り値を代入させないと無限ループに入る。

isis2json/
======================================================================

何かのファイルの JSON ファイルへのコンバーター。

Iterator/generator 以外の注意点を挙げる：

* isis2json.py: コマンドラインインターフェースを有するスクリプト

  * ``ArgumentParser`` をしっかり利用。
  * 関数 ``iter_iso_records`` だけ調べればいい。

    * ``dict.setdefault(key, [])`` みたいな使い方は覚えておきたい。

  * ``uuid.uuid4()`` は面白い。``str()`` して使うのがふつうらしい。

* iso2709.py: 主題に沿う研究対象はこのファイルか？

  * クラス ``IsoFile`` に ``__iter__()`` と ``__next__()`` あり。
    前者は ``return self`` だけで後者も単に ``return IsoRecord(self)`` する。
    クラス自体はファイルを読み込みモードで開く操作をラップしたもの。
    バイナリーモードで処理する。

    * ``for record in IsoFile(...)`` で ``IsoRecord`` オブジェクトに順次アクセスできるわけだ。

  * クラス ``IsoRecord`` も同じ仕組みの iterator だ。

* subfield.py: Python 2 専用コードらしいので研究の対象外。

以上
