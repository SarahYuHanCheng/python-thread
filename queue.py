class MaxSizeList(object):

    def __init__(self, max_length):
        self.max_length = max_length
        self.ls = []

    def push(self, st):
        if len(self.ls) == self.max_length:
            return 1
        self.ls.append(st)
        return 0

    def pop_first(self):
        return self.ls.pop(0)
    def get_list(self):
        return self.ls

room_q=MaxSizeList(4)

r=room_q.get_list()
print(r[-1])
(r[-1][2]).pop()
rr=room_q.get_list()
print(rr[-1])

# the assigned variable(r,rr) would edit the original instance(room_q) of class
