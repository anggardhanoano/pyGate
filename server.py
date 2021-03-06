import falcon
from falcon_multipart.middleware import MultipartMiddleware
from wsgiref import simple_server

from gateway.utils import GatewayUtil
from gateway.resource import GatewayResource
# falcon.API instances are callable WSGI apps


def create_server(service_json):
    app = falcon.API(middleware=[
        MultipartMiddleware()
    ])

    gateway = GatewayUtil(service_json)

    urls = gateway.urls
    for url in urls:
        resource = GatewayResource(url["service_url"], url["jwt_secure"])
        app.add_route(url["url"], resource)
    
    return app, urls

if __name__ == '__main__':

    host = '127.0.0.1'
    port = 8000

    app, urls = create_server('service.json')

    print('=================================================================================')
    print("GATEWAY is Running on " "http://" + host + ":" + str(port))
    print('---------------------------------------------------------------------------------')
    print("LIST of ENDPOINT")
    for url in urls:
        print(url["url"] + " - " + "JWT Secured: " + str(url["jwt_secure"]) + " - " + "Service URL: " + url["service_url"])
    print('=================================================================================')

    httpd = simple_server.make_server(host, 8000, app)
    httpd.serve_forever()