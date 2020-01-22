Sample code for Chapter 10 - "Sequence hacking, hashing and slicing"

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do

vector_v1.py
============

クラス Vector の実装再び。

* ``array.array`` のラッパーになった。``__init__()`` の実引数に柔軟性が生じる。
  これにより次元フリーになる。
* ``__repr__()`` の実装は ``eval()`` するとオブジェクトを生成できる文字列を返す。
  既存型オブジェクトの repr が欲しいならば ``reprlib.repr()`` を利用する。
* ``bytes`` のための各種インターフェイス

vector_v2.py
============

さらに ``__len__()`` と ``__getitem__()`` を実装。
重要なのは後者でスライスに対応していること。

.. code:: python

   def __getitem__(self, index):
        if isinstance(index, slice):
            return type(self)(._components[index])

vector_v3.py
============

``.x`` や ``.y`` を実装。このため ``__getattr__(), __setattr()__`` を実装。このため

簡略化するとこうだ：

.. code:: python

   def __getittr__(self, name):
       if name == 'x':
           return self._components[0]
       # ...

* ``__setattr__()`` は最後にオリジナルの処理を呼び出す。

  .. code:: python

     def __setattr__(self, name, value):
         # ...
         super().__setattr__(name, value)

* どちらも ``AttributeError`` を送出する可能性がある。

vector_v4.py
============

* ``__eq__()`` の実装では ``array`` の機能は使えないのかという疑問が生じる。
* ``__hash__()`` を実装。全成分の ``hash()`` 値を XOR するというものらしい。
  このため関数プログラミング的手法を採用する。

  .. code:: python

     functools.reduce(operator.xor, (hash(x) for x in self), 0)

vector_v5.py
============

* ``angle(), angles()`` でベクトルが各座標軸とのなず角を計算して返す。
* ``__format__()`` で円柱座標系と直交座標系をサポート。
  * ``{:h}`` で前者の座標成分表示を返す。この成分計算のために前述の角度メソッドが要るわけだ。

以上
