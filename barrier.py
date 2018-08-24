# coding=UTF-8  
import threading, time, random   
  
lock = threading.Lock()  
rlock = threading.Lock()  
data_size=10  
tmp_sum = []  
  
print "\t[Info] Prepare data..."  
for i in range(data_size):  
    tmp_sum.append(i+1)  
      
class Status:          
    def  __init__( self , size, lock):  
        self._init(size)  
        self.lock = lock  # protect data from race condition? 
          
    def _init(self, size):  
        self.status = []  
        for i in range(size+1):              
            self.status.append(1) # status=[1,1...1] 11 elements  
              
    def atom_read(self, pid):  
        self.lock.acquire()  
        try:  
            return self.status[pid]  
        finally:  
            self.lock.release() 
# The finally clause is also executed when any other clause of the try statement is left via a break, continue or return statement.  
              
    def atom_done(self, pid):  
        self.lock.acquire()  
        try:
            print('status[%d]=0'%pid)  
            self.status[pid]=0  
        finally:  
            self.lock.release()  
              
    def isDone(self):  
        return self.status[0]==0  
          
print "\t[Info] Preparing status object..."              
status = Status(data_size, lock)  
  
class Reducer(threading.Thread):  
    def  __init__( self , lock, pid, tsize, status, tmp_sum):  
        super(Reducer,  self ).__init__(name = pid)   #注意：一定要顯式的調用父類的初始化函數.  
        self.lock = lock            
        self.pid = pid  
        self.tsize= tsize  
        self.status = status  
        self.tmp_sum = tmp_sum  
          
    def  run(self):  
        for s in range(0,self.tsize):  
            s=2**s  # interation times
            if s>self.tsize: break  
            if (self.pid % (2*s)==0) and (self.pid+s<self.tsize):  
                while(self.status.atom_read(self.pid+s)!=0):  # not yet done
                    print "\t[Info] PID={0} wait for PID={1}...".format(self.pid, self.pid+s)  
                    # time.sleep(1)  
                    pass  
                print "sum(tmp_sum[{0}]={1}, tmp_sum[{2}]={3})...".format(self.pid, self.tmp_sum[self.pid], self.pid+s, self.tmp_sum[self.pid+s])  
                self.lock.acquire()  # acquire here? why not last line? because need to read tmp_sum[]
                self.tmp_sum[self.pid]=self.tmp_sum[self.pid+s]+self.tmp_sum[self.pid]  
                # self.lock.acquire()  # acquire here? why not last line? because need to read tmp_sum[]
                print "\t[Info] tmp_sum[{0}]={1}...(s={2})".format(self.pid, self.tmp_sum[self.pid], s)  
                self.lock.release()  
            else:                  
                break  
        self.lock.acquire()  
        # print "\t[Info] PID={0} is done with value={1}...".format(self.pid, self.tmp_sum[self.pid])  
        self.lock.release()  
        self.status.atom_done(self.pid)  # odd index done first(due to the if condition)
              
print "\t[Info] Start paralleling actions..."  
for i in range(data_size):
    # print("Reducer.start")  
    Reducer(rlock, i, data_size, status, tmp_sum).start()  
                   
while(not status.isDone()):  
    time.sleep(2)  
      
print "\t[Info] Sum={0}".format(tmp_sum[0])    