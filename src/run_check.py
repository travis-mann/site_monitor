from multiprocessing import Process, Queue
import logging


class RunCheckTimeoutException(Exception):
    pass


def worker(func: callable, queue: Queue, *args, **kwargs):
    queue.put(func(*args, **kwargs))


def run_check(func: callable, timeout_sec: int, *args, **kwargs):
    """
    purpose: accepts a function to run as a child process and a timeout to prevent the process from
             running too long. Will return the same output as the given function
    """
    result_queue = Queue()
    child_process = Process(target=worker, args=(func, result_queue, *args), kwargs=kwargs)
    logging.info(f"starting child process for {func.__name__} with {timeout_sec} sec timeout")
    child_process.start()
    child_process.join(timeout_sec)

    # timeout occurred
    if child_process.is_alive():
        logging.info(f"{func.__name__} exceeded {timeout_sec} sec timeout. Terminating.")
        child_process.terminate()
        raise RunCheckTimeoutException

    # timeout did not occur
    return result_queue.get()



