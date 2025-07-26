import os, ssl, multiprocessing


bind = "0.0.0.0:8080"


workers = 2 * multiprocessing.cpu_count()
threads = multiprocessing.cpu_count()
worker_class = "gthread"

timeout = 30
keepalive = 10

keyfile = "key.pem" if os.path.exists("key.pem") else None
certfile = "cert.pem" if os.path.exists("cert.pem") else None

__is_ssl_enabled = True if keyfile is not None and certfile is not None else False

ssl_version = ssl.PROTOCOL_TLS if __is_ssl_enabled else None
cert_reqs = True if __is_ssl_enabled else False
