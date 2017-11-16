import numpy as np
from copy import copy, deepcopy
import matplotlib.pyplot as plt

avg_array = []
quantum_array = []
tat_array = []


def findWaitingTime(at, n, bt, wt, quantum):
    # Make a copy of burst times bt[] to store remaining burst times.
    rem_bt = []
    rem_bt = deepcopy(bt)
    t = 0  # Current time
    # Keep traversing processes in round robin manner
    # until all of them are not done.
    done = False
    while not done:
        done = True
        # Traverse all processes one by one repeatedly
        for i in range(n):
            # If burst time of a process is greater than 0
            # then only need to process further
            if rem_bt[i] > 0:
                done = False  # There is a pending process
                if rem_bt[i] > quantum:
                    # Increase the value of t i.e. shows how much
                    # time a process has been processed
                    t += quantum
                    # Decrease the burst_time of current process by quantum
                    rem_bt[i] -= quantum

                # If burst time is smaller than or equal to quantum.
                # Last cycle for this process
                else:
                    # Increase the value of t i.e. shows
                    # how much time a process has been processed
                    t = t + rem_bt[i]
                    # Waiting time is current time minus
                    # time used by this process
                    wt[i] = t - bt[i] - at[i]
                    # As the process gets fully executed make its
                    # remaining burst time = 0
                    rem_bt[i] = 0


def findTurnAroundTime(n, bt, wt, tat):
    # calculating turnaround time by adding bt[i] + wt[i]
    for i in range(n):
        tat[i] = bt[i] + wt[i]


# Function to calculate average time
def findavgTime(at, n, bt, quantum):
    wt = [0]*n
    tat = [0]*n
    total_wt = 0
    total_tat = 0

    # Function to find waiting time of all processes
    findWaitingTime(at, n, bt, wt, quantum)

    # Function to find turn around time for all processes
    findTurnAroundTime(n, bt, wt, tat)

    # Display processes along with all details
    print("Processes   Arrival time   Burst time   " +
          "Waiting time   Turn around time\n")

    # Calculate total waiting time and total turn around time
    for i in range(0, n):
        total_wt += wt[i]
        total_tat += tat[i]
        print("    " + str(i+1) + "\t\t" + str(at[i]) + "\t\t" + str(bt[i])
              + "\t     " + str(wt[i]) + "\t\t" + str(tat[i]) + "\n")

    average_time = float(total_wt / n)
    avg_array.append(average_time)
    tat_array.append(total_tat)

    print("Average waiting time = ", sum(wt) / len(wt))
    print("Average turn around time = ", sum(tat) / len(tat))
    print('Standard Deviation of Turnaround Time : ', np.std(tat))
    print()


def main():
    p = []
    at = []
    burst_time = []

    filename = input("Enter the file to be read: ")
    # filename = 'inp.txt'
    f = open(filename, "r")

    if f.mode == 'r':
        print("The file is ready to be read")

    contents = f.read().splitlines()
    n = len(contents)
    # will split according '\n'. It will split all the values into 2D array.

    for i in range(n):
        p.append(contents[i].split(' '))

    print("Do you want to consider time taken in interrupts?")
    print("1. Yes\n2. No")
    choice = input()
    # choice = 1
    if choice == '1':
        for i in p:
            p[2] += (p[3])

    for i in range(len(p)):
        for j in range(i):
            p[i][1] = int(p[i][1]) + int(p[j][1])

    for i in range(n):
        at.append(float(p[i][1]))
        burst_time.append(float(p[i][2]))

    print("Burst Time: ", burst_time)

    for i in range(10):
        quantum = 1 + i
        quantum_array.append(quantum)
        findavgTime(at, n, burst_time, quantum)

    plt.scatter(quantum_array, avg_array)
    plt.xlabel("Quantum size (Time Slice)")
    plt.ylabel("Average Waiting Time")
    plt.title('Q vs AWT')
    plt.show()


if __name__ == '__main__':
    main()
