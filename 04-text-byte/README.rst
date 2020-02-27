======================================================================
Sample code for Chapter 4 - "Text and bytes"
======================================================================

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do

Unicode
======================================================================

先にこれを読んでおくといい：

https://docs.python.org/3.9/library/unicodedata.html#module-unicodedata

* 文字には正規形が二つ存在する。

  * 標準等価性

    * NFD: 標準分解。各文字を分解された形に変換する。
    * NFC: 標準分解を適用した後、結合済文字を再構成する。

  * 互換等価性

    * NFKD: 互換分解。すべての互換文字を等価な文字で置換する。
    * NFKC: 互換分解を適用してから標準分解を適用する。

default_encodings.py
======================================================================

実行結果をここに書くだけでメモになるのは楽だ：

.. code:: text

   locale.getpreferredencoding() -> 'cp932'
                   type(my_file) -> <class '_io.TextIOWrapper'>
                my_file.encoding -> 'cp932'
             sys.stdout.isatty() -> True
             sys.stdout.encoding -> 'utf-8'
              sys.stdin.isatty() -> True
              sys.stdin.encoding -> 'utf-8'
             sys.stderr.isatty() -> True
             sys.stderr.encoding -> 'utf-8'
        sys.getdefaultencoding() -> 'utf-8'
     sys.getfilesystemencoding() -> 'utf-8'

* ``str.rjust()`` でも文字列の右揃えができる。

normeq.py
======================================================================

``unicodedata.normalize()`` の実演。NFC, NFKC, NFD, NFKD から選んで「正規化」するようだ。

* カフェの比較が NFC の概念を端的に説明している。

numerics_demo.py
======================================================================

正規表現、文字列メソッド、モジュール ``unicodedata`` の関数による数値判定比較か。

* ``x`` なんとかや ``u`` なんとかで文字コードを指定して文字を指定できる。
* 組み込み関数 ``ord()`` で文字の Unicode コードポイント値を返す。
* 数値判定方法

  * 正規表現 ``r'\d'``
  * メソッド ``.isdigit()``, ``.isnumeric()``
  * ``unicodedata.numeric()`` はその文字が表す数値を浮動小数点数として返す。
    例えば「半分」を意味する文字に対してならば 0.5 が返るというわけだ。

* 文字の「名前」を ``unicodedata.name()`` で得られる。

.. code:: pycon

   >>> %run numerics_demo.py
   U+0031    1     re_dig  isdig   isnum    1.00   DIGIT ONE
   U+00bc    ¼     -       -       isnum    0.25   VULGAR FRACTION ONE QUARTER
   U+00b2    ²     -       isdig   isnum    2.00   SUPERSCRIPT TWO
   U+0969    ३     re_dig  isdig   isnum    3.00   DEVANAGARI DIGIT THREE
   U+136b    ፫     -       isdig   isnum    3.00   ETHIOPIC DIGIT THREE
   U+216b    Ⅻ     -       -       isnum   12.00   ROMAN NUMERAL TWELVE
   U+2466    ⑦     -       isdig   isnum    7.00   CIRCLED DIGIT SEVEN
   U+2480    ⒀     -       -       isnum   13.00   PARENTHESIZED NUMBER THIRTEEN
   U+3285    ㊅    -       -       isnum    6.00   CIRCLED IDEOGRAPH SIX

これは良質な教材だ。

ola.py
======================================================================

``coding: cp1252`` のテスト。

* VS Code などのテキストエディターで encoding を指定して開くといい。

ramanujan.py
======================================================================

正規表現はバイナリーデータに対しても機能する。

* このスクリプトの　Unicode で指定されている文字列がインド風味。
* ``re.compile(rb'\d+')`` などとして正規表現オブジェクトを生成する。
  あとで ``.findall()`` することで
* ``str.encode('utf-8')`` とすると ``str`` を ``bytes`` に変換して返す。
* この結果によると ``\d`` で match するものは ``\w`` でのそれらの部分集合である。

sanitize.py
======================================================================

変わった文字を ASCII 文字に置換する実演コード。
モジュール ``unicodedata`` を駆使している。

* 単純な置換ならば ``.replace()`` でよい。
* ``str.maketrans()`` を二度用いているが、両者で指示様式が明らかに異なる。
* ``.translate()`` により文字列中の文字の置換をいっぺんに済ませる。
* ASCII 化の仕上げに ``unicodedata.normalize()`` を NFKC モードで呼び出す。
* デモコードの「アサイー」の変換に注目すると意味がわかりやすい。

この実演コードは複雑かもしれない。

以上
