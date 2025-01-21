import pandas as pd

import mpvis

bug_log_path = "data/Minimal.csv"

bug_event_log = pd.read_csv(bug_log_path, sep=",")

print(bug_event_log)


bug_format = {
    "case:concept:name": "ID",
    "concept:name": "Activity_MACRO",
    "time:timestamp": "Timestamp end",
    "start_timestamp": "Timestamp start",
    # "org:resource": "",
    # "cost:total": "cost",
}
minimal_event_log = mpvis.log_formatter(bug_event_log, bug_format)

manual_grouped_log = mpvis.preprocessing.manual_log_grouping(
    minimal_event_log,
    activities_to_group=["Checkout of UROLOGY department", "Waiting area for checkout URO"],
    group_name="Checkout of UROLOGY Department",
)
print(minimal_event_log)

print(manual_grouped_log)
