from sven.api.wsgi import Server, Application
from sven.utils.config import Config


def main():
    config = Config('E:/Python_Project/sven/sven/sven.conf')
    app = Application(config)
    server = Server(app)
    server.run('0.0.0.0', 8000)


if __name__ == '__main__':
    main()
