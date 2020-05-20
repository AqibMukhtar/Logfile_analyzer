import re
import csv
import operator

log_lines = [
    "May 27 11:45:40 ubuntu.local ticky: INFO: Created ticket [#1234] (username)",
    "Jun 1 11:06:48 ubuntu.local ticky: ERROR: Connection to DB failed (username)",
]
error_stats = {}
user_stats = {}

for line in log_lines:
    result = re.search(r"ticky: ERROR: ([ \w]+)", line)
    if result:
        error = result[1].strip()
        if error in error_stats.keys():
            error_stats[error] += 1
        else:
            error_stats[error] = 1
sorted_errors = sorted(error_stats.items(), key=operator.itemgetter(1), reverse=True)

for line in log_lines:
    result = re.search(r"ticky: (ERROR|INFO):.*\((\w+)\)", line)
    if result:
        action = result[1]
        username = result[2]
        if username in user_stats.keys():
            if action in user_stats[username].keys():
                user_stats[username][action] += 1
            else:
                user_stats[username][action] = 1
        else:
            user_stats[username] = {action: 1}
sorted_users = sorted(user_stats.items())

with open("error_message.csv", "w", newline="") as error_file:
    writer = csv.DictWriter(error_file, fieldnames=["Error", "Count"])
    writer.writeheader()
    for record in sorted_errors:
        writer.writerow({"Error": record[0], "Count": record[1]})

with open("user_statistics.csv", "w", newline="") as user_file:
    writer = csv.DictWriter(user_file, fieldnames=["Username", "INFO", "ERROR"])
    writer.writeheader()
    for record in sorted_users:
        writer.writerow(
            {
                "Username": record[0],
                "INFO": record[1]["INFO"],
                "ERROR": record[1]["ERROR"],
            }
        )
