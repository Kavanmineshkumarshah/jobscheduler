import time
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Job:
    def __init__(self, name, action_func):
        self.name = name
        self.action_func = action_func
        self.dependencies = []
        self.is_done = False

    def needs(self, *jobs):
        for job in jobs:
            self.dependencies.append(job)

    def execute(self):
        if not self.is_done:
            self.action_func()
            self.is_done = True

    def __repr__(self):
        return self.name


class KitchenScheduler:
    def __init__(self):
        self.jobs = []

    def add_job(self, job):
        self.jobs.append(job)

    def cut_vegetables_action(self):
        logging.info("STARTING: Cutting vegetables...")
        time.sleep(5)  # Using 5 seconds instead of 300 for quick testing
        logging.info("DONE: Vegetables are cut.")

    def boil_rice_action(self):
        logging.info("STARTING: Boiling rice...")
        time.sleep(8)  # Using 8 seconds instead of 180
        logging.info("DONE: Rice is boiled.")

    def make_curry_action(self):
        logging.info("STARTING: Making curry...")
        time.sleep(6)  # Using 6 seconds instead of 180
        logging.info("DONE: Curry is made.")

    def serve_food_action(self):
        logging.info("STARTING: Serving food...")
        time.sleep(2)  # Using 2 seconds instead of 120
        logging.info("DONE: Food is served!")

    def dfs_recursive(self, job, visited, permanent_visited):
        # Cycle detection
        if job in visited:
            raise ValueError(f"Circular dependency detected at job: {job}")
        
        if job not in permanent_visited:
            visited.add(job)
            for dependency in job.dependencies:
                self.dfs_recursive(dependency, visited, permanent_visited)
            visited.remove(job)
            permanent_visited.append(job)

    def run_scheduler(self):
        permanent_visited = []
        visited = set()
        
        for job in self.jobs:
            if job not in permanent_visited:
                self.dfs_recursive(job, visited, permanent_visited)
        
        
        cut_veg = next(j for j in permanent_visited if j.name == "cut_vegetables")
        rice = next(j for j in permanent_visited if j.name == "boil_rice")
        curry = next(j for j in permanent_visited if j.name == "make_curry")
        serve = next(j for j in permanent_visited if j.name == "serve_food")

        cut_veg.execute()

        logging.info("Launching parallel tasks...")
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(rice.execute)
            executor.submit(curry.execute)

        serve.execute()


if __name__ == "__main__":
    scheduler = KitchenScheduler()

    cut_veg_job = Job("cut_vegetables", scheduler.cut_vegetables_action)
    boil_rice_job = Job("boil_rice", scheduler.boil_rice_action)
    make_curry_job = Job("make_curry", scheduler.make_curry_action)
    serve_food_job = Job("serve_food", scheduler.serve_food_action)

    boil_rice_job.needs(cut_veg_job)   
    make_curry_job.needs(cut_veg_job)  
    serve_food_job.needs(boil_rice_job, make_curry_job) 

    scheduler.add_job(serve_food_job)
    scheduler.add_job(make_curry_job)
    scheduler.add_job(boil_rice_job)
    scheduler.add_job(cut_veg_job)

    scheduler.run_scheduler()
