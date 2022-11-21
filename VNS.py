import numpy as np
import pickle
import copy
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import gen_solution
from gen_solution import Doctor, Solution


def get_forward_range(solution, doctor, ind):
    day = doctor.start[ind] // 24
    if (ind-1) >= 0 and doctor.start[ind-1] // 24 == day:
        forward_range = list(range(doctor.end[ind-1] + 2, doctor.start[ind])) #约束4：间隔2h
    else:
        forward_range = list(range(day*24 + 7, doctor.start[ind]))
    for s in forward_range:
        e = s + doctor.end[ind] - doctor.start[ind]
        if 1 in solution.schedule[e:doctor.end[ind]]: #约束8：至少有1人值班
            forward_range.remove(s)
    return forward_range


def get_back_range(solution, doctor, ind):
    day = doctor.start[ind] // 24
    if (ind + 1) < len(doctor.start) and doctor.start[ind + 1] // 24 == day:
            back_range = list(range(doctor.end[ind] + 1, doctor.start[ind + 1] - 2)) #约束4：间隔2h
    else:
        if doctor.dayornight[(day + 1) % 7] == 3:
            back_range = list(range(doctor.end[ind] + 1, day * 24 + 16 + 1)) #约束8：夜班前8h不上班
        else:
            back_range = list(range(doctor.end[ind] + 1, day * 24 + 24 + 1))
    for e in back_range:
        s = e - doctor.end[ind] + doctor.start[ind]
        if 1 in solution.schedule[doctor.start[ind]: s]: #约束8：至少有1人值班
            back_range.remove(e)
    return back_range


def Move(init_solution): #平移
    solution = copy.deepcopy(init_solution)
    best_obj = init_solution.get_objection()
    best_sol = copy.deepcopy(init_solution)
    for doctor in solution.doc_list:
        for i in range(len(doctor.start)):
            if doctor.start[i] % 24 == 0: #夜班不移动
                continue
            else:
                origin_start = doctor.start[i]
                origin_end = doctor.end[i]
                forward_range = get_forward_range(solution, doctor, i)
                back_range = get_back_range(solution, doctor, i)
                h = doctor.end[i] - doctor.start[i]
                for num in range(len(forward_range)):
                    doctor.start[i] = forward_range[num]
                    doctor.end[i] = forward_range[num] + h
                    if solution.get_objection() < best_obj -0.1:
                        best_obj = solution.obj
                        best_sol = copy.deepcopy(solution)
                    doctor.start[i] = origin_start
                    doctor.end[i] = origin_end
                for num in range(len(back_range)):
                    doctor.end[i] = back_range[num]
                    doctor.start[i] = back_range[num] - h
                    if solution.get_objection() < best_obj -0.1:
                        best_obj = solution.obj
                        best_sol = copy.deepcopy(solution)
                    doctor.start[i] = origin_start
                    doctor.end[i] = origin_end
    print("Move shift: ", "Objection =", best_sol.obj, "max_len =", max(best_sol.length), "doctor_num =", best_sol.__len__(), "len_flag", best_sol.len_flag)
    return best_sol


def shorten(init_solution): #缩短班次
    solution = copy.deepcopy(init_solution)
    best_obj = init_solution.get_objection()
    best_sol = copy.deepcopy(init_solution)
    for doctor in solution.doc_list:
        for i in range(len(doctor.start)):
            if doctor.start[i] % 24 == 0: #夜班不动
                continue
            elif  doctor.end[i] - doctor.start[i] == 4:
                continue
            else:
                origin_start = doctor.start[i]
                origin_end = doctor.end[i]
                start_delay_range = list(range(doctor.start[i] + 1, doctor.start[i] - 4 + 1))
                end_advance_range = list(range(doctor.start[i] + 4, doctor.end[i]))
                for s in start_delay_range:
                    if 1 in solution.schedule[doctor.start[i]: s]: #约束8：至少有1人值班
                        continue
                    else:
                        doctor.start[i] = s
                        if solution.get_objection() < best_obj:
                            best_obj = solution.obj
                            best_sol = copy.deepcopy(solution)
                        doctor.start[i] = origin_start
                for e in end_advance_range:
                    if 1 in solution.schedule[e: doctor.end[i]]: #约束8：至少有1人值班
                        continue
                    else:
                        doctor.end[i] = e
                        if solution.get_objection() < best_obj:
                            best_obj = solution.obj
                            best_sol = copy.deepcopy(solution)
                        doctor.end[i] = origin_end
    print("Shorten shift: ", "Objection =", best_sol.obj, "max_len =", max(best_sol.length), "doctor_num =", best_sol.__len__(), "len_flag", best_sol.len_flag)
    return best_sol



def extend(init_solution): #延长班次
    solution = copy.deepcopy(init_solution)
    best_obj = init_solution.get_objection()
    best_sol = copy.deepcopy(init_solution)
    for doctor in solution.doc_list:
        for i in range(len(doctor.start)):
            day = doctor.start[i] // 24
            h = doctor.end[i] - doctor.start[i]
            if doctor.start[i] % 24 == 0: #夜班不动
                continue
            elif  h == 8:
                continue
            elif sum(doctor.schedule[day*24 : (day+1)*24]) == 10:
                continue
            else:
                origin_start = doctor.start[i]
                origin_end = doctor.end[i]
                if i - 1 >= 0 and doctor.start[i - 1] // 24 == day: #当天当前班次前面有班次
                    h_before = doctor.end[i - 1] - doctor.start[i - 1]
                    if h_before + h < 10:
                        start_advance_range = list(range(max(doctor.end[i-1] + 2, doctor.start[i] - (10-h_before) + h), doctor.start[i]))
                        if doctor.dayornight[(day + 1) % 7] == 3:
                            end_delay_range = list(range(doctor.end[i] + 1, min(day * 24 + 16, doctor.end[i] + (10-h_before) - h) + 1)) #约束8：夜班前8h不上班
                        else:
                            end_delay_range = list(range(doctor.end[i] + 1, min(day * 24 + 24, doctor.end[i] + (10-h_before) - h) + 1))
                    else:
                        continue
                elif i + 1 < len(doctor.start) and doctor.start[i + 1] // 24 == day:#当天当前班次后面有班次
                    h_after = doctor.end[i + 1] - doctor.start[i + 1]
                    if h_after + h < 10:
                        start_advance_range = list(range(max(day*24 + 7, doctor.start[i] - (10-h_after) + h), doctor.start[i]))
                        end_delay_range = list(range(doctor.end[i] + 1, min(doctor.start[i + 1] - 2, doctor.end[i] + (10-h_after) - h) + 1))
                    else:
                        continue
                else: #当天当前只有一个班次
                    start_advance_range = list(range(max(day*24 + 7, doctor.start[i] - 8 + h), doctor.start[i]))
                    if doctor.dayornight[(day + 1) % 7] == 3:
                        end_delay_range = list(range(doctor.end[i] + 1, min(day * 24 + 16, doctor.end[i] + 8 - h) + 1)) #约束8：夜班前8h不上班
                    else:
                        end_delay_range = list(range(doctor.end[i] + 1, min(day * 24 + 24, doctor.end[i] + 8 - h) + 1))
        
                for s in start_advance_range:
                    doctor.start[i] = s
                    if solution.get_objection() < best_obj -0.1:
                        best_obj = solution.obj
                        best_sol = copy.deepcopy(solution)
                    doctor.start[i] = origin_start
                for e in end_delay_range:
                    doctor.end[i] = e
                    if solution.get_objection() < best_obj -0.1:
                        best_obj = solution.obj
                        best_sol = copy.deepcopy(solution)
                    doctor.end[i] = origin_end
    print("Extend shift: ", "Objection =", best_sol.obj, "max_len =", max(best_sol.length), "doctor_num =", best_sol.__len__(), "len_flag", best_sol.len_flag)
    return best_sol


def increse_shift(init_solution): #增加班次
    solution = copy.deepcopy(init_solution)
    best_obj = init_solution.get_objection()
    best_sol = copy.deepcopy(init_solution)
    for doctor in solution.doc_list:
        for day in range(7):
            if doctor.rest_day == day or doctor.dayornight[day] == 3:
                continue
            elif doctor.dayornight[day] == 1: 
                ind, start_last = gen_solution.find_day_ind(day, doctor.start)
                end_last = doctor.end[ind]
                hour = end_last - start_last
                if start_last - 2 >= day*24 + 7 + 4 and hour < 7:
                    start =  gen_solution.gen_prob_randint(solution.length, day*24 + 7, start_last - 2 - 4)
                    if gen_solution.Night_restraint(day, start, doctor):
                        doctor.start.append(start)
                        doctor.dayornight[day] += 1
                        end = random.randint(start + 4, min(start_last - 2, start + 10 - hour))
                        doctor.end.append(end)
                    else:
                        break
                elif end_last + 2 < (day+1)*24-4 and hour < 7:
                    start = gen_solution.gen_prob_randint(solution.length, end_last + 2, (day+1) * 24 - 4)
                    if gen_solution.Night_restraint(day, start, doctor):
                        doctor.start.append(start)
                        doctor.dayornight[day] += 1
                        if doctor.dayornight[(day + 1) % 7] == 3:
                            end_limit = day * 24 + 16
                            end = random.randint(start + 4, min(end_limit, start + 10 - hour))
                            doctor.end.append(end)
                        else:
                            end = random.randint(start + 4, min((day + 1)*24, start + 10-hour))
                            doctor.end.append(end)
                    else:
                        break
                else:
                    break
            elif doctor.dayornight[day] == 0:
                start =  gen_solution.gen_prob_randint(solution.length, day * 24 + 7, (day+1)* 24 - 4) #约束：夜间不上下班
                if gen_solution.Night_restraint(day, start, doctor):
                    doctor.dayornight[day] += 1
                    doctor.start.append(start)
                    if doctor.dayornight[(day + 1) % 7] == 3:
                        end_limit = day * 24 + 16
                        end = random.randint(start + 4, min(end_limit, start + 8))
                        doctor.end.append(end)
                    else:
                        end = start + random.randint(4, min(8, (day + 1)*24 - start))
                        doctor.end.append(end)
                else:
                    break
            doctor.start.sort()
            doctor.end.sort()
            if solution.get_objection() < best_obj - 0.1:
                best_obj = solution.obj
                best_sol = copy.deepcopy(solution)
                doctor.start.remove(start)
                doctor.end.remove(end)
                doctor.dayornight[day] -= 1
            else:
                continue
    print("Increse shift: ", "Objection =", best_sol.obj, "max_len =", max(best_sol.length), "doctor_num =", best_sol.__len__(), "len_flag", best_sol.len_flag)
    return best_sol


def decrese_shift(init_solution): #减少班次
    solution = copy.deepcopy(init_solution)
    best_obj = init_solution.get_objection()
    best_sol = copy.deepcopy(init_solution)
    for doctor in solution.doc_list:
        for i in range(len(doctor.start)):
            if doctor.start[i] % 24 == 0: #夜班不动
                continue
            else:
                origin_start = doctor.start[i]
                origin_end = doctor.end[i]
                del doctor.start[i]
                del doctor.end[i]
                day = origin_start // 24
                doctor.dayornight[day] -= 1 
                if solution.constraint_flag == True and solution.get_objection() < best_obj -0.1:
                    best_obj = solution.get_objection()
                    best_sol = copy.deepcopy(solution)
                doctor.start.append(origin_start)
                doctor.end.append(origin_end)
                doctor.start.sort()
                doctor.end.sort()
                doctor.dayornight[day] += 1
    print("Decrese shift: ", "Objection =", best_sol.obj, "max_len =", max(best_sol.length), "doctor_num =", best_sol.__len__(),"len_flag", best_sol.len_flag)
    return best_sol


def add_doc(init_solution): #增加人数
    solution = copy.deepcopy(init_solution)
    best_sol = copy.deepcopy(init_solution)
    best_obj = init_solution.get_objection()
    solution.doc_list.append(Doctor(random.randint(0,6)))
    count = 0
    while count < 15:
        solution.doc_list = gen_solution.gen_init(solution)
        if solution.get_objection() < best_obj -0.1:
            best_obj = solution.get_objection()
            best_sol = copy.deepcopy(solution)
        else:
            count += 1
            solution = copy.deepcopy(init_solution)
    print("Add Doctor: ", "Objection =", solution.obj, "max_len =", max(solution.length), "doctor_num =", solution.__len__(), "len_flag", solution.len_flag)
    return best_sol


def reduce_doc(init_solution): #减少人数
    solution = copy.deepcopy(init_solution)
    while True:
        i = random.randint(0,solution.__len__() - 1)
        if 3 in solution.doc_list[i].dayornight:
            continue
        else:
            del solution.doc_list[i]
            print("Red Doctor: ", "Objection =", solution.get_objection(), "max_len =", max(solution.length), "doctor_num =", solution.__len__(), "len_flag", solution.len_flag)
            return solution


def rearrange(init_solution, k): #重新安排k个医生
    print("Rearrange before: ", "Objection =", init_solution.obj, "doctor_num =", init_solution.__len__())
    solution = copy.deepcopy(init_solution)
    doc_ind_list = random.sample(range(0, init_solution.__len__()), k)
    for i, ind in enumerate(doc_ind_list):
        doctor = solution.doc_list[ind]
        if 3 in doctor.dayornight:
            start_store = []
            end_store = []
            dayornight = [0 for i in range(7)]
            for i, s in enumerate(doctor.start):
                if s % 24 == 0:
                    start_store.append(s)
                    end_store.append(doctor.end[i])
                    dayornight[s // 24] = 3
            doctor.__init__()
            doctor.start = copy.deepcopy(start_store)
            doctor.end = copy.deepcopy(end_store)
            doctor.dayornight = copy.deepcopy(dayornight)
            discard = []
            for d in range(7):
                if doctor.dayornight[d] == 3:
                    discard.append(d)
            doctor.rest_day = gen_solution.gen_randint(0, 6, discard) #约束6:休息一整天         
        else:
            doctor.__init__(random.randint(0,6))
    solution = gen_solution.gen_init(solution)
    print("Rearrange%d: "%k, "Objection =", solution.get_objection(), "max_len =", max(solution.length), "doctor_num =", solution.__len__(), "len_flag", solution.len_flag)
    return solution

            
def VND(init_solution, l_max):
    solution = copy.deepcopy(init_solution)
    cf_solution = []
    step = 0
    while step < l_max:
        print('step:', step) 
        if step == 1:
            candidate = Move(solution)
        elif step == 3:
            candidate = decrese_shift(solution)
        elif step == 0:
            candidate = extend(solution)
        elif step == 2:
            candidate = increse_shift(solution)
        # objection_list.append(candidate.obj)
        # plot_obj(objection_list)

        if candidate.constraint_flag() == True:
            if candidate.get_objection() < solution.get_objection() -0.1:
                solution  = copy.deepcopy(candidate)
                step = 0
            else:
                step += 1
        else:
            print('constraint_flag=False')
            cf_solution.append((candidate, step))
            solution  = copy.deepcopy(candidate)
            step = (step + 1) % l_max
            if step == cf_solution[0][1]:
                return cf_solution[0][0]
    return solution 


def VNS(initial_solution, l_max = 4, k_max = 1, iteration = 10):
    print("Initial: ", "Objection =", initial_solution.obj, "max_len =", max(initial_solution.length), "doctor_num =", initial_solution.__len__(), "len_flag", initial_solution.len_flag)
    k = 0
    initial_solution.iter = 0
    best_solution = copy.deepcopy(initial_solution)
 
    while(k < k_max):
        x1 = rearrange(best_solution, k + 1)
        x2 = VND(x1, l_max)

        if best_solution.len_flag == False or x2.len_flag == True:
            obj = x2.get_objection()
            while True:
                x2 = shorten(x2)
                if x2.get_objection() == obj:
                    break
                else:
                    obj = x2.get_objection()
        
        for doc in x2.doc_list: #check
            doc.check()

        if (x2.get_objection() < best_solution.get_objection()):
            best_solution = copy.deepcopy(x2)
            print("temp best shcedule =", best_solution.schedule)
            k = 0
        else:
            k += 1
        print("Iteration = ", k,  "Objection =", best_solution.obj, "max_len =", max(best_solution.length), "doctor_num =", best_solution.__len__(),"len_flag", best_solution.len_flag)
    return best_solution


def plot_obj(y):
    x = [i for i in range(len(y))]
    plt.figure(figsize=(10,6),dpi=100)
    plt.plot(x, y, 'o-', alpha=0.5, linewidth=1, label='objection')
    plt.legend() 
    plt.xlabel('iteration')
    plt.ylabel('obj')
    plt.savefig("./obj.png")
    plt.close()

def plot_len_contrast(y1, y2):
    x = [i for i in range(len(y1))]
    plt.figure(figsize=(10,6),dpi=100)
    plt.plot(x, y1, 'o-', color = 'blue', alpha=0.5, linewidth=1, label='init_len')
    plt.legend()
    plt.plot(x, y2, 'o-', color = 'red',alpha=0.5, linewidth=1, label='len')
    plt.legend()
    plt.xlabel('time')
    plt.ylabel('people')

    x_major_locator = MultipleLocator(12)
    ax=plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)

    plt.savefig("./len_contrast.png")
    plt.close()

