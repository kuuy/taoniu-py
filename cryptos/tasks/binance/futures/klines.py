from cryptos import celery

@celery.task(ignore_result=True)
def rank():
    print('rank')
