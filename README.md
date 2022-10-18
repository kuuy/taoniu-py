# taoniu-py
淘牛服务端（python）

# 异步任务处理
```shell
celery -A cryptos.celery beat -S redbeat.RedBeatScheduler
celery -A cryptos.celery worker -c 10 -l INFO -P gevent -Q cryptos.tasks.tradingview
```

# 运行
```shell
apt install -y python3-pip

python3 -m pip install --user --upgrade pip
~/.local/bin/pip install --user virtualenv
~/.local/bin/virtualenv venv

pip install -r requirements.txt
## pip install torch==1.12.0+cu116 torchvision==0.13.0+cu116 torchaudio==0.12.0 --extra-index-url https://download.pytorch.org/whl/cu116

pip install -e .
```