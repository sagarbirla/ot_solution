<h1> Workload Balancer </h1>

<h3> Setup Broker </h3>
apt-get update

apt install python-pip

pip install celery

apt-get install rabbitmq-server

<h3> Setup RabbitMQ Users and Permissions </h3>
rabbitmqctl add_user <user_password>

rabbitmqctl add_vhost test_broker_vhost

rabbitmqctl add_vhost test_backend_vhost

rabbitmqctl set_permissions -p test_broker_vhost "." "." ".*"

rabbitmqctl set_permissions -p test_backend_vhost "." "." ".*"

Restart RabbitMQ

<h3> Setup Worker </h3>
apt-get update

apt install python-pip

pip install celery

Run workers on all servers in background: nohup celery -A tasks worker --loglevel=info & > /tmp/celery_worker.out

<h3> Start a job </h3>
On control server: python run_tasks.py <app_name>
