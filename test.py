import threading,time
import IOevent
from sensors import sensors

class uc(sensors.sensor):
    timetable=[]
    timer_lock=threading.RLock()
    def __init__(self):
        self.is_running = False
        self.thread = None

    def start(self):
        if not self.is_running:
            #print("open_new timer thread")
            self.is_running = True
            self.thread = threading.Thread(target=self.checking,args=[])
            self.thread.start()

    def set(self, mevent:IOevent.gameevent, message:dict):
        second=message["value"] #計時時間 
        content=message["key"] #計時時間
        # for t in self.timetable:            
        #     if t['userid']==mevent.user_id and t['content']==content: 
        #         self.timetable.remove(t)
        # self.timetable=[t for t in self.timetable if t['userid']==mevent.user_id and t['content']==content]

        with self.timer_lock:
            self.timetable = list(filter(lambda t: t['userdata'][id]!=mevent.touserdict()['id'] or t['content']!=content, self.timetable))

            if second>=0:
                t={}
                t['userdata']=mevent.touserdict()
                t['content']=content
                # t["api"]=mevent.API_container.API
                t['time_end']=time.time()+second
                self.timetable.append(t)
                #print("timeout_list:"+str(self.timetable))
                # temp=threading.Thread(target=self.checking,args=[])
                # temp.start()
                self.start()

    def checking(self):
        # self.timer_lock.acquire(False)
        over_list=[]
        while len(self.timetable)>0:
            for t in self.timetable:
                if time.time()>t['time_end']:
                    userdict=t['userdata']
                    task=t['content']
                    # self.timetable.remove(t)
                    over_list.append(t)
                    #print("remove t",str(t))
                    #TODO 待測試
                    sensors.update(userdict,task)   
            if len(over_list)!=0:
                #所有寫入修改都需要枷鎖，以保證安全
                with self.timer_lock:
                    self.timetable = list(filter(lambda t:t not in over_list, self.timetable))
                over_list=[]

        self.is_running = False
        # self.timer_lock.release()
                 