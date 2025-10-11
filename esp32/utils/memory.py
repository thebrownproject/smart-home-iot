import gc

class Memory:
    def __init__(self):
        pass

    def collect(self, reason=""):
        gc.collect()
        free = gc.mem_free()
        print(f"[MEMORY] GC after {reason}: {free} bytes free.")
        return free


    def mem_free(self):
        free = gc.mem_free()
        print(f"[MEMORY] Free memory: {free} bytes.")
        return free