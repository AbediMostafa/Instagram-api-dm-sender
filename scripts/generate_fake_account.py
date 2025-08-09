"""
Run this in the database to insert the records in there
COPY accounts (
  proxy, color, screen_resolution, profile, category, secret_key, username, password, name, bio, email, profile_pic_url, instagram_state, app_state, avatar_changed, username_changed, initial_posts_deleted, has_enough_posts, is_used, is_active, is_public, web_session, mobile_session, log, updated_at, next_login
) FROM '/home/accounts.csv' CSV HEADER;

"""

import csv
from faker import Faker
from random import randint, choice
from pathlib import Path

# CSV output path
OUTPUT_FILE = Path("accounts.csv")

# Number of fake rows
NUM_RECORDS = 100000

# Create faker instance
fake = Faker()

# CSV columns matching your Account model's database fields
columns = [
    "proxy",
    "color",
    "screen_resolution",
    "profile",
    "category",
    "secret_key",
    "username",
    "password",
    "name",
    "bio",
    "email",
    "profile_pic_url",
    "instagram_state",
    "app_state",
    "avatar_changed",
    "username_changed",
    "initial_posts_deleted",
    "has_enough_posts",
    "is_used",
    "is_active",
    "is_public",
    "web_session",
    "mobile_session",
    "log",
    "updated_at",
    "next_login",
]


def generate_row():
    return [
        randint(1, 100),  # proxy
        randint(1, 10),  # color
        randint(1, 5),  # screen_resolution
        randint(1, 50),  # profile
        randint(1, 20),  # category
        fake.sha256(),  # secret_key
        fake.user_name(),  # username
        fake.password(),  # password
        fake.name(),  # name
        fake.text(max_nb_chars=100),  # bio
        fake.email(),  # email
        fake.image_url(),  # profile_pic_url
        choice(["active", "banned"]),  # instagram_state
        choice(["idle", "running"]),  # app_state
        randint(0, 1),  # avatar_changed
        randint(0, 1),  # username_changed
        randint(0, 1),  # initial_posts_deleted
        randint(0, 1),  # has_enough_posts
        randint(0, 1),  # is_used
        1,  # is_active
        randint(0, 1),  # is_public
        fake.uuid4(),  # web_session
        fake.uuid4(),  # mobile_session
        fake.text(max_nb_chars=50),  # log
        fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S"),  # updated_at
        fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S"),  # next_login
    ]


def main():
    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        for _ in range(NUM_RECORDS):
            writer.writerow(generate_row())

    print(f"✅ CSV file created: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()
