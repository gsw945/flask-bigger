# -*- coding: utf-8 -*-
'''部署阶段-启动文件'''
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from run import start_server


if __name__ == '__main__':
    run_cfg = {
        'host': '0.0.0.0',
        'port': 5556
    }
    wsgi_app = start_server(run_cfg, is_deploy=True)
    host = run_cfg['host']
    port = run_cfg['port']
    http_server = HTTPServer(WSGIContainer(wsgi_app))
    http_server.listen(port, address=host)

    IOLoop.instance().start()