# -*- coding: utf-8 -*-
'''数据库迁移配置'''
import sys

from flask_script import (
    Manager,
    Server
)
from flask_migrate import (
    Migrate,
    MigrateCommand
)

from run import start_server


if __name__ == '__main__':
    # 解析参数
    parser = Server().create_parser()
    ns = vars(parser.parse_known_args(sys.argv)[0])
    host = ns.get('host', '127.0.0.1')
    port = ns.get('port', 5556)
    is_debug = ns.get('use_debugger', False)
    is_threaded = ns.get('threaded', False)
    # 获取应用(app)
    run_cfg = {
        'host': host,
        'port': port,
        'debug': is_debug,
        'threaded': is_threaded
    }
    app = start_server(run_cfg, is_deploy=True)
    # 命令配置
    migrate = Migrate(app, app.db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.run()