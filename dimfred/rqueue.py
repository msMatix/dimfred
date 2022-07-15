from rsmq import RedisSMQ


class RQueue:
    def __init__(self, name, host="127.0.0.1", port=6379, options=None, **kwargs):
        self.queue = RedisSMQ(host=host, port=port, options=options, **kwargs)
        self.queue.createQueue(qname=name).execute()

    def push(self, msg):
        self.queue.sendMessage(message=msg).execute()

    def pop(self, **kwargs):
        try:
            self.queue.popMessage(**kwargs)
        except:
            return None
