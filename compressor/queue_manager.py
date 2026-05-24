from concurrent.futures import ThreadPoolExecutor
from compressor.encoder import VideoEncoder

class QueueManager:

    def __init__(self, workers=2):
        self.workers = workers
        self.jobs = []

    def add_job(self, config):
        self.jobs.append(config)

    def process(self):

        with ThreadPoolExecutor(
            max_workers=self.workers
        ) as executor:

            futures = []

            for job in self.jobs:

                encoder = VideoEncoder(**job)

                futures.append(
                    executor.submit(
                        encoder.encode
                    )
                )

            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print("ERROR:", e)