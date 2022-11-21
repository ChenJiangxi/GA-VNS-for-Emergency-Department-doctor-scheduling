# GA-VNS-for-Emergency-Department-doctor-scheduling
Hybrid genetic algorithm of variable neighborhood search heuristic algorithm, to solve the problem of doctor scheduling in emergency department

### Problem Statement


- A day is divided into 24 hour-long periods on average. The defined starting point of a week is zero on Monday, assuming that no patients are in the system at this starting point.

- The arrival rate of patients can be different in different time periods, but the arrival rate of patients in a time period remains unchanged. The patient arrival rate per hour t is $\lambda_t$

- Service rate for each doctor is constant and all are $\mu$

- A doctor who is off duty and still has a patient on hand should return the patient to the front of the queue; In particular, Doctor A is off duty at the time of the patient's visit (required service time a, at which time a' has been performed), and the next doctor B is at work at the same position (service time for the patient is still a, requiring another A-A '), because of the nature of the exponential distribution.

- Emergency physicians can only commute at the beginning or end of each session. The patient queue is subject to the first come, first served rule (FCFS), assuming that there are no patients who leave without being served. The whole system can be thought of as a $𝑀_𝑡$ /$𝑀$ / $𝑝_𝑡$ queuing system (including $𝑝_𝑡$ needs to be determined by the doctor roaster).

- There are $N$ ($N$ = 10)doctors in the emergency department

- Each doctor is allowed a maximum of two day shifts, or 1 night shift 24 hours a day starting at midnight

- Night shift: 0-7, during which doctors are not allowed to work. Night doctors are not allowed to work eight hours before the start of the night shift (after 17:00 the previous day) or on the day the night shift ends. A doctor must immediately rest for 24 hours straight after his night shift before he can be assigned a new job. A doctor works no more than two night shifts a week.

- The maximum length of a doctor's shift is 8 hours and the minimum is 4 hours. Doctors spend no more than 10 hours a day on the job. Every doctor should take at least one full day off in a week, i.e., 24h (from 0:00 to 0:00 the next day).

- At least one doctor is on duty at any one time serving patients

- At the end of each hour, the number of patients in the system (queue + people being served), whose expected value (or some approximation of the expected value) does not exceed an upper threshold.

- If there are not enough doctors in the department, doctors from other departments can be seconded. A seconded doctor will incur a seconded cost c(per week)

- Goal: Aim to minimize all doctors in a week (including the total number of hours on secondment plus the cost of secondment). Ask for each doctor's daily commute time.

### Algrithm

![image](https://user-images.githubusercontent.com/75166126/203094367-89065b47-4862-4ba3-8f1d-55a28229f99b.png)\\

![image](https://user-images.githubusercontent.com/75166126/203094432-47308435-4917-477c-b213-58187a50abdc.png)


### Run
If you want to run General-Variable-Neighborhood-Search, just run `GVNS.py`.
If you want to run Hybrid genetic algorithm of variable neighborhood search heuristic algorithm, just run `GA-VNS.py`.


### Reference

[面向时变非稳态需求的急诊室医生排班研究](https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CMFD&dbname=CMFD201902&filename=1019654958.nh&uniplatform=NZKPT&v=DSlrDCTmUfzIz7pmyhH6xj0k9QmdCTdK2EXmoQM1WIwkK5Ij3KJTPypOeE3io9U1)

[面向时变回诊患者需求的急诊周排班研究](https://qikan.chaoxing.com/detail_38502727e7500f26558dc607da1268812058ce404f0f743c1921b0a3ea255101fc1cf1fbb4666ae6cc3e0043d77d9129660df4a740caeb831655bd7de1a1a83db967f8aa9263830c1b455defb68836d9)

[面向高度时变不确定患者需求的急诊医生周排班方法研究](https://kns.cnki.net/KXReader/Detail?invoice=vV2f2OU2fubYmzY1dzeh1gqr96XwVRKCtqX82ze0kNerMUhz5O1mms454CIEGK4UBqgRSBCBP1KO%2FBMUnvDYRn0SjWbkIpE5vMCj6R0%2FiAu5sW1ydUQL3cCbGKlZm4oqO%2BUvFURk2nkpzQt6wWCRZStWwYfcBDdK5uGnyLF8Q20%3D&DBCODE=CJFD&FileName=GYGC202003021&TABLEName=cjfdlast2020&nonce=95E3E6F47970486498D7321D29414898&uid=&TIMESTAMP=1665112938057)

[面向时变不确定患者需求的急诊医疗运作资源管理研究](https://kreader.cnki.net/Kreader/CatalogViewPage.aspx?dbCode=cdmd&filename=1021674158.nh&tablename=CMFD202201&compose=&first=1&uid=WEEvREcwSlJHSldSdmVqelcxY2NSU0h4akd4WU11bXFSTTZTVDl0T2lzRT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4ggI8Fm4gTkoUKaID8j8gFw!!)

[Terminal appointment system design by non-stationary M(t)Ekc(t) queueing model and genetic algorithm](https://www.sciencedirect.com/science/article/pii/S0925527313003824)

[A variable neighborhood search heuristic for periodic routing problems](https://www.sciencedirect.com/science/article/pii/S0377221707011034)

[Physician Staffing for Emergency Departments with Time-Varying Demand](https://pubsonline.informs.org/doi/10.1287/ijoc.2017.0799)

[遗传算法与变邻域搜索混合模型在护士排班中的应用](https://www.cnki.com.cn/Article/CJFDTotal-BJSC201506012.htm)

