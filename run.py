#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os
import time
import json
from threading import Timer

from mephisto.operations.operator import Operator
from mephisto.tools.scripts import task_script, load_db_and_process_config
from mephisto.operations.hydra_config import build_default_task_config
from mephisto.abstractions.blueprints.parlai_chat.parlai_chat_blueprint import (
    BLUEPRINT_TYPE_PARLAI_CHAT,
    SharedParlAITaskState,
)

from omegaconf import DictConfig
from dataclasses import dataclass, field

def run_lt(port):
    if os.path.isfile('/usr/local/bin/lt'):
        print("localtunnel is alreadty installed.")
    else:
        os.system('npm install -g localtunnel')
    output = os.system(f'lt -p {port}')
    return output

def start_lt(port):
    lt_adress = run_lt(port)
    print(lt_adress)

@dataclass
class ParlAITaskConfig(build_default_task_config("base")):  # type: ignore
    num_turns: int = field(
        default=30,
        metadata={"help": "Number of turns before a conversation is complete"},
    )
    turn_timeout: int = field(
        default=300,
        metadata={
            "help": "Maximum response time before kicking "
            "a worker out, default 300 seconds"
        },
    )


@task_script(config=ParlAITaskConfig)
def main(operator: "Operator", cfg: DictConfig) -> None:
    config = None
    fold = __file__.replace(os.path.basename(__file__), "")
    with open(fold+"config.json", encoding='utf-8') as config_file:
        config = json.load(config_file)

    world_opt = {"num_turns": cfg.num_turns, "turn_timeout": cfg.turn_timeout}
    custom_bundle_path = cfg.mephisto.blueprint.get("custom_source_bundle", None)
    if custom_bundle_path is not None:
        assert os.path.exists(custom_bundle_path), (
            "Must build the custom bundle with `npm install; npm run dev` from within "
            f"the {cfg.task_dir}/webapp directory in order to demo a custom bundle "
        )
        world_opt["send_task_data"] = True

    shared_state = SharedParlAITaskState(
        world_opt=world_opt, onboarding_world_opt=world_opt
    )

    cfg['mephisto']['architect']['port'] = config["port"]
    operator.launch_task_run(cfg.mephisto, shared_state)

    if (config["localtunnel"]):
        thread = Timer(1, start_lt, args=(cfg['mephisto']['architect']['port'],))
        thread.setDaemon(True)
        thread.start()

    operator.wait_for_runs_then_shutdown(skip_input=True, log_rate=30)

if __name__ == "__main__":
    main()