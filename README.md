# CPU-Scheduler-Visualizer
A CPU scheduler visualizer built in Python, imitates First in First Out, Shortest Time to Competition First, Round Robin and Lottery Schedulers.
A process can be instantiated as Process(x,y,z) where
x is the time of arrival of the process
y is the total amount of seconds the process takes to complete
z is the process identifier 

Each scheduler function takes in a process list argument, which is a list of all processes to be exectued.
The round robin scheduler takes in an additonal argument, time-slice which is how many seconds each process executes for before being switched. 
