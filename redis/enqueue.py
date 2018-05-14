from redis import Redis
from rq import Queue

from tasks import add


# localhost の TCPポート6379で待ち受けているRedisに接続する
# この2つの値はデフォルト値なので、省略しても良い
conn = Redis('localhost',6379)

# defaultという名前のQueueオブジェクトを取得する。
# この名前はデフォルト値なので、省略しても良い
q = Queue('default', connection=conn)

# 関数と引数を指定して、ジョブを追加する。
q.enqueue("tasks.add",3,4)
