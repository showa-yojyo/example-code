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

flags*.py
----------------------------------------------------------------------

コードを少し読んで本書を読んだ記憶が思い出せた。
国旗イメージをダウンロードしまくる実演があったことを。

* flags.py は何の平行性もないコード。これが基本形となる。

  * Requests は使い勝手の良いサードパーティー製パッケージなのでインストールする。
  * ``get_flag()`` で画像データをコードとして扱う方法がわかる。
  * ``download_many()`` がおそらく改造されていく。

* flags_threadpool.py は基本形を改造して平行化したもの。

  * ``ThreadPoolExecutor`` は context manager なので ``with`` 文で使う。
  * 前にも見たが ``.map()`` で平行実行する。ここでは ``download_one()`` を指定。
    マルチスレッドで ``download_one()`` が処理されることが期待できる。

* flags_asyncio.py が非同期処理版だ。最新の書き方になっている。

  * 要 ``aiohttp`` モジュール。
  * ``asyncio.run()`` で ``download_many()`` を非同期呼び出しする？
  * ``download_many()``, ``download_one(), ``get_flag()`` は ``async`` 宣言されている。

    * ``async def`` な関数には ``await`` 文を含む処理がある。

  * ``get_flag()`` はファイルのダウンロードとバイト列の読み込み処理が変わった。

    * ``requests.get()`` を ``session.get()`` に変更。
      ``session`` は ``download_many()`` で確保したものを共通して使う。

  * ``download_one()`` は ``get_flag()`` の呼び出しに ``await`` が付いた。
    それ以外は変化なし。
  * ``download_many()`` は大幅に変更。

    * ``aiohttp.ClientSession`` 型の ``session`` オブジェクトを使うようになった。
      これは context manager なので ``with`` 文で使う。
      あとで HTTP GET するときに同じドメインにアクセスするのでこのやり方が有効だ。

    * ``await asyncio.gather()`` で複数タスクを一括処理すると読める。
    * 問題は ``download_one()`` の戻り値をなぜ ``asyncio.create_task()`` に引き渡すのかだ。
      元々 ``gather()`` が ``Task`` を受け取るようになっていたが、
      内部的に自動的に coroutine が ``Task`` に変換されるので実はいらない。

* ``aiohttp`` の機能としては ``ClientSession`` しか使っていないので、理解の心配はしなくていい。

* ``async def`` のついた関数を coroutine という。
  ``Task`` は coroutine から作るものとする。
* Awaitable であるとは ``await`` 文が書けるオブジェクトのことをいい、
  coroutines, ``Task``, ``Future`` が当てはまる。
* ``Future`` は低レベルなので一般プログラマーは直接作成しないらしい。

flags2*.py
----------------------------------------------------------------------

強化版？

* flags2_common.py: 以降のデモコードの共通要素をまとめたモジュール。

  * ``main()`` まで共通化するとは。
  * ここに ``save_flag()`` がある。

* flags2_sequential.py:

  * ``collections.Counter`` で HTTP リクエストの結果をステータスごとに勘定する。
  * ``tqdm`` なるモジュールは謎。ただ ``--verbose`` 時しか使われないから読み飛ばす。
  * ``download_many()`` は単にループで ``download_one()`` を呼び続けるだけ。
  * ``download_one()`` は ``get_flag()`` して ``save_flag()`` する処理を丁寧に書いたもの。
  * ``get_flag()`` も特に工夫なし。

* flags2_threadpool.py:

  * ``download_many()`` で ``ThreadPoolExecutor`` を使用。今までと使い方が異なる。

    * ループで ``executor.submit(download_one)`` を順次呼び出し
      ``Future`` オブジェクトをかき集める。
    * ``futures.as_completed()`` にかき集めたものを渡す。
      これが awaitable な物を concurrent に処理して ``Future`` オブジェクトを返すようだ。
    * ループで ``future.result()`` する。
      このタイミングで実際の処理が終わっていない可能性があることに注意。
      したがって ``try`` ブロックの中で処理することにしたのだろう。
  * ``download_one()`` は sequential 版を再利用。

* flags2_asyncio.py: 少し古い書き方をしているが問題ない。

  * ``download_many()`` では ``loop.run(downloader_coro)`` するだけでいい。
  * ``downloader_coro()`` は ``async`` 関数。

    * ``asyncio.Semaphore`` オブジェクトと ``aiohttp.ClientSession`` オブジェクトを
      後続の ``download_one()`` で使い回すのが急所。このやり方をよく覚えておく。

      * ``as_completed()`` するのは先ほどの実演コードと同じ。
      * ループで ``await future`` する。意味は先ほどと同じ。

  * ``download_one()`` で ``await get_flag()`` する際に
    ``semaphore`` を見るように変更したようだ。

  * ``get_flag()`` は ``async`` が付いて awaitble になった。

    * ``resp.read()`` に ``await`` が要る。同じ行で ``return`` できる。

demo_executor_map.py
======================================================================

旧ディレクトリーのものと同一の内容。

以上
