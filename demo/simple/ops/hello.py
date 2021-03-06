from falsy.jlog.jlog import JLog

log = JLog().bind()

def get_it(name):
    log.debug('get it')
    return {
        'get': name
    }


def post_it(name):
    log.debug('post it')
    return {
        'post': name
    }


def delete_it(name):
    return {
        'delete': name
    }


def put_it(name):
    return {
        'put': name
    }


def patch_it(name):
    return {
        'patch': name
    }
