import numpy as np

cnts = np.zeros(3, np.int)
plist = [1 / 6, 1 / 3, 0.5]
names = ["小明", "小红", "小芳", "小李", "小花", "大壮", "大牛", "大猪", "大虎", "大葱"]
info = ""

first_names = []
second_names = []
third_names = []
cnts[0] = 1
cnts[1] = 2
cnts[2] = 3


def lotteryAgain():
    global cnts
    for i in range(5):
        global info, plist, first_names, second_names, third_names, names
        if (len(names) == 0 or cnts.sum(axis=0) == 0):
            print("已经全部抽完")
            break
        # 随机抽取是几等奖
        step = np.random.choice(3, 1, p=plist)[0]
        while cnts[step] == 0:
            step = np.random.choice(3, 1, p=plist)[0]
        print("step:%d" % (step))

        cnts[step] = cnts[step] - 1
        if step == 0:
            first_names.append(names[0])
        elif (step == 1):
            second_names.append(names[0])
        else:
            third_names.append(names[0])
        del names[0]
    print(first_names)
    print(second_names)
    print(third_names)
    print(names)
    print(cnts)
    #  info = "names:" + ",".join(names) + "first:" + ",".join(first_names) + "second:" + ",".join(second_names) + "third:" + ",".join(third_names)


lotteryAgain()
lotteryAgain()
