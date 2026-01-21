'''
This project simulates multiple CPU Schedulers
1. FIFOScheduler : FIFO (First in First Out) Scheduler
2. STCFScheduler : STCF (Shortest Time to Complete First) Scheduler
3. RRScheduler : RR (Round Robin) Scheduler
4. Lottery Scheduler : Tickets based on total time to execute process

Lottery scheduler variant based on remaining execution time. Typcically, a lottery scheduler uses fixed tickets to represent CPU share. More of a hybrid between STCF and Lottery schedulers.

Each scheduler dynamically prints the current process (if any) running at every second.
At the end (when every process has completed executing) key metrics are printed for each process
These metrics are : Arrival Time, Completion Time, Turnaround Time (Completion - Arrival), Response Time (When the process was first executed by the CPU)

'''

import sys
import copy
import time as tm
import os
import random

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

def TaskSwitching(process_origin_pid,process_switch_pid,time):
    print(f'Process {process_origin_pid} -> {process_switch_pid} at time {time} seconds')

def FIFOScheduler(pl):
    scheduler_list = sorted(pl, key=lambda p: p.t_arrival)
    time = 0
    while scheduler_list:
        current_process = scheduler_list[0]
        if time > 0:
            TaskSwitching(temp.pid, current_process.pid, time)
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
        temp = scheduler_list.pop(0)
    print()
    PrintProccesses(pl, 'FIFOScheduler')

def STCFScheduler(pl):
    pl_copy = pl.copy()
    time = 0
    scheduler_list = sorted(pl, key=lambda p: p.t_arrival)
    scheduler_runner = []
    time = 0
    temp = None
    while scheduler_list:
        time += 1
        for p in pl:
            if p.t_arrival <= time:
                scheduler_runner.append(p)
                scheduler_runner = sorted(scheduler_runner, key=lambda p: p.t_time_to_run)
                pl.remove(p)

        if scheduler_runner:
            if temp and temp.pid != scheduler_runner[0].pid:
                TaskSwitching(temp.pid, scheduler_runner[0].pid, time)

            current_process = scheduler_runner[0]
            temp = current_process
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
    tm.sleep(0.5)
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
                    if temp.pid != scheduler_runner[0].pid:
                        TaskSwitching(temp.pid,scheduler_runner[0].pid,time)

        else:
            DynamicPrint(None, time)
    print()
    PrintProccesses(pl_copy, 'RRScheduler')

def LotteryScheduler(pl):
    pl_copy = pl.copy()
    time = 0
    scheduler_list = sorted(pl, key=lambda p: p.t_arrival)
    scheduler_runner = []
    lottery_sum = []
    process_list = []
    random_ticket = None
    process_ran = False
    while scheduler_list:
        time += 1
        current_process = None

        for p in pl:
            if p.t_arrival <= time and p not in scheduler_runner:
                lottery_sum += [p.pid for _ in range(p.t_time_to_run)]
                scheduler_runner.append(p)

        if lottery_sum:
            random_ticket = random.choice(lottery_sum)
            for process in scheduler_runner:
                if random_ticket == process.pid:
                    if process_list and process_list[-1] != random_ticket:
                        TaskSwitching(process_list[-1], random_ticket,time)
                    current_process = process
                    process_list.append(process.pid)
                    if process.t_response is None:
                        process.t_response = time - process.t_arrival

        if current_process:
            current_process.t_time_to_run -= 1
            lottery_sum.remove(current_process.pid)
            if current_process.t_time_to_run == 0:
                current_process.t_completion = time+1
                current_process.t_turnaround = current_process.t_completion - current_process.t_arrival
                scheduler_list.remove(current_process)
                scheduler_runner.remove(current_process)
        DynamicPrint(current_process, time)
    print()
    PrintProccesses(pl_copy, 'LotteryScheduler')


def main():
    '''  Process(arrival, time_to_run, pid)
         arrival : The time at which the processer arrives to the scheduler
         time_to_run : The time amount of cycles (seconds) in takes for the process to be finished
         pid : Identifier for the process
    '''

    #Example run-through with RR Scheduler with a timesplice of 3
    p1 = Process(5, 3, 1)
    p2 = Process(5,10,2)

    process_list = [p1,p2]
    LotteryScheduler(process_list)

if __name__ == '__main__':
    main()

