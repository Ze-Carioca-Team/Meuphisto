#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


from mephisto.abstractions.databases.local_database import LocalMephistoDB
from mephisto.tools.examine_utils import run_examine_or_review, print_results
from mephisto.data_model.worker import Worker

db = None


def format_for_printing_data(data):
    global db
    # Custom tasks can define methods for how to display their data in a relevant way
    output_string = "=" * 80
    worker_name = Worker.get(db, data["worker_id"]).worker_name
    output_string += f"\nWorker name: {worker_name}"
    role = data['data']['agent_name']
    output_string += f"\nRole: {role}"
    output_string += f"\nUnit: {data['unit_id']}"
    output_string += f"\nAssignment: {data['assignment_id']}"
    output_string += f"\nStatus: {data['status']}"
    output_string += f"\nDuration: {data['task_end'] - data['task_start']:.3f}\n"
    output_string += "-" * 80
    story = data["data"]["initial_data"]
    output_string += f"\nStory Id: {story['id']}"
    output_string += f"\nStory:\n{data['data']['messages'][1]['text']}"
    output_string += f"\nMessages:\n"
    if data["data"]["save_data"]:
        for msg in data["data"]["save_data"]:
            if "text" in msg and msg["id"] == role:
                output_string += f" * {msg['text']}\n"
    output_string += "=" * 80
    return output_string


def main():
    global db
    db = LocalMephistoDB()
    print(db)
    run_examine_or_review(db, format_for_printing_data)

if __name__ == "__main__":
    main()
