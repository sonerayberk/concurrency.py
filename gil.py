""" Let's code about GIL.

"GIL is bad", -- they said.

Thoughts about the GIL.

BTW >Python3.2 is cool as it released sys.setswitchinterval() to make a demo.

Nothing works in parallel on one CPU core.

CPU core are switching threads each fixed period of time.

GIL is not blocking IO operations: network, file read/write, DB etc.
GIL is released on that operations by OS system, OS threads take care about it.
GIL is not prevent concurrent model as GIL is released on blocking operations.
GIL is NOT preventing from logical errors: code_damage() function presents it.
GIL is for SAVE PYTHON INTERPETOR, PYTHON CODE.

CPU core is always swith the running threads.

GIL is just releasing the threads.

"""

import functools
import threading
import time
import typing
import sys


DEFAULT_SYSTEM_SWITCH_INTERVAL = sys.getswitchinterval()


def code_damage():
    global_list: typing.List[int] = [0, 1, 2, 3, 4]

    def get_value(_list, index) -> typing.Optional[int]:
        if len(_list) > index:
            # print('GIL now will release me')
            time.sleep(1)  # Sleep for a second

            # GIL acquire back current thread
            assert _list == []

            # return _list[index]
        else:
            return None

    def remove_values(_list) -> list:
        _list.clear()
        return _list  # Return: []

    # #############################
    # Let's interesting code begins

    sys.setswitchinterval(0.5)  # Release GIL after 0.5 seconds

    get_value_thread = threading.Thread(
        target=get_value, args=(global_list, 4)
    )  # Expected to return: 4
    remove_values_thread = threading.Thread(
        target=remove_values, args=(global_list,)
    )

    get_value_thread.start(); remove_values_thread.start()

    # TODO: handle get_value_thread exception
    get_value_thread.join(); remove_values_thread.join()


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        return end - start
    return wrapper


def die_threads():
    sys.setswitchinterval(DEFAULT_SYSTEM_SWITCH_INTERVAL)

    COUNTDOWN: int = 50_000_000

    def countdown(n):
        while n > 0:
            n -= 1

    @timer
    def run_in_one_thread():
        countdown(COUNTDOWN)

    @timer
    def run_in_two_threads():
        t1 = threading.Thread(target=countdown, args=(COUNTDOWN / 2,))
        t2 = threading.Thread(target=countdown, args=(COUNTDOWN / 2,))

        t1.start(); t2.start()
        t1.join(); t2.join()

    one_thread_timer_value = run_in_one_thread()
    two_threads_timer_value = run_in_two_threads()

    class huge(float):
        def __rshift__(self, other):  # <3
            # TODO: check via number exponent
            return super().__gt__(other)

    two_threads_timer_value = huge(two_threads_timer_value)

    assert two_threads_timer_value >> one_thread_timer_value  # MUCH bigger


def concurrent_execution():
    """ TODO: implement via concurrent.futures.ProcessPoolExecutor """


if __name__ == '__main__':
    code_damage()
    die_threads()
