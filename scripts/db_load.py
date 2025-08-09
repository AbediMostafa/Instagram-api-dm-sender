from concurrent.futures import ThreadPoolExecutor, as_completed

from datetime import datetime, timedelta
import time

from numpy import average

from models.Account import Account

per_thread_time = []
total_time = []


def query_accounts_with_date_filter():
    # Define a datetime threshold — e.g., accounts updated in the last 30 days
    threshold_date = datetime.now() - timedelta(days=10)
    t0 = time.time()
    t0c = time.process_time()

    with Account._meta.database.connection_context():
        # Filter active accounts updated after threshold_date
        filtered_accounts = Account.select().where(
            (Account.is_active == 1) & (Account.updated_at > threshold_date)
        )

        count = filtered_accounts.count()

        # Example: fetch first 5 filtered accounts
        sample_accounts = list(filtered_accounts.limit(5))
    # print(sample_accounts)
    t = time.process_time()
    total_t = time.time() - t0
    per_thread_time.append(total_t)
    cpu_t = t - t0c
    # print(f"CPU TIME: {t} . {total_time}")
    return count, sample_accounts


for i in [4] * 50:
    threads = i
    t0 = time.time()
    with ThreadPoolExecutor(threads) as executor:
        futures = [
            executor.submit(query_accounts_with_date_filter) for i in range(int(150))
        ]
        for future in as_completed(futures):
            result = future.result()  # get the return value of task()
    t1 = time.time()
    av = average(per_thread_time)
    print(f"average latency per thread {round(av, 3)} - Threads: {threads} - Total Latency: {t1-t0}")
