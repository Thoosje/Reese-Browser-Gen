from .generator import Generator
import time

class Queue():
    def __init__(self, exe_path: str, amount_of_workers: int):
        self.workers: list[Generator] = []
        
        for i in range(amount_of_workers):
            self.workers.append(
                Generator(exe_path)
            )


    def get_cookie(self, aihToken: str, reese_script: str):
        amount_of_tries: int = 30
        for count in range(amount_of_tries):
            found_worker = None
            for worker in self.workers:
                if not worker.is_working:
                    found_worker = worker
                    break
            
            if not found_worker:
                time.sleep(1)
                continue
            else:
                data = worker.generate(aihToken, reese_script)
                worker.is_working = False
                return data
                
        raise Exception('Failed to find any available worker after %s tries.' % amount_of_tries)