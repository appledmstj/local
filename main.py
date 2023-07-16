import tkinter as tk
from tkinter import messagebox
import random
import csv
import numpy as np


#   전역변수
indiv_preference = []           #   개인 1-17지망 저장, 행번호+1이 교번, 각 열이 지망 의미 (1행 1열= 교번2의 2지망)
region_name_to_key = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6,
                      'g':7, 'h':8, 'i':9, 'j':10, 'k':11, 'l':12,
                      'm':13, 'n':14, 'o':15, 'p':16, 'q':17}              #   각 지역에 키 부여
region_key_to_name = {1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',
                      7:'g',8:'h',9:'i',10:'j',11:'k',12:'l',
                      13:'m',14:'n',15:'o',16:'p',17:"q"}
region_name_list = ['a', 'b','c','d','e','f','g','h','i','j','k','l','m','o','p','q']
capacity = [40,10,30,20,40,10,10,21,19,28,15,12,10,10,15,5,5]                   #   각 지역 정원, 인덱스+1이 해당 지역의 키 (인덱스3 = 지역번호4 = D지역)
capacity_update = capacity      #   각 지역 정원 업데이트 값
indiv_region = [None] * 300               #   개인 확정 지역 저장, 초기값 없음
unconfirmed_indiv = list(range(1, 301))         #   아직 확정되지 않은 교번 저장. 초기값=전원
unconfirmed_region = list(range(1, 18))         #   정원 남아있는 지역 키로 저장. 초기값=전지역
priority = {}                   #   우선배치인원 저장용 변수
region_final = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]             # 각 지역의 확정 인원 교번 저장용 리스트, region_final[i]의 리스트가 지역번호 i+1의 명단



class LotteryDataProcessor:     # 전처리전용, 파일데이터 다운로드
    def __init__(self, filename):
        self.filename = filename
        self.data_list = []
        self.column_counts = {}

    def load_data_from_csv(self):       # 개인 지망 다운로드 후 indiv_preference 저장
        with open(self.filename, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for row in csv_reader:
                data_row = [char for char in row[1:]]
                self.data_list.append(data_row)
            return self.data_list

    def count_data_by_column(self):
        for sublist in self.data_list:
            for i, data in enumerate(sublist):
                if i not in self.column_counts:
                    self.column_counts[i] = {}

                if data in self.column_counts[i]:
                    self.column_counts[i][data] += 1
                else:
                    self.column_counts[i][data] = 1

    def print_column_counts(self):
        for col, counts in self.column_counts.items():
            print(f"열 {col + 1}:")
            for data, count in counts.items():
                print(f"{data}: {count}개")
            print()
import random

class PriorityDataProcessor:     # 전처리전용, 우선순위 다운로드 후 priority에 저장
    def __init__(self, filename):
        self.filename = filename
        self.data_dict = {}

    def load_priority_from_csv(self):
        with open(self.filename, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for row in csv_reader:
                key = int(row[0])
                value = int(row[1])
                self.data_dict[key] = value
            return self.data_dict




def draw_lottery(data_list, target):        #data_list 에서 target을 지망한 사람 중 추첨 진행해 당첨인원 반환
    #print("hi", data_list[6])
    name = region_key_to_name[target+1]
    dellist = []
    for i in range(len(data_list)):
        #print("i", i, data_list[i]+1)
        if (data_list[i]+1) in unconfirmed_indiv:
            continue
        else:
            #rint("i", i, data_list[i] + 1)
            dellist.append(data_list[i])
    #print("drawlist", data_list)

    for j in range(len(dellist)):
        #print(dellist[j])
        data_list.remove(dellist[j])

    num_a = len(data_list)
    #print(num_a, capacity_update[target])
    if num_a <= capacity_update[target]:
        #print("a")
        selected_indices = data_list
    else:
        selected_indices = random.sample(data_list, capacity_update[target])

    #print("draw", selected_indices)
    return selected_indices

def lottery_update(selected_list, regionkey):   #당첨자 업데이트 함수. 입력값: 당첨자리스트, 지역번호키
    global indiv_region
    global region_final
    global unconfirmed_indiv
    global capacity_update
    #print(selected_list)
    for i in range(len(selected_list)):
        #print("i", selected_list[i])
        indiv_region[selected_list[i]] = regionkey      #   확정자 indiv_region에 업데이트
        #print("gg",unconfirmed_indiv[selected_list[i]])
        unconfirmed_indiv.remove(selected_list[i]+1)      #   unconfirmed에서 확정자 제거
        selected_list[i] = selected_list[i] +1
    region_final[regionkey-1].extend(selected_list)   # 지역확정리스트에 확정자 교번 추가. regionkey를 인덱스로 쓰려면 -1
    #print(region_final[regionkey-1])
    capacity_update[regionkey-1] = capacity_update[regionkey-1] - len(selected_list)    #   당첨수만큼 정원축소
    if capacity_update[regionkey-1] <= 0 :
        unconfirmed_region.remove(regionkey)

def temp_display(selected, i, j):
    print(i+1, "지망", region_key_to_name[j+1], "지역" )
    if i == 0:
        print(region_final[j])
    #elif i+1 not in unconfirmed_region:
    #    print("done")
    else:
        print(selected)


def priority_confirm():
    global priority
    #print(priority)
    for key, value in priority.items():
        templist = [key-1]
        #print(templist)
        lottery_update(templist, value)


def main():
    global indiv_preference
    global priority
    global unconfirmed_region

    lottery_data_processor = LotteryDataProcessor('lottery.csv')
    priority_data_processor = PriorityDataProcessor('priority.csv')

    indiv_preference = lottery_data_processor.load_data_from_csv()      #개인 지망 변수 저장
    priority = priority_data_processor.load_priority_from_csv()         #우선순위 변수 저장
    np_preference = np.array(indiv_preference)




    priority_confirm()      #   배려대상자 확정 및 정원 업데이트
    for i in range(0, 17):
        this_preferenece = np_preference[:, i]        #   i지망 저장
        this_regionkey = [None] * 300
        for key in range(len(this_preferenece)):
            #print("kk",this_preferenece[key], region_name_to_key[this_preferenece[key]])
            this_regionkey[key] = region_name_to_key[this_preferenece[key]]
        #print("thisregionkey", this_regionkey)
        for j in range(0, 17):
            if j+1 in this_regionkey and j+1 in unconfirmed_region:

                region_index = []
                for k in range(len(this_regionkey)):
                    if this_regionkey[k] == j+1:
                        region_index.append(k)
                #print(i,j)
                #print("rein", region_index)
                #############   버튼 ########
                selected = draw_lottery(region_index, j)
                #print("i,j: ", i,j, selected)
                lottery_update(selected, j+1)
                ###### 당첨자 디스플레이 #######
                temp_display(selected, i, j)
    for key in range(0, 17):
        print(region_key_to_name[key+1], "final list:", region_final[key])

    filen = 'final_list.csv'
    with open(filen, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['final_list'])
        for row in region_final:
            writer.writerow(row)

if __name__ == '__main__':
    main()

"""
# 데이터 리스트 출력
for data in data_list:
    print(data)
"""





"""
def draw_numbers():
    numbers = list(range(1, 18))
    random.shuffle(numbers)
    selected_numbers = numbers[:3]
    messagebox.showinfo("추첨 결과", f"추첨된 번호: {selected_numbers}")

# Tkinter 윈도우 생성
window = tk.Tk()
window.title("추첨 프로그램")

# 버튼 생성
button = tk.Button(window, text="추첨하기", command=draw_numbers)
button.pack(padx=50, pady=30
            )

# 윈도우 실행
window.mainloop()

"""