import falcon
import jwt
from .constant import JWT_SETTINGS

def decode_jwt_header(jwt_token):
    try:
        if JWT_SETTINGS["PUBLIC_KEY"] is not None:
            decode = jwt.decode(jwt_token, JWT_SETTINGS["PUBLIC_KEY"], algorithms='RS256')
            return decode, "Success decode"
        elif JWT_SETTINGS["JWT_KEY"] is not None:
            decode = jwt.decode(jwt_token, JWT_SETTINGS["JWT_KEY"], algorithms='HS256')
            return decode, "Success decode"
        else:
            raise falcon.HTTPNotAcceptable(description='No JWT_KEY or PUBLICK_KEY provided')
    except Exception as error:
        return None, str(error)

def authentication_handler(request, jwt_secure):
    
    if not jwt_secure:
        return True, None
    elif jwt_secure and request.get_header('Authorization') is None:
        raise falcon.HTTPUnauthorized(title="AUTHORIZATION missing", description="AUTHORIZATION header missing")
    else:
        # clean header from Bearer
        jwt_token = request.get_header('Authorization').split()[1]
        decode, msg = decode_jwt_header(jwt_token)
        if decode is None:
            raise falcon.HTTPUnauthorized(title="JWT Rejected", description=msg)
        return True, request.get_header('Authorization')

def request_validation(request, url):
    if request.uri == url:
        raise falcon.HTTPLoopDetected(title="loop request", description="can't make request because infinite loop")
    else:
        return True