from drScratch.celery import app


@app.task
def init_batch():
    print("----------------------- BATCH MODE CELERY ----------------------------------------------")
    