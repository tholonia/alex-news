# @CrewBase
# class AnewsCrew():
#     """News Crew"""
#     @agent
#     def agent_1(self) -> Agent:
#         return  Agent(config=agents_config["agent_1"])
#     @agent
#     def agent_2(self) -> Agent:
#         return  Agent(config=agents_config["agent_2"])

#     @task
#     def task_1(self) -> Task:
#         return Task(config=self.tasks_config["task1"],agent=self.agent_1(),)
#     @task
#     def task_2(self) -> Task:
#         return Task(config=self.tasks_config["task2"],agent=self.agent_2(),)

#     @crew
#     def crew(self) -> Crew:
#         return Crew(agents=self.agents,tasks=self.tasks
