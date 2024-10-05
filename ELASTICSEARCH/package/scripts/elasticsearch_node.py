"""

"""
from resource_management.libraries.script.script import Script
from resource_management.core.logger import Logger
from resource_management import *


class ElasticsearchNode(Script):
    def install(self, env):
        # 在页面服务首次安装时自动执行的函数
        import params
        env.set_params(params)
        # self.install_packages(env)
        Logger.info('Start Install ELASTICSEARCH......')
        self.configure(env)
        File(path=os.path.join("/lib/systemd/system/elasticsearch.service", "elasticsearchnode.service.j2"),
             owner='root', group='root')
        Execute(command="systemctl daemon-reload", owner='root', group='root')
        Execute(command="systemctl enable elasticsearch", owner='root', group='root')
        Logger.info("Install complete")

    def configure(self, env):
        # 主要执行一些服务配置操作，该方法Ambari不会主动触发
        import params
        env.set_params(params)
        Logger.info('Start Setting ELASTICSEARCH......')
        elasticsearch(type='server')

    def start(self, env):
        # 在页面点击服务启动时自动执行的函数
        import params
        env.set_params(params)
        Execute('systemctl start elasticsearch', owner='root', group='root')

    def stop(self, env):
        # 在页面点击服务停止时自动执行的函数
        import params
        env.set_params(params)
        Execute('systemctl stop elasticsearch', owner='root', group='root')

    def status(self, env):
        # 检查服务状态，大概每隔60s执行一次
        import params
        env.set_params(params)
        Execute('systemctl status elasticsearch', owner='root', group='root')

    def restart(self, env):
        # 当文件内没有 restart() 方法的时候，程序会在重启的时候自动执行 stop() 和 start() 方法，以实现重启命令。
        # 当有 restart() 方法时，程序会在重启的时候执行 restart() 方法逻辑
        import params
        env.set_params(params)
        Execute('systemctl restart elasticsearch', owner='root', group='root')


def elasticsearch(type=None):
    import params
    Directory(user=params.es_user, group=params.user_group,
              path=[params.es_home, params.config_dir, params.es_data_dir, params.es_log_dir],
              create_parents=True)
    # 下载es包安装包
    Execute(
        'wget {0} -P {1} -O elasticsearch-7.11.2-linux-x86_64.tar.gz'.format((params.config_dir, params.es_home)))

    # 将安装包解压到指定目录
    Execute(format('tar -zxf {es_home}/elasticsearch-7.11.2-linux-x86_64.tar.gz -C {es_home}'))

    # 删除下载的安装包
    Execute(command='mv elasticsearch-7.11.2-linux-x86_64.tar.gz /tmp', user='root')

    # 初始化环境变量
    Execute(format("cuseradd {es_user} -g {user_group}"))
    Execute(format("cd {es_home}; chown -R {es_user}:{user_group} elasticsearch*"))
    configFile("elasticsearch.yml", template_name="elasticsearch.yml.j2")
    configFile("jvm.options", template_name="jvm.options.j2")
    Execute(
        format("ln -s {config_dir}/elasticsearch.yml {es_home}/elasticsearch-7.11.2/config/elasticsearch.yml"))
    Execute(
        format("ln -s {config_dir}/jvm.options {es_home}/elasticsearch-7.11.2/config/jvm.options"))


def configFile(name, template_name=None, mode=None):
    import params
    File(os.path.join(params.config_dir, name),
         content=Template(template_name),
         owner=params.es_user,
         group=params.user_group,
         mode=mode
         )


if __name__ == '__main__':
    ElasticsearchNode().execute()
