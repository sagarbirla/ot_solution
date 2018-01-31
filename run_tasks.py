from tasks import find_free_port
import logging
import sys
import subprocess
import celery
from celery.exceptions import SoftTimeLimitExceeded
import time

logger = logging.getLogger('DeploymentLog')

hdlr = logging.FileHandler(filename='deployment.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

def deploy_app(port, ip, app_name = sys.argv[1]):
    #Running cmd to deploy app on remote machine
    logger.info("Deploying %s on %s:%s", app_name, ip, port)
    cmd = 'deploy ' + app_name + ip + port

    try:
        #cmd_return = subprcess.check_call(cmd, shell=True)
        #cmd_return = subprcess.check_call('exit 1', shell=True)
        logger.info("Successfully deployed app %s on %s:%s, app_name, ip, port")
    except Exception as e:
        logger.error("Deployment for %s got failed. Port on worker seems busy now. Re-enque job again", app_name)

if __name__ == '__main__':

    #Add job to find a free ip and port (on that server) to RabbitMQ
    try:
        async_result = find_free_port.apply_async(expires=60)
        time.sleep(0.1)
        result = celery.result.AsyncResult(async_result.task_id)
        port, ip = result.result
        deploy_app(str(port), str(ip))
    except SoftTimeLimitExceeded:
        logger.error("No worker retruned with free port. All sources are full")
