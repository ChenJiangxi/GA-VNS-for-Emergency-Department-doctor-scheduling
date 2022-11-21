"""
Time:2022-11-21
Author: Chen jiangxi
Describe: generate solutions for emergency department doctor scheduling
"""

import numpy as np
import random
import csv
import copy
import pickle
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

from B_PSFFA import bisection

class Doctor:
    def __init__(self, rest_day = None):
        self.workingtime = 0
        self.rest_day = rest_day
        self.dayornight = [0 for i in range(7)] #长度为7的数组，0,1,2为当天白班个数，3为当天夜班
        self.start = []
        self.end = []
        self.schedule = [0 for i in range(168)]

    def Sol2Sche(self):
        self.schedule = [0 for i in range(168)]
        for i in range(len(self.start)):
            for n in range(self.end[i] - self.start[i]):
                self.schedule[self.start[i]+n] = 1
    
    def cal_each_shift(self):
        for i in range(len(self.start)):
            if self.end[i] - self.start[i] > 8 :
                print(self.start[i], self.end[i], "单个班次时长大于8")
                return False
            if self.end[i] - self.start[i] < 4 :
                print(self.start[i], self.end[i], "单个班次时长小于4")
                return False 
        return True

    def cal_one_day(self):
        for day in range(7):
            hour = 0
            for i, s in enumerate(self.start):
                if s // 24 == day:
                    hour += self.end[i] - self.start[i]
            if hour > 10:
                print(day, self.schedule[day * 24: (day + 1)*24], "一天班次时长大于10")
                return False
        return True

    def shift_interval(self):
        for i in range(len(self.start)):
            if i - 1 >= 0 and self.start[i] - self.end[i - 1] < 2:
                print(self.start[i], self.end[i - 1], "两个班次间隔时长小于2")
                return False
            elif i - 1 < 0 and self.start[i] - self.end[i - 1] + 168 < 2:
                print(self.start[i], self.end[i - 1], "两个班次间隔时长小于2")
                return False
        return True
    
    def night_restraint(self):
        for day in range(7):
            if self.dayornight[day] == 3:
                if sum(self.schedule[day * 24 - 8: day * 24]) > 0:
                    print(day, "夜班前8h有班次")
                    return False
                elif sum(self.schedule[day * 24 + 7: (day+1) * 24 + 7]) > 0:
                    print(day, "夜班后24h有班次")
                    return False
        return True
    
    def check(self):
        if self.cal_each_shift() and self.cal_one_day() and self.shift_interval() and self.night_restraint():
            return True
        else:
            return False


class Solution:
    def __init__(self, Doc_list, week) -> None:
        self.obj = None
        self.doc_list = copy.deepcopy(Doc_list)
        self.schedule = [0 for i in range(168)]
        self.length = []
        self.len_flag = None
        self.lam = week
        self.iter = 0

    def __len__(self):
        return len(self.doc_list)

    def get_objection(self):
        penalty_factor = exponential_decay(self.iter)
        self.schedule = [0 for i in range(168)]
        for doc in self.doc_list:
            doc.Sol2Sche()
            self.schedule = np.sum([self.schedule, doc.schedule],axis=0).tolist()
        self.obj = sum(self.schedule) + 10 * (self.__len__() - 10)
        self.get_len()
        for l in self.length:
            if l > 15:
                self.obj += penalty_factor * l #让目标函数加上最大队长（惩罚系数动态调整）
        return self.obj
    
    def get_len(self):
        mu = 5.9114
        self.len_flag, self.length = est_len(self.lam, mu, self.schedule)
        return self.len_flag, self.length

    def constraint_flag(self):
        if 0 in self.schedule:
            return False
        else:
            return True

def exponential_decay(t, init = 5, m = 10, finish = 0.5):
    alpha = np.log(init / finish) / m
    l = - np.log(init) / alpha
    decay = np.exp(-alpha * (t + l))
    return decay


def gen_init(solution):
    for doctor in solution.doc_list:
        for day in range(7):
            if doctor.rest_day == day or doctor.dayornight[day] == 3:
                continue
            else:
                while(doctor.dayornight[day] < 2): #约束1：2白or1夜
                    if doctor.dayornight[day]  == 1:
                        ind, start_last = find_day_ind(day, doctor.start)
                        end_last = doctor.end[ind]
                        hour = end_last - start_last
                        if start_last - 2 >= day*24 + 7 + 4 and hour < 7:
                            start =  gen_prob_randint(solution.length, day*24 + 7, start_last - 2 - 4)
                            if Night_restraint(day, start, doctor):
                                doctor.dayornight[day] += 1
                                doctor.start.append(start)
                                end = random.randint(start + 4, min(start_last - 2, start + 10 - hour))
                                doctor.end.append(end)
                                # print("a",start, end)
                            else:
                                break
                        elif end_last + 2 < (day+1)*24-4 and hour < 7:
                            start = gen_prob_randint(solution.length, end_last + 2, (day+1) * 24 - 4)
                            if Night_restraint(day, start, doctor):
                                doctor.start.append(start)
                                doctor.dayornight[day] += 1
                                if doctor.dayornight[(day + 1) % 7] == 3:
                                    end_limit = day * 24 + 16
                                    end = random.randint(start + 4, min(end_limit, start + 10 - hour))
                                    doctor.end.append(end)
                                    # print("b",start, end)
                                else:
                                    end = random.randint(start + 4, min((day + 1)*24, start + 10-hour))
                                    doctor.end.append(end)
                                    # print("c",start, end)
                            else:
                                break
                        else:
                            break
                    else:
                        start = gen_prob_randint(solution.length, day*24 + 7, (day+1)*24 - 4)#约束：夜间不上下班。第一个白班先在上午开始
                        if Night_restraint(day, start, doctor):
                            doctor.dayornight[day] += 1
                            doctor.start.append(start)
                            if doctor.dayornight[(day + 1) % 7] == 3:
                                end_limit = day * 24 + 16
                                end = random.randint(start + 4, min(end_limit, start + 8))
                                doctor.end.append(end)
                                # print("d",start, end)
                            else:
                                end = start + random.randint(4, min(8, (day + 1)*24 - start))
                                doctor.end.append(end)
                                # print("e",start, end)
                        else:
                            break
                    doctor.start.sort()
                    doctor.end.sort()
                    doctor.Sol2Sche()
                    doctor.check()
    return solution


def greed(Doc_list): 
    for i in range(len(Doc_list)):
        if i < 7:
            Doc_list[i].dayornight[i % 7] = 3
            Doc_list[i].start.append((i % 7) * 24)
            Doc_list[i].end.append((i % 7) * 24 + 7)
        if i - 1 >= 0 and i - 1 <= 6:
            Doc_list[i].dayornight[i - 1] += 1
            Doc_list[i].start.append((i-1)*24 + 7)
            Doc_list[i].end.append((i-1)*24 + 15)
        if i - 2 >= 0 and i -2 <= 6:
            Doc_list[i].dayornight[i - 2] += 1
            Doc_list[i].start.append((i-2)*24 + 12)
            Doc_list[i].end.append((i-2)*24 + 20)
        if i - 3 >= 0 and i -3 <= 6:
            Doc_list[i].dayornight[i - 3] += 1
            Doc_list[i].start.append((i-3)*24 + 16)
            Doc_list[i].end.append((i-3)*24 + 24)
        if i - 4 >= 0 and i -4 <= 6:
            if i == 8:
                continue
            else:
                Doc_list[i].dayornight[(i-4) % 7] = 3
                Doc_list[i].start.append(((i-4) % 7) * 24)
                Doc_list[i].end.append(((i-4) % 7) * 24 + 7)
        if i == 1:
            Doc_list[i].dayornight[6] = 3
            Doc_list[i].start.append(6 * 24)
            Doc_list[i].end.append(6 * 24 + 7)

    for i in range(len(Doc_list)):
        Doc_list[i].start.sort()
        Doc_list[i].end.sort()
        discard = []
        for d in range(7):
            if Doc_list[i].dayornight[d] > 0:
                discard.append(d)
        Doc_list[i].rest_day = gen_randint(0, 6, discard) #约束6:休息一整天
    return Doc_list


def greed_2(Doc_list): 
    for i in range(len(Doc_list)):
        if i < 7:
            Doc_list[i].dayornight[i % 7] = 3
            Doc_list[i].start.append((i % 7) * 24)
            Doc_list[i].end.append((i % 7) * 24 + 7)
        if i - 1 >= 0 and i - 1 <= 6:
            Doc_list[i].dayornight[i - 1] += 1
            Doc_list[i].start.append((i-1)*24 + 7)
            Doc_list[i].end.append((i-1)*24 + 15)
        if i - 2 >= 0 and i -2 <= 6:
            Doc_list[i].dayornight[i - 2] += 1
            Doc_list[i].start.append((i-2)*24 + 12)
            Doc_list[i].end.append((i-2)*24 + 20)
        if i - 3 >= 0 and i -3 <= 6:
            Doc_list[i].dayornight[i - 3] += 1
            Doc_list[i].start.append((i-3)*24 + 16)
            Doc_list[i].end.append((i-3)*24 + 24)
        if i - 4 >= 0 and i -4 <= 6:
            if i == 7:
                Doc_list[i].dayornight[1] = 3
                Doc_list[i].start.append(1 * 24)
                Doc_list[i].end.append(1 * 24 + 7)
            else:
                Doc_list[i].dayornight[(i-4) % 7] = 3
                Doc_list[i].start.append(((i-4) % 7) * 24)
                Doc_list[i].end.append(((i-4) % 7) * 24 + 7)
        if i == 1 or i == 2:
            Doc_list[i].dayornight[6] = 3
            Doc_list[i].start.append(6 * 24)
            Doc_list[i].end.append(6 * 24 + 7)
        if i == 0:
            Doc_list[i].dayornight[4] = 3
            Doc_list[i].start.append(4 * 24)
            Doc_list[i].end.append(4 * 24 + 7)
        if i == 8:
            Doc_list[i].dayornight[2] = 3
            Doc_list[i].start.append(2 * 24)
            Doc_list[i].end.append(2 * 24 + 7)

    for i in range(len(Doc_list)):
        Doc_list[i].start.sort()
        Doc_list[i].end.sort()
        discard = []
        for d in range(7):
            if Doc_list[i].dayornight[d] > 0:
                discard.append(d)
        Doc_list[i].rest_day = gen_randint(0, 6, discard) #约束6:休息一整天
    return Doc_list

def find_day_ind(day, list, flag = 0):
    for ind in range(len(list)):
        if flag == 1: #end
            if list[ind] % 24 != 0 and list[ind] // 24 == day:
                return list[ind]
            elif list[ind] % 24 == 0 and list[ind] // 24 == day+1:
                return list[ind]
        else: #start
            if list[ind] // 24 == day:
                return ind, list[ind]


def gen_randint(low, high, discard_list):
    result_list = list(range(low, high+1))
    for i in range(len(discard_list)):
            result_list.remove(discard_list[i])
    np.random.shuffle(result_list)
    return result_list.pop()


def gen_prob_randint(length, low, high):
    p = []
    result_list = list(range(low, high+1))
    hour_list = length[low:high+1]
    for n in range(high - low + 1):
        p.append(hour_list[n] - 15)
    if len(p) > 1:
        min_p = min(p)
        p = [i - min_p for i in p]
    prob = np.array([i / sum(p) for i in p])
    # prob = np.exp(p)/sum(np.exp(p)) #softmax 归一化
    return max(low, np.random.choice(result_list, p=prob.ravel())-3) #预防机制


def Night_restraint(day, start, Doctor): #约束4：前8，后24不上班
    night_day = [i for i, x in enumerate(Doctor.dayornight) if x == 3]
    for i in night_day:
        if i == 0 and day == 6 and start % 24 > 16 - 4:
            return False
        elif i == 6 and day == 0 and start % 24 < 7:
            return False
        else:
            if day == i:
                return False
            elif day == i-1 and start % 24 > 16 - 4:
                return False
            elif day == i+1 and start % 24 < 7:
                return False
    return True


def est_len(lam, mu, schedule): #约束8:队长约束
    length = [0]
    for i, c in enumerate(schedule):
        length.append(bisection(length[i], lam[i], mu, c))
    del length[0]
    if max(length) > 15:
        return False, length
    else:
        return True, length


def read_data(ROOT):
    week1 = []
    week2 = []
    with open(ROOT, 'r') as f:
        reader = csv.reader(f)
        result = list(reader)
        for i in range(7):
            week1.extend(result[i])
            week2.extend(result[i+7])
    float_week1 = [float(item) for item in week1]
    float_week2 = [float(item) for item in week2]
    return float_week1, float_week2

def store(sol, i, root):
    with open(root + 'solution%d.pk'%i, 'wb') as f:
        pickle.dump(sol, f)

def plot_len(y):
    x = [i for i in range(168)]
    plt.figure(figsize=(12,6),dpi=100)
    plt.plot(x, y, 'o-', color='#4169E1', alpha=0.5, linewidth=1, label='length')
    plt.legend() 
    plt.xlabel('time')
    plt.ylabel('people')
    x_major_locator = MultipleLocator(12)
    ax=plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    plt.savefig("./len.png")
    plt.close()

def initial(doc_num):
    Doc_list = []
    for i in range(doc_num): 
        Doc_list.append(Doctor())
    Doc_list = greed(Doc_list)
    return Doc_list

def initial_2(doc_num):
    Doc_list = []
    for i in range(doc_num): 
        Doc_list.append(Doctor())
    Doc_list = greed_2(Doc_list)
    return Doc_list


if __name__ == '__main__':
    mu = 5.9113
    ROOT ='lambda.csv'
    week1, week2 = read_data(ROOT)
    Doc_list = initial(10)
    solution = Solution(Doc_list, week1)
    solution.get_objection()

    best_sol = copy.deepcopy(solution)
    Flag = False
    count = 0
    num = 0 
    while(count < 5):
        if num > 1000:
            num = 0
            solution = copy.deepcopy(best_sol)
            solution.doc_list.append(Doctor(random.randint(0,6)))
            count = solution.__len__() - 10
        solution = gen_init(solution)
        if solution.get_objection() < best_sol.get_objection():
            best_sol = copy.deepcopy(solution)
            print('false_add:', best_sol.__len__() - 10)
            print('false_obj:', best_sol.obj)
            plot_len(best_sol.length)
            for i in range(solution.__len__()):
                print('Doctor.%d'%i, solution.doc_list[i].dayornight)
        else:
            num += 1
            if solution.__len__() > 10:
                doctor = solution.doc_list[random.randint(10, solution.__len__() - 1)]
                doctor.__init__(random.randint(0,6))
    # store(solution, solution.obj) #有误
    print("schedule:", solution.schedule)
    print("workingtime:", sum(solution.schedule))
    plot_len(solution.length)
    print("add:", count)
    for i in range(solution.__len__()):
        print('Doctor.%d'%i, solution.doc_list[i].dayornight)

            
