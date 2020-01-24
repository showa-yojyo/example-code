======================================================================
Sample code for Chapter 12 - "Inheritance: for good or for worse"
======================================================================

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do

diamond.py
======================================================================

ダイヤモンド継承の実演コード。

* ``D`` は ``B, C`` の順序で継承している。
* ``d.pong()`` すると実際には ``B.pong()`` が呼び出される。
  したがって ``d.pongpong()`` においては

  * ``self.pong()`` は ``B.pong()``
  * ``super().pong()`` も ``B.pong()``
  * ``C.pong()`` だけ ``C.pong()``

  がそれぞれ呼び出される。

.. code:: console

   bash$ python -c "from diamond import D; d = D(); d.pingpong()"
   ping: <diamond.D object at 0x0000019E2AC48548>
   post-ping: <diamond.D object at 0x0000019E2AC48548>
   ping: <diamond.D object at 0x0000019E2AC48548>
   pong: <diamond.D object at 0x0000019E2AC48548>
   pong: <diamond.D object at 0x0000019E2AC48548>
   PONG: <diamond.D object at 0x0000019E2AC48548>

以上
