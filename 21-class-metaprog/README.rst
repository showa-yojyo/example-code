======================================================================
Sample code for Chapter 21 - "Class metaprogramming"
======================================================================

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do


bulkfood/
======================================================================

最終バージョン。

bulkfood_v*.py
----------------------------------------------------------------------

クラス ``LineItem`` に ``@model.entity`` decorator が付いた。
後述するようにメンバーデータの ``.storage_name`` に適宜名前が付く。

あるいは ``LineItem`` のサブクラスを ``model.Entity`` とする。
後述するように同じ効果が得られるように関連メタクラス群が実装されている。

``LineItem`` に対してクラスメソッドとして ``field_names()`` を呼び出すと
各メンバーデータの ``storage_name`` が返る。

model_v*.py
----------------------------------------------------------------------

クラス ``AutoStorage``, ``Validated``, ``Quantity``, ``NoBlank`` は
対応する前章の最終版とそれぞれ同一内容だ。

関数 ``entity()`` は型を受け取って ``Validate`` 型のメンバーデータ
``.storage_name`` にその型の名前と連番を含む文字列を代入する。

クラス ``EntityMeta`` は ``type`` を継承するメタクラス（クラスを生成するクラス）だ。

* ``__init__()`` の signature に注意。第一引数は ``cls`` だ。``self`` ではない。
* 処理内容は関数 ``entity()`` の主要部と同じだ。

  * 修正版では対象クラスの ``_field_names`` に辞書のキーを収納する。
  * 修正版では ``@classmethod`` として ``__prepare__()`` を定義する。
    空の ``collections.OrderedDict`` オブジェクトを返すだけのものだ。
    どう使われるかは実演コードで調べる。

クラス ``Entity`` は ``metaclass=EntityMeta`` によるサブクラスだ。
初期版では中身は空だが最終的に ``@classmethod`` として ``field_names()`` を実装する。
対象クラスの ``_field_names`` の内容を一つずつ yield する。

eval 系
======================================================================

クラスを継承するときの ``metaclass=XXX`` についての実演コード。
サブクラスを定義するときはふつうは丸括弧の中にスーパークラスを直接指定する。
ここではその代わりに ``metaclass=XXX`` を指定する。

``XXX`` は ``type`` のサブクラスを指定するのがふつうだ。ここでもそうしている。

* evalsupport.py

  * 関数 ``deco_alpha`` はクラスに対する decorator として定義している。
    これにより ``method_y()`` なるメソッドが修飾されるクラスに自動的に定義される。
  * クラス ``MetaAleph`` は ``type`` を基底クラスとする特殊なものらしい。
    これにより ``__init__()`` が呼び出されるならば、クラスに対して
    ``method_z()`` なるメソッドが実行時に追加される。

    * ``__init__()`` の第一引数が ``self`` ではなく ``cls`` となっている。
      これを見落としてはならない。

* evaltime.py: これはここまでの本書の内容で説明できる。

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
  * ``three.method_y()`` の呼び出しに注意。上述の decorator に上書きされた
    本来の ``print('<[8]> ClassThree.method_y')`` をするほうは消える。
  * ``four.method_y()`` は ``ClassThree`` を継承しているがオーバーライドをしているために
    ``print('<[10]> ClassFour.method_y')`` するほうが呼び出される。

* evaltime_meta.py: TBW

  .. code:: text

     bash$ ./evaltime_meta.py
     <[100]> evalsupport module start
     <[400]> MetaAleph body
     <[700]> evalsupport module end
     <[1]> evaltime_meta module start
     <[2]> ClassThree body
     <[200]> deco_alpha
     <[4]> ClassFour body
     <[6]> ClassFive body
     <[500]> MetaAleph.__init__
     <[9]> ClassSix body
     <[500]> MetaAleph.__init__
     <[11]> ClassThree tests ..............................
     <[300]> deco_alpha:inner_1
     <[12]> ClassFour tests ..............................
     <[5]> ClassFour.method_y
     <[13]> ClassFive tests ..............................
     <[7]> ClassFive.__init__
     <[600]> MetaAleph.__init__:inner_2
     <[14]> ClassSix tests ..............................
     <[7]> ClassFive.__init__
     <[600]> MetaAleph.__init__:inner_2
     <[15]> evaltime_meta module end

  * 同じ理由で ``ClassThree.method_y()`` として本来の
    ``print('<[3]> ClassThree.method_y')`` の処理は decorator 版が呼び出される。
  * 同じ理由で ``ClassFour.method_y()`` として本来の
    オーバーライド版である ``print('<[5]> ClassFour.method_y')`` が呼び出される。
  * ``ClassFive.__init__()`` は自身のそれと ``MetaAleph`` のそれがこの順に呼び出される。
  * ``five.method_z()`` として ``MetaAleph.__init__()`` で動的にオーバーライドされた
    メソッドが呼び出されて、本来のものは消える。
  * ``ClassSix`` は ``ClassFive`` を継承して、かつ ``method_z()`` を
    オーバーライドしているが、基底クラスの ``__init__()`` でメソッドが
    動的にオーバーライドされる。したがって ``six.method_z()`` としては
    ``print('<[10]> ClassSix.method_y')`` のものが呼び出されない。

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
