from application.workers import celery

@celery.task()
def test():
  print("INSIDE TEST TASK")
  print("HELLO NOUFAL")