import falcon

def jwt_authentication(req, resp, resource, params, need_authentication):
    print(need_authentication)
    if need_authentication:
        print(need_authentication)
        raise falcon.HTTPUnauthorized('Auth token required')
        