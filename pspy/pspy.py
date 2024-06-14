import os, time, pwd, re
PROC = "/proc"

#absolute max this wil run for
MAX_SECONDS_SAFEGUARD = 180



class PSpy:
    monitor_directories = ["/tmp", "/var","/bin", "/sbin","usr"]
    
    def __init__(self) -> None:
        self.pids = self.getPIDS()
        print(self.pids)


    def getNewPIDS(self):
        """
        Get PIDS that didn't exist since the last time I wrote self.pids
        """
        current_pids = self.getPIDS()        
        new_pids = list(set(current_pids) - set(self.pids))
        self.pids = current_pids        
        return new_pids

    async def SpinAsync(self,seconds=5):
        return self.Spin(seconds)
    
    
    def Spin(self,seconds=5,outlist=None):
        """
        Run for seconds seconds, and return an array of tuples of new processes
        """
        if seconds < 0 or seconds > MAX_SECONDS_SAFEGUARD:
            return [("0","nope","nope")]
        
        start_time = time.perf_counter()        
        all_process_infos = []
        while time.perf_counter() < start_time + seconds:
            time.sleep(0.001)
            pids = self.getNewPIDS()            
            for p in pids:                
                infos = self.getPIDInfo(p)
                print(infos)
                all_process_infos.append(infos)

        #if using threaded output value
        if outlist:
            outlist = all_process_infos
        return all_process_infos

    def getPIDS(self):
        """
        Get system PIDs, and refresh the internal pid tracker
        """
        pids = [ f.name for f in os.scandir(PROC) if f.is_dir() and f.name.isdigit() ]        
        return pids

    def getPIDInfo(self,pid):
        try:
            path = f"/proc/{pid}/cmdline"
            
            with open(path, "r") as f:
                contents = f.read().strip().replace("\0"," ")            
                
            with open(f"/proc/{pid}/status","r") as f:
                status_text = f.read()
                group = re.search("^Uid:[\\s]*(\\d+)[\\s]*",status_text,flags=re.MULTILINE).group(1)
                if group:
                    owner_struct = pwd.getpwuid(int(group))                
                    owner = f"{owner_struct.pw_name}({owner_struct.pw_uid})"
                else:
                    owner = f"Unknown"
            return (pid,owner,contents)
        except Exception as e:
            return ("??","ERR",f"No idea on pid {pid} {e}")