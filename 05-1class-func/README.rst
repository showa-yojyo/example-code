Sample code for Chapter 5 - "First-class functions"

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do

bingocall.py
============
クラス ``Bingo`` を定義する。

* わざわざクラスにするような内容でもなさそうだが ``__call__()`` が地味にうれしい。
* ``list.pop()`` の例外型が ``IndexError`` だとは。
  その違和感は著者も持っているようで、``LookupError`` に変換して送出することにしたようだ。

clip.py vs clip_annot.py
========================
関数定義時に signature にゴチャゴチャと注釈を付すことがオプションでできるようだ。
しかし関数機能はまったく変化がないようだ。

.. code:: text

   >>> clip?
   Signature: clip(text: str, max_len: 'int > 0' = 80) -> str
   Docstring:
   Return text clipped at the last space before or after max_len

   File:      ...clip_annot.py
   Type:      function

* 関数自体から ``__code__``, ``__defaults__`` などのプロパティーが得られる。
* ``inspect.signature()`` で関数の仕様を得られる。
  * ``.return_annotation``
  * ``.parameters``

.. code:: text

   >>> sig = signature(clip)
   >>> sig.return_annotation
   str

   >>> sig.parameters
   mappingproxy({'text': <Parameter "text: str">,
                 'max_len': <Parameter "max_len: 'int > 0' = 80">})


tagger.py
=========
関数を引数リストに注目して定義する。
位置引数、可変長位置引数、デフォルト引数、可変長キーワード引数の混合。

* ``*args`` も ``**kwargs`` も実引数がまったくない呼び出しが普通にあり得ることに注意する。

以上
