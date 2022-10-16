# taoniu-py
淘牛服务端（python）

# 异步任务处理
```shell
celery -A cryptos.celery beat -S redbeat.RedBeatScheduler
celery -A cryptos.celery worker -c 10 -l INFO -P gevent -Q cryptos.tasks.tradingview
```