"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Ambari Agent

"""
import status_params
import os

from resource_management.libraries.functions import format
from resource_management.libraries.functions.version import format_stack_version
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.stack_features import check_stack_feature
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions import StackFeature
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.expect import expect

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

stack_root = status_params.stack_root

component_directory = status_params.component_directory

# New Cluster Stack Version that is defined during the RESTART of a Rolling Upgrade
version = default("/commandParams/version", None)

# default parameters
es_home = "/usr/bigdata/elasticsearch"
reposUrl = config['repositoryFile']['repositories']
baseUrl = ''
for url in reposUrl:
    if 'HDP-UTILS' in url['repoName']:
        baseUrl = url['baseUrl'].split('HDP')[0] + 'bigdatas/'
config_dir = "/etc/elasticsearch"
# config_file = "/etc/elasticsearch/conf"
es_smoke_pid = os.path.join(es_home, "elasticsearch.pid")

es_user = config['configurations']['elasticsearch.yml']['es_user']
es_lable = config['configurations']['elasticsearch.yml']['es_lable']
hostname = config['agentLevelParams']['hostname']
user_group = config['configurations']['cluster-env']['user_group']
es_env_sh_template = config['configurations']['elasticsearch.yml']['content']

es_log_dir = config['configurations']['elasticsearch.yml']['path.logs']
es_data_dir = config['configurations']['elasticsearch.yml']['path.data']
es_pid_dir = status_params.es_pid_dir
es_pid_file = status_params.es_pid_file

if 'elasticsearch.yml' in config['configurations']:
    es_yml_properties_map = config['configurations']['elasticsearch.yml']
else:
    es_yml_properties_map = {}

if 'jvm.options' in config['configurations']:
    es_jvm_properties_map = config['configurations']['jvm.options']
else:
    es_jvm_properties_map = {}

java64_home = config['ambariLevelParams']['java_home']
java_version = expect("/ambariLevelParams/java_version", int)

elasticsearch_hosts = config['clusterHostInfo']['elasticsearch_server_hosts']
elasticsearch_hosts.sort()
cluster_name = str(config['clusterName'])
