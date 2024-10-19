from resource_management import *
from resource_management.libraries.script.script import Script
import sys, os, glob, socket
from resource_management.libraries.functions.default import default

# server configurations
config = Script.get_config()

port = default('configurations/redis/port', '7000')
port_replica = default('configurations/redis/replica_port', '7001')
redis_user = default('configurations/redis/redis_user', 'redis')
db_path = default('configurations/redis/db_path', '/data/redis/data')
conf_path = config['configurations']['redis']['conf_path']
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]
redis_hosts = config['clusterHostInfo']['redis_node_hosts']
redis_hosts_str = ','.join(redis_hosts)
redis_current_host = socket.getfqdn(socket.gethostname())
server_cnf_content = config['configurations']['redis']['content']
redis_home = "/usr/bigdata/redis"
reposUrl = config['repositoryFile']['repositories']
baseUrl = ''
for url in reposUrl:
    if 'HDP-UTILS' in url['repoName']:
        baseUrl = url['baseUrl'].split('HDP')[0] + 'bigdatas/'
