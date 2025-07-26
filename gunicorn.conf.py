import multiprocessing


bind = "0.0.0.0:8080"


workers = 2 * multiprocessing.cpu_count()
threads = multiprocessing.cpu_count()
worker_class = "gthread"

timeout = 30
keepalive = 10
