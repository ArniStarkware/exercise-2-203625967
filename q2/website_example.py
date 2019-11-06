from webserver import WebServer


web_server = WebServer()


@web_server.route('/')
def index():
    return 200, '<html>users list</html>'


@web_server.route('/users/([0-9]+)')
def user(user_id):
    if user_id not in ['1', '2']:
        return 404, ''
    return 200, f'<html>user {user_id}</html>'


if __name__ == '__main__':
    web_server.run(('127.0.0.1', 8000))
