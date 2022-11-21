# GA-VNS-for-Emergency-Department-doctor-scheduling
Hybrid genetic algorithm and heuristic algorithm of variable neighborhood search problem solve the problem of doctor scheduling in emergency department

### Problem Statement


- A day is divided into 24 hour-long periods on average. The defined starting point of a week is zero on Monday, assuming that no patients are in the system at this starting point.

- The arrival rate of patients can be different in different time periods, but the arrival rate of patients in a time period remains unchanged. The patient arrival rate per hour t is $\lambda_t$

- Service rate for each doctor is constant and all are $\mu$

- A doctor who is off duty and still has a patient on hand should return the patient to the front of the queue; In particular, Doctor A is off duty at the time of the patient's visit (required service time a, at which time a' has been performed), and the next doctor B is at work at the same position (service time for the patient is still a, requiring another A-A '), because of the nature of the exponential distribution.

- Emergency physicians can only commute at the beginning or end of each session. The patient queue is subject to the first come, first served rule (FCFS), assuming that there are no patients who leave without being served. The whole system can be thought of as a $ 𝑀_𝑡 /𝑀 / 𝑝_𝑡$ queuing system (including $𝑝_𝑡$ needs to be determined by the doctor roaster).

- There are $N$ ($N = 10 $)doctors in the emergency department

- Each doctor is allowed a maximum of two day shifts, or 1 night shift 24 hours a day starting at midnight

- Night shift: 0-7, during which doctors are not allowed to work. Night doctors are not allowed to work eight hours before the start of the night shift (after 17:00 the previous day) or on the day the night shift ends. A doctor must immediately rest for 24 hours straight after his night shift before he can be assigned a new job. A doctor works no more than two night shifts a week.

- The maximum length of a doctor's shift is 8 hours and the minimum is 4 hours. Doctors spend no more than 10 hours a day on the job. Every doctor should take at least one full day off in a week, i.e., 24h (from 0:00 to 0:00 the next day).

- At least one doctor is on duty at any one time serving patients

- At the end of each hour, the number of patients in the system (queue + people being served), whose expected value (or some approximation of the expected value) does not exceed an upper threshold.

- If there are not enough doctors in the department, doctors from other departments can be seconded. A seconded doctor will incur a seconded cost c(per week)

- Goal: Aim to minimize all doctors in a week (including the total number of hours on secondment plus the cost of secondment). Ask for each doctor's daily commute time.

