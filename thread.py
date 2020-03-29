import threading

def main():
    print("STARTING...")

    thread1 = threading.Thread(target=myFunction, args=("andy",))
    thread2 = threading.Thread(target=loop, args=(2,10))
    thread3 = threading.Thread(target=loop, args=(3,10))


    thread1.start()
    thread2.start()
    thread3.start()

    thread2.join()
    thread3.join()


def myFunction(name):
    print("hello", name)

def loop(idx, n):
    for i in range(n):
        print(idx, "->", i)


if __name__ == "__main__":
    main()