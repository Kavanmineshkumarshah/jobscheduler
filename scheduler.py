import random
class Scheduler:
    def __init__(self):
        self.jobs = []
        self.current_job_index = 0
        self.current_job = None
        self.is_running = False
        self.is_paused = False
        self.is_stopped = False
        self.is_completed = False
        self.is_failed = False
        self.is_cancelled = False
        self.is_resumed = False
        self.is_scheduled = False
        self.is_executing = False
        self.cut_vegetables = False
        self.boil_rice = False
        self.make_curry = False
        self.serve_food = False
    def add_job(self, job):
        self.jobs.append(job)
    def cut_vegetables_job(self):
        self.cut_vegetables = True
        if self.cut_vegetables==5:
            print("Vegetables are already cut.")
        else:
           print("Cutting vegetables...")
    def boil_rice_job(self):
        self.boil_rice = True
        if self.boil_rice==8:
            print("Rice is already boiled.")
        else:
            print("Boiling rice...")
    def make_curry_job(self):
        self.make_curry = True
        if self.make_curry==6:
            print("Curry is already made.")
        else:
            print("Making curry...")
    def serve_food_job(self):
        self.serve_food = True
        if self.serve_food==2:
            print("Food is already served.")
        else:
            print("Serving food...")
    def schedule_jobs(self):
        random.shuffle(self.jobs)
        for job in self.jobs:
            job.execute()
    def get_jobs(self):
        return self.jobs
    def clear_jobs(self):
        self.jobs = []
    def get_current_job(self):
        if self.current_job_index < len(self.jobs):
            return self.jobs[self.current_job_index]
        return None
    def next_job(self):
        if self.current_job_index < len(self.jobs) - 1:
            self.current_job_index += 1
            return self.jobs[self.current_job_index]
        return None
    def previous_job(self):
        if self.current_job_index > 0:
            self.current_job_index -= 1
            return self.jobs[self.current_job_index]
        return None
    def get_job_status(self):
        if self.current_job is None:
            return "No job is currently running."
        if self.is_running:
            return "Job is running."
        if self.is_paused:
            return "Job is paused."
        if self.is_stopped:
            return "Job is stopped."
        if self.is_completed:
            return "Job is completed."
        if self.is_failed:
            return "Job has failed."
        if self.is_cancelled:
            return "Job is cancelled."
        if self.is_resumed:
            return "Job has resumed."
        if self.is_scheduled:
            return "Job is scheduled."
        if self.is_executing:
            return "Job is executing."
        return "Unknown job status."
    def get_job_progress(self):
        if self.current_job is None:
            return 0
        return self.current_job.get_progress()
    def get_job_result(self):
        if self.current_job is None:
            return None
        return self.current_job.get_result()
    def get_job_error(self):
        if self.current_job is None:
            return None
        return self.current_job.get_error()
    def get_job_logs(self):
        if self.current_job is None:
            return []
        return self.current_job.get_logs()
    def get_job_metrics(self):
        if self.current_job is None:
            return {}
        return self.current_job.get_metrics()
    def get_job_configuration(self):
        if self.current_job is None:
            return {}
        return self.current_job.get_configuration()
    def get_job_dependencies(self):
        if self.current_job is None:
            return []
        return self.current_job.get_dependencies()
    def get_job_priority(self):
        if self.current_job is None:
            return None
        return self.current_job.get_priority()
    def get_job_timeout(self):
        if self.current_job is None:
            return None
        return self.current_job.get_timeout()
    def get_job_retries(self):
        if self.current_job is None:
            return None
        return self.current_job.get_retries()
    def get_job_schedule(self):
        if self.current_job is None:
            return None
        return self.current_job.get_schedule()
    def get_job_resources(self):
        if self.current_job is None:
            return {}
        return self.current_job.get_resources()
    def get_job_environment(self):
        if self.current_job is None:
            return {}
        return self.current_job.get_environment()
    def get_job_notifications(self):
        if self.current_job is None:
            return {}
        return self.current_job.get_notifications()
    def get_job_metadata(self):
        if self.current_job is None:
            return {}
        return self.current_job.get_metadata()
    def get_job_statistics(self):
        if self.current_job is None:
            return {}
        return self.current_job.get_statistics()
    def get_job_audit_trail(self):
        if self.current_job is None:
            return []
        return self.current_job.get_audit_trail()
    def get_job_history(self):
        if self.current_job is None:
            return []
        return self.current_job.get_history()
    def get_job_logs(self):
        if self.current_job is None:
            return []
        return self.current_job.get_logs()
    def get_job_metrics(self):
        if self.current_job is None:
            return {}
        return self.current_job.get_metrics()
    def get_job_configuration(self):
        if self.current_job is None:
            return {}
        return self.current_job.get_configuration()
if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.cut_vegetables_job()
    scheduler.boil_rice_job()
    scheduler.make_curry_job()
    scheduler.serve_food_job()