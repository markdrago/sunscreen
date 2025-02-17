import asyncio


class Loop:
    def __init__(self):
        self.tasks = set()
        self.event_handler = None
        self.loop = asyncio.get_event_loop()
        self.init_event_task()

    def set_event_handler(self, event_handler):
        self.event_handler = event_handler

    def init_event_task(self):
        self.event_queue = asyncio.Queue()
        self.add_future(self.handle_event())

    async def handle_event(self):
        while True:
            event = await self.event_queue.get()
            if self.event_handler:
                self.event_handler(event)

    # external_loop: func that can loop infinitely
    def add_external_loop(self, external_loop):
        task = self.loop.run_in_executor(None, external_loop)
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        task.add_done_callback(lambda _: self.loop.stop())

    def add_future(self, future):
        task = asyncio.ensure_future(future)
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)

    # can be executed from another thread
    def queue_add_event(self, event):
        asyncio.run_coroutine_threadsafe(self.event_queue.put(event), self.loop)

    def run(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            for task in self.tasks:
                task.cancel()
