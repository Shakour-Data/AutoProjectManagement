import schedule
import time
import threading

class Scheduler:
    def __init__(self):
        self.jobs = []

    def start(self):
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(1)

        thread = threading.Thread(target=run_scheduler, daemon=True)
        thread.start()

    def schedule_hourly(self, job_func):
        job = schedule.every(1).hours.do(job_func)
        self.jobs.append(job)

    def schedule_daily(self, job_func):
        job = schedule.every().day.at("00:00").do(job_func)
        self.jobs.append(job)

# Example usage:
# from dashboards_reports import update_dashboards
# from reporting import update_reports
#
# scheduler = Scheduler()
# scheduler.schedule_hourly(update_dashboards)
# scheduler.schedule_daily(update_reports)
# scheduler.start()
#
# while True:
#     time.sleep(10)
