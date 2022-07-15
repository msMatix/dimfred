from rsmq import RedisSMQ


class RQueue:
    def __init__(self, name, url="127.0.0.1:6379", options=None, **kwargs):
        host, *port = url.split(":")
        port = 6379 if not port else port[0]
        port = 6379 if not port else port[0]
        self.queue = RedisSMQ(host=host, port=port, options=options, **kwargs)

        try:
            self.queue.createQueue(qname=name).execute()
        except Exception:
            pass

    def push(self, msg):
        self.queue.sendMessage(message=msg).execute()

    def pop(self, **kwargs):
        try:
            return self.queue.popMessage(**kwargs)
        except Exception:
            return None
