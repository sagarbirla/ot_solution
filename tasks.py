from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

import socket

app = Celery('tasks', 
              backend='amqp://<rmq_user>:<rmq_password>@<rmq_backend_ip>:<rmq_backend_port>/<rmq_backend_vhost>', 
              broker='amqp://<rmq_user>:<rmq_password>@<rmq_broker_ip>/<rmq_broker_vhost>')


#This function finds a random free non-standard (1025-65535) port on localhost
@app.task
def find_free_port():
    try:
        s = socket.socket()
        s.bind(('', 0))
        port = s.getsockname()[1]
        hostip = socket.gethostbyname(socket.gethostname())
        s.close()
        logger.info("Found port number {0} free on IP {1}.".format(port, hostip))
    except Exception as e:
        logger.warning("Could not find any free port on worker. Trying new worker")
        self.retry(countdown=2, exc=e)
    return [port, hostip]
