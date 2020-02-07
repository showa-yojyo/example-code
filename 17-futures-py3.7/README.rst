======================================================================
Updated sample code for Chapter 17 - "Concurrency with futures"
======================================================================

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do

This directory contains code updated to run with Python 3.7 and
**aiohttp** 3.5.   When the first edition of "Fluent Python" was
written, the **asyncio** package was provisional, and the latest
version of **aiohttp** was 0.13.1. The API for both packages had
significant breaking changes.

countries/
======================================================================

特別な準備が必要そうなので後回しか。コードだけでも読むか？

flags*.py
----------------------------------------------------------------------

コードを少し読んで本書を読んだ記憶が思い出せた。
国旗イメージをダウンロードしまくる実演があったことを。

* flags.py は何の平行性もないコード。これが基本形となる。

flags2*.py
----------------------------------------------------------------------

demo_executor_map.py
======================================================================

``ThreadPoolExecutor`` の実演。

* ``.map(func, args)`` で平行実行みたいなことになると想像に難くない。
* ``loiter()`` 内の ``sleep()`` は通常版。

以上
