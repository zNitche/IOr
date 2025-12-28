import os, multiprocessing


bind = "0.0.0.0:8080"


workers = 2 * multiprocessing.cpu_count()
threads = multiprocessing.cpu_count()
worker_class = "gthread"

timeout = 30
keepalive = 10

keyfile = "key.pem" if os.path.exists("key.pem") else None
certfile = "cert.pem" if os.path.exists("cert.pem") else None

def ssl_context(conf, default_ssl_context_factory):
    import ssl

    context = default_ssl_context_factory()
    context.minimum_version = ssl.TLSVersion.TLSv1_3

    return context
