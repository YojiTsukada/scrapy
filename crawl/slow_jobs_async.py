import asyncio

async def slow_job(n):
    """
    引数で指定した秒数だけ時間のかかる処理を非同期で行うコルーチン。
    """

    print('Job {0} will take {0} seconds'.format(n))
    await asyncio.sleep(n) #n秒sleepする処理が終わるまで待つ。
    print('Job {0} finished'.format(n))

# イベントループを取得。
loop = asyncio.get_event_loop()

# 3つのコルーチンを作製。コルーチンはこの時点では実行するされない。
coroutines = [slow_job(1),slow_job(2),slow_job(3)]


# イベントループで3つのコルーチンを実行、終了まで待つ。
loop.run_until_complete(asyncio.wait(coroutines))