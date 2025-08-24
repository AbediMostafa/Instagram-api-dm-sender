from datetime import datetime
import time
from typing import Callable
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError


class Scheduler:
    _sched: BackgroundScheduler

    def __init__(self, concurrency=5) -> None:
        from django_apscheduler.jobstores import DjangoJobStore

        executors = {
            "default": ThreadPoolExecutor(
                concurrency, dict(thread_name_prefix="Scheduler")
            )
        }
        jobstores = {"default": DjangoJobStore()}  # FIXME
        self._sched = BackgroundScheduler(executors=executors)

    def fire(self):
        self._sched.start()
        while True:
            time.sleep(1000)

    def set_interval(
        self,
        func,
        seconds=0,
        minutes=0,
        hours=0,
        days=0,
        weeks=0,
        start_date=None,
        end_date=None,
        id=None,
        name=None,
        max_instances=1,
        coalesce=False,
        replace_existing=False,
        jobstore="default",
        executor="default",
        misfire_grace_time=None,
        jitter=None,
        timezone=None,
        args=None,
        kwargs=None,
    ):
        """
        Add a job with an interval trigger to the scheduler.
        """
        self._sched.add_job(
            func=func,
            trigger="interval",
            seconds=seconds,
            minutes=minutes,
            hours=hours,
            days=days,
            weeks=weeks,
            start_date=start_date,
            end_date=end_date,
            id=id,
            name=name,
            max_instances=max_instances,
            coalesce=coalesce,
            replace_existing=replace_existing,
            jobstore=jobstore,
            executor=executor,
            misfire_grace_time=misfire_grace_time,
            jitter=jitter,
            timezone=timezone,
            args=args or [],
            kwargs=kwargs or {},
        )

    def set_cron(
        self,
        func: Callable,
        args: tuple = (),
        kwargs: dict | None = None,
        *,
        id: str | None = None,
        name: str | None = None,
        replace_existing: bool = False,
        coalesce: bool = True,
        max_instances: int = 1,
        misfire_grace_time: int | None = None,
        next_run_time: datetime | None = None,
        timezone: str | None = None,
        year: str | int | None = None,
        month: str | int | None = None,
        day: str | int | None = None,
        week: str | int | None = None,
        day_of_week: str | int | None = None,
        hour: str | int | None = None,
        minute: str | int | None = None,
        second: str | int | None = None,
    ):
        """Schedule a cron job with explicit arguments instead of *args/**kwargs."""
        return self._sched.add_job(
            func=func,
            trigger="cron",
            args=args,
            kwargs=kwargs or {},
            id=id,
            name=name,
            replace_existing=replace_existing,
            coalesce=coalesce,
            max_instances=max_instances,
            misfire_grace_time=misfire_grace_time,
            next_run_time=next_run_time,
            timezone=timezone,
            year=year,
            month=month,
            day=day,
            week=week,
            day_of_week=day_of_week,
            hour=hour,
            minute=minute,
            second=second,
        )

    def remove_job(self, job_id):
        try:
            self._sched.remove_job(job_id)
        except JobLookupError:
            print(f"No job found with id {job_id}")
