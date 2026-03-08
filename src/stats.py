class Stats:
    def __init__(self):
        self.total_runs = 0

    def record_run(self):
        self.total_runs += 1

    def reset(self):
        self.total_runs = 0