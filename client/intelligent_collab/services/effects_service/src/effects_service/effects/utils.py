import psutil


def num_physical_cores():
    return str(psutil.cpu_count(logical=False))
