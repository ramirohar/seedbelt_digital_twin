import time 
def check_command(ard, comm, timeout = 2, verbose = True):
    t0 = time.time()
    while time.time() - t0 < timeout:
        if ard.get_data() == "OK":
            if verbose:
                print(comm + " excecuted")
            return 
        
    raise TimeoutError(comm + " not excecuted")

def clear_buf(ard, verbose = False):
    while True:
        data = ard.get_data()
        if data is None:
             break
        else:
            print(data)

def func(comm_func):
    def inner(ard, *args, **kwargs):
        comm = comm_func(*args, **kwargs)
        ard.send_command(comm)
        check_command(ard, comm, timeout=1)
    return inner

@func 
def nsteps(n):
    return f"NSTEPS {n}"

@func 
def mode(n):
    return f"MODE {n}"
