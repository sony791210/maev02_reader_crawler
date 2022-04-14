


def sucess(data):
    return {
        "code":200,
        "data":data,
        "message":"請求成功"
    }

def fail(code,message):
    return {
        "code":code,
        "data":None,
        "message":str(message)
    }