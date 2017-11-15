import numpy as np


def waiting_time(data, wt):
    exe_time = []
    complete = t = shortest = 0
    n = len(data)
    wt = [0]*n
    minx = 10000000
    check = False

    for i in data:
        exe_time.append(float(i[2]))

    while(complete != n):
        for j in range(n):
            if (float(data[j][1]) <= t and
               exe_time[j] <= minx and exe_time[j] > 0):
                # if two burst time are same
                if exe_time[j] == minx:
                    temp = min(data[j][5], data[shortest][5])
                    if temp == data[j][5]:
                        tie = j
                    elif temp == data[shortest][5]:
                        tie = shortest
                    minx = exe_time[tie]
                    shortest = tie

                else:
                    minx = exe_time[j]
                    shortest = j
                check = True

        if not check:
            t += 1
            continue

        exe_time[shortest] -= 1

        minx = exe_time[shortest]
        if minx == 0:
            minx = 10000000

        if exe_time[shortest] == 0:
            complete += 1
            finish_time = t + 1
            wt[shortest] = (finish_time - float(data[shortest][2])
                            - float(data[shortest][1]))
            wt[shortest] = max(wt[shortest], 0)

        t += 1
    return wt


def turn_around(data, wt, tat):
    tat = [0]*len(data)
    for i in range(0, len(data)):
        tat[i] = wt[i] + float(data[i][2])
    return tat


def sjf(data):
    wt = []
    tat = []
    print("\n ======= Data Input ======= \n")
    print('Name \t Arrival Time \tBurst Time \t Elapsed Time \t'
          + 'Waiting & Processing Time \t Priority')
    for i in data:
        print(str(i[0]) + "\t\t" + str(i[1]) + "\t    " + str(i[2])
              + "\t\t    " + str(i[3]) + "\t\t\t   " + str(i[4])
              + "\t\t\t    " + str(i[5]))
    print()
    fwt = waiting_time(data, wt)
    ntat = turn_around(data, fwt, tat)

    print("\n ====== Output Data =======\n")
    print('Name \t Total Waiting Time \t Turned-around Time')
    for i in range(0, len(data)):
        print(str(data[i][0]) + "\t\t" + str(fwt[i]) + "\t\t\t" + str(ntat[i]))
    print()
    print('Total waiting time: ', sum(fwt))
    print('Average waiting Time : ', sum(fwt) / len(fwt))
    print('Average Turn-around Time : ', sum(ntat) / len(ntat))
    print('Standard Deviation of Turnaround Time : ', np.std(ntat))
    print()


def main():
    inputdata = [[]]
    # filename = 'inp.txt'
    filename = input('Enter input file name: ')
    '''
    name
    arrival time
    total execution time
    elapsed time between I/O interrupts (system calls)
    time spent waiting and processing the I/O
    priority
    '''
    with open(filename, 'r') as input_file:
        inputdata = [line[:-1].split(' ') for line in input_file]
        # line[:-1] is to remove '\n' coming at end.

    # Changed arrival time to relative arrival time
    for i in range(len(inputdata)):
        inputdata[i][1] = float(inputdata[i][1])
        if i > 0:
            inputdata[i][1] += inputdata[i-1][1]

    print("Do you want to consider time taken in interrupts?")
    print("1. Yes\n2. No")
    choice = input()
    if choice == '1':
        for i in range(0, len(inputdata)):
            inputdata[i][2] = float(inputdata[i][2])
            inputdata[i][2] += float(inputdata[i][3])
        sjf(inputdata)

    elif choice == '2':
        sjf(inputdata)


if __name__ == '__main__':
        main()
