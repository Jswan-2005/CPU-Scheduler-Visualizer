'''
This project simulates multiple CPU Schedulers
1. FIFOScheduler : FIFO (First in First Out) Scheduler
2. STCFScheduler : STCF (Shortest Time to Complete First) Scheduler
3. RRScheduler : RR (Round Robin) Scheduler

Each scheduler dynamically prints the current process (if any) running at every second.
At the end (when every process has completed executing) key metrics are printed for each process
These metrics are : Arrival Time, Completion Time, Turnaround Time (Completion - Arrival), Response Time (When the process was first exectued by the CPU)
'''

import sys
import copy
import time as tm
import os



class Process:
    def __init__(self, arrival, time_to_run, pid):
        self.t_arrival = arrival
        self.t_time_to_run = time_to_run
        self.pid = pid
        self.t_turnaround = None
        self.t_completion = None
        self.t_response = None
        self.t_running = 0

def PrintProccesses(pl, scheduler):
    print(f"Result From {scheduler}")
    for p in pl:
        print(f"Process {p.pid} -> Arrival Time {p.t_arrival} -> Completion Time {p.t_completion}, Turnaround Time {p.t_turnaround}, Response Time {p.t_response}")

def FIFOScheduler(pl):
    scheduler_list = sorted(pl, key=lambda p: p.t_arrival)
    time = 0
    while scheduler_list:
        current_process = scheduler_list[0]
        while current_process.t_arrival > time:
            DynamicPrint(None, time)
            time += 1

        if current_process.t_response is None:
            current_process.t_response = time - current_process.t_arrival

        while current_process.t_time_to_run > 0:
            time += 1
            DynamicPrint(current_process, time-1)
            current_process.t_time_to_run -= 1

        current_process.t_completion = time
        current_process.t_turnaround = current_process.t_completion - current_process.t_arrival
        scheduler_list.pop(0)
    print()
    PrintProccesses(pl, 'FIFOScheduler')

def STCFScheduler(pl):
    pl_copy = pl.copy()
    time = 0
    scheduler_list = sorted(pl, key=lambda p: p.t_arrival)
    scheduler_runner = []
    time = 0
    while scheduler_list:
        time += 1
        for p in pl:
            if p.t_arrival <= time:
                scheduler_runner.append(p)
                scheduler_runner = sorted(scheduler_runner, key=lambda p: p.t_time_to_run)
                pl.remove(p)

        if scheduler_runner:
            current_process = scheduler_runner[0]
            DynamicPrint(current_process, time)
            current_process.t_time_to_run -= 1

            if current_process.t_response is None:
                current_process.t_response = time - current_process.t_arrival

            if current_process.t_time_to_run == 0:
                current_process.t_completion = time
                current_process.t_turnaround = current_process.t_completion - current_process.t_arrival
                scheduler_list.remove(scheduler_runner[0])
                scheduler_runner.pop(0)
                continue
        else:
            DynamicPrint(None, time)
    print()
    PrintProccesses(pl_copy, 'STCFScheduler')

def DynamicPrint(current_process,time):
    if current_process:
        print(f"Current Process {current_process.pid} running at time {time}")
    else:
        print(f"No current processes at time {time}")
    tm.sleep(1)
    os.system('cls')


def RRScheduler(pl,timesplice):
    pl_copy = pl.copy()
    time = 0
    scheduler_list = sorted(pl, key=lambda p: p.t_arrival)
    scheduler_runner = []
    while scheduler_list:
        time += 1

        for p in pl:
            if p.t_arrival <= time:
                scheduler_runner.append(p)
                pl.remove(p)

        if scheduler_runner:
            current_process = scheduler_runner[0]
            if current_process.t_response is None:
                current_process.t_response = time - current_process.t_arrival

            DynamicPrint(current_process, time)


            current_process.t_time_to_run -= 1
            current_process.t_running += 1

            if current_process.t_time_to_run == 0:
                scheduler_list.remove(scheduler_runner[0])
                scheduler_runner.pop(0)
                current_process.t_completion = time
                current_process.t_turnaround = current_process.t_completion - current_process.t_arrival


            if current_process.t_running % timesplice == 0:
                if scheduler_runner:
                    temp = scheduler_runner[0]
                    scheduler_runner.remove(scheduler_runner[0])
                    scheduler_runner.append(temp)
        else:
            DynamicPrint(None, time)
    print()
    PrintProccesses(pl_copy, 'RRScheduler')

def main():
    '''  Process(arrival, time_to_run, pid)
         arrival : The time at which the processer arrives to the scheduler
         time_to_run : The time amount of cycles (seconds) in takes for the process to be finished
         pid : Identifier for the process
    '''

    #Example run-through with RR Scheduler with a timesplice of 3
    p1 = Process(5, 10, 1)
    p2 = Process(7, 5, 2)
    p3 = Process(15, 3,3)

    process_list = [p1, p2, p3]
    RRScheduler(process_list,3)

if __name__ == '__main__':
    main()