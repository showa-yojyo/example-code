Sample code for Chapter 8 - "Object references, mutability and recycling"

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do

bus.py
======

実演コードによるとコピーが主題のようだ。

クラス ``Bus`` の定義は ``list`` の軽いラッパーに過ぎず、見るべきところはない。

``copy.copy()`` と ``copy.deepcopy()`` の違いを示す。
オリジナルのバスからある乗客を下ろすと、前者のコピーバスからも当該客が消える。
一方後者のバスには当該客は乗車中のままだ。

cheese.py
=========

``weakref.WeakValueDictionary`` の振る舞いを示すものだ。

オリジナルオブジェクトを参照するものがすべて消滅したときに限り、
この辞書にあるオブジェクトも消滅する。C++ の ``weak_ptr`` みたいなものか。

haunted_bus.py
==============

bus.py のさらに雑なバージョンとなる。こういうコードを書いてはいけない。

特に ``HauntedBus.__init__()`` におけるデフォルト引数がまずい。
どうまずいのかは ``HauntedBus.__init__.__defaults__`` をトレースすればわかる。

こういうデバッグができるようになるので、Python の関数の特殊属性を習得するべきなのだ。

twilight_bus.py
===============

「委譲型」のバスを実装。``TwilightBus.__init__()`` に ``list`` を渡すと、
その中身の所有権がバスオブジェクトに移る。したがって実演コードのようにオリジナルの ``list`` からも乗客が消える。

以上
