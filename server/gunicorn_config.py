import os
import multiprocessing

port = os.environ.get("PORT", 5000)

bind = f"0.0.0.0:{port}"
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
timeout = 500
capture_output = True
enable_stdio_inheritance = True
reload = True

# Logging
loglevel = "debug"
accesslog = "stdout.log"
errorlog = "stderr.log"