#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from parlai.crowdsourcing.utils.worlds import CrowdOnboardWorld, CrowdTaskWorld  # type: ignore
from parlai.core.worlds import validate  # type: ignore
from joblib import Parallel, delayed  # type: ignore


class MultiAgentDialogOnboardWorld(CrowdOnboardWorld):
    def __init__(self, opt, agent):
        super().__init__(opt, agent)
        self.opt = opt

    def parley(self):
        self.agent.agent_id = "Onboarding Agent"
        self.agent.observe({"id": "System", "text": "Welcome onboard!"})
        x = self.agent.act(timeout=self.opt["turn_timeout"])
        self.agent.observe(
            {
                "id": "System",
                "text": "Thank you for your input! Please wait while "
                "we match you with another worker...",
                "episode_done": True,
            }
        )
        self.episodeDone = True


class MultiAgentDialogWorld(CrowdTaskWorld):
    """
    Basic world where each agent gets a turn in a round-robin fashion, receiving as
    input the actions of all other agents since that agent last acted.
    """

    def __init__(self, opt, agents=None, shared=None):
        # Add passed in agents directly.
        self.agents = agents
        self.acts = [None] * len(agents)
        self.episodeDone = False
        self.max_turns = opt.get("num_turns", 3)
        self.current_turns = 0
        self.send_task_data = opt.get("send_task_data", False)
        self.opt = opt
        self.agents[0].agent_id = "Cliente"
        self.agents[1].agent_id = "Atendente"
        self.dialogue_data = shared.shared
        self.utterances = []

    def push_to_db(self, acts):
        # acts.pop("id", None)
        # acts.pop("task_data", None)
        # acts.pop("timestamp", None)
        self.utterances.append(acts)

    def parley(self):
        """
        For each agent, get an observation of the last action each of the other agents
        took.
        Then take an action yourself.
        """
        if self.current_turns == 0:
            self.agents[0].observe({
                 "id": "História",
                 "text": "\n".join(self.dialogue_data["client"])
            })
            self.agents[1].observe({
                 "id": "História",
                 "text": "\n".join(self.dialogue_data["system"])
            })
        acts = self.acts
        for index, agent in enumerate(self.agents):
            self.current_turns += 1
            acts[index] = agent.act(timeout=self.opt["turn_timeout"])
            if acts[index]["text"] == "!end":
                acts[index].force_set("episode_done", True)
            self.push_to_db(acts[index].copy())
            if self.send_task_data:
                acts[index].force_set(
                    "task_data",
                    {
                        "last_acting_agent": agent.agent_id,
                        "current_dialogue_turn": self.current_turns,
                        "utterance_count": self.current_turns + index,
                    },
                )
            if acts[index]["episode_done"]:
                self.episodeDone = True
            for other_agent in self.agents:
                if other_agent != agent:
                    other_agent.observe(validate(acts[index]))
        if self.current_turns >= self.max_turns:
            self.episodeDone = True

    def prep_save_data(self, agent):
        """Process and return any additional data from this world you may want to store"""
        print("A conversation has finished! Saving data...")
        return self.utterances

    def episode_done(self):
        return self.episodeDone

    def shutdown(self):
        """
        Shutdown all mturk agents in parallel, otherwise if one mturk agent is
        disconnected then it could prevent other mturk agents from completing.
        """
        global shutdown_agent

        def shutdown_agent(agent):
            try:
                agent.shutdown(timeout=None)
            except Exception:
                agent.shutdown()  # not MTurkAgent

        Parallel(n_jobs=len(self.agents), backend="threading")(
            delayed(shutdown_agent)(agent) for agent in self.agents
        )


def make_onboarding_world(opt, agent):
    return MultiAgentDialogOnboardWorld(opt, agent)


def validate_onboarding(data):
    """Check the contents of the data to ensure they are valid"""
    print(f"Validating onboarding data {data}")
    return True


def make_world(opt, agents, initialization_data):
    return MultiAgentDialogWorld(opt, agents, initialization_data)


def get_world_params():
    return {"agent_count": 2}
