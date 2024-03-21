import time

def elap(ori_fun):
    def wrapper2():
        start = time.time()
        result = ori_fun()
        end = time.time()
        print('수행시간 %f 초' % (end - start))
        return result
    return wrapper2

def myfunc():
    print('1번 함수가 수행 되었다.')

    
decorated_func = elap(myfunc)
decorated_func()

@elap
def myfunc2():
    print('2번 함수가 실행됩니다')

myfunc2()