======================================================================
Sample code for Chapter 21 - "Class metaprogramming"
======================================================================

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do


bulkfood/
======================================================================

TBW

eval 系
======================================================================

* evalsupport.py

  * 関数 ``deco_alpha`` はクラスに対する decorator として定義している。
    これにより ``method_y()`` なるメソッドが修飾されるクラスに自動的に定義される。
  * クラス ``MetaAleph`` は ``type`` を基底クラスとする特殊なものらしい。
    これにより ``__init__()`` が呼び出されるならば、クラスに対して
    ``method_z()`` なるメソッドが実行時に追加される。

* evaltime.py

  .. code:: text

     bash$ ./evaltime.py
     <[100]> evalsupport module start
     <[400]> MetaAleph body
     <[700]> evalsupport module end
     <[1]> evaltime module start
     <[2]> ClassOne body
     <[6]> ClassTwo body
     <[7]> ClassThree body
     <[200]> deco_alpha
     <[9]> ClassFour body
     <[11]> ClassOne tests ..............................
     <[3]> ClassOne.__init__
     <[5]> ClassOne.method_x
     <[12]> ClassThree tests ..............................
     <[300]> deco_alpha:inner_1
     <[13]> ClassFour tests ..............................
     <[10]> ClassFour.method_y
     <[14]> evaltime module end
     <[4]> ClassOne.__del__

  * ``__main__`` の一行目までが長い。
  * ``three.method_y()`` の呼び出しに注意。

* evaltime_meta.py: TBW

factories.py
======================================================================

``collections.namedtuple`` のようなものを自前で実装する実演コードだ。

* クラス名と引数名のリストを引数にとる関数の形で実装する。
* 本体は Python 組み込み関数の ``type()`` だ。ここにクラス名、基底クラス、属性の辞書を与えて終わり。

  * 基底クラスは ``object`` 固定。Python の既定の基底クラスだ。
  * 属性として引数名リストを ``__slot__`` とする以外に
    ``__init__()``, ``__iter__()``, ``__repr__()`` をここで作って渡す。

    * ``__init__()`` は slots と ``setattr()`` を使ってメンバーデータをオブジェクト
      ``self`` に安定させる。
    * ``__iter__()`` はおまけのようなもので、メンバーデータを適当に iterate する。
      メンバーデータ名が slots に全部あるのでループで回して ``getattr()`` で参照する。

以上
