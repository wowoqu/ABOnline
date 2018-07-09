import threading
import time
from multiprocessing import Array, Value, Process


def func1(a, b):
    a.value = 3.333333333333333
    for i in range(len(b)):
        b[i] = -b[i]


if __name__ == "__main__":
    num = Value('d', 0.0)
    arr = Array('i', range(11))

    c = Process(target=func1, args=(num, arr))
    d = Process(target=func1, args=(num, arr))
    c.start()
    d.start()
    c.join()
    d.join()

    print(num.value)
    for i in arr:
        print(i)


def show(arg):
    time.sleep(1)
    print('thread' + str(arg))


for i in range(10):
    t = threading.Thread(target=show, args=(i,))
    t.start()

print('main thread stop')


def run(n):
    print('[%s]------running----\n' % n)
    # time.sleep(2)
    print('--done--')


def main():
    for i in range(5):
        t = threading.Thread(target=run, args=[i, ])
        # time.sleep(1)
        t.start()
        t.join(1)
        print('starting thread', t.getName())


m = threading.Thread(target=main, args=[])
m.setDaemon(False)  # 将主线程设置为Daemon线程,它退出时,其它子线程会同时退出,不管是否执行完任务
m.start()
# m.join(timeout=2)
print("---main thread done----")


def addNum():
    global num
    print('--get num:', num)
    time.sleep(1)
    num -= 1


num = 100
thread_list = []
for i in range(100):
    t = threading.Thread(target=addNum)
    t.start()
    thread_list.append(t)

for t in thread_list:
    t.join()

print('final num:', num)


def addNum():
    global num  # 在每个线程中都获取这个全局变量
    print('--get num:', num)
    time.sleep(1)
    lock.acquire()  # 修改数据前加锁
    num -= 1  # 对此公共变量进行-1操作
    lock.release()  # 修改后释放


num = 100  # 设定一个共享变量
thread_list = []
lock = threading.Lock()  # 生成全局锁
for i in range(100):
    t = threading.Thread(target=addNum)
    t.start()
    thread_list.append(t)

for t in thread_list:  # 等待所有线程执行完毕
    t.join()

print('final num:', num)


def do(event):
    print('start')
    event.wait()
    print('execute')


event_obj = threading.Event()
for i in range(10):
    t = threading.Thread(target=do, args=(event_obj,))
    t.start()

event_obj.clear()
inp = input('input:')
if inp == 'true':
    event_obj.set()


def consumer(cond):
    with cond:
        print("consumer before wait")
        cond.wait()
        print("consumer after wait")


def producer(cond):
    with cond:
        print("producer before notifyAll")
        cond.notifyAll()
        print("producer after notifyAll")


condition = threading.Condition()
c1 = threading.Thread(name="c1", target=consumer, args=(condition,))
c2 = threading.Thread(name="c2", target=consumer, args=(condition,))

p = threading.Thread(name="p", target=producer, args=(condition,))

c1.start()
time.sleep(2)
c2.start()
time.sleep(2)
p.start()
