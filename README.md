# DProcessor
a simple python parallel execution framework

use it like this:
```python
import dprocessor
import time
import sys

class TestDprocessor:
    def __init__(self):
        self.id = 0
        
    def test_per_process(self, num):
        self.id += num
        print self.id
        sys.stdout.flush()
        time.sleep(self.id)
        self.id += 20
        print self.id
        sys.stdout.flush()

def per_process(process, num):
    process.test_per_process(num)

def gen_funcs():
    load_funcs = []
    test_process = TestDprocessor()
    for i in range(10):
        func_name = "func"+str(i)
        func_meta = per_process
        f_args = [test_process, i]
        p_func = [func_name, func_meta]
        p_func.extend(f_args)
        load_funcs.append(p_func)
    return load_funcs

if __name__ == '__main__':
    multi_process = dprocessor.DProcessor(func_items=[], pnum=3)
    funcs = gen_funcs()
    multi_process.set_funcs(funcs)
    multi_process.run()
```
