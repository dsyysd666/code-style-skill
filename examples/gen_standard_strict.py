"""筛选成年人姓名并按年龄排序（standard 打印 + strict 语法）。"""
# 按你的风格：全名变量 + 每块一行注释 + 函数入口打印参数（standard / strict）


def filter_adults(people):
    """筛选出成年人。people 是 (姓名, 年龄) 元组列表。"""
    print("[入口] filter_adults 参数 people =", people)
    adult_list = []
    for person in people:
        name = person[0]
        age = person[1]
        if age >= 18:
            adult_list = adult_list + [person]
    print("[关键] 筛选结果 adult_list =", adult_list)
    return adult_list


def sort_by_age(adult_list):
    """按年龄升序排序，不使用 lambda 或推导式。"""
    sorted_list = adult_list + []
    index = 0
    while index < len(sorted_list):
        inner_index = index + 1
        while inner_index < len(sorted_list):
            first_age = sorted_list[index][1]
            second_age = sorted_list[inner_index][1]
            if second_age < first_age:
                temp = sorted_list[index]
                sorted_list[index] = sorted_list[inner_index]
                sorted_list[inner_index] = temp
            inner_index = inner_index + 1
        index = index + 1
    return sorted_list


# 第 1 步：准备数据
people = [("张三", 17), ("李四", 25), ("王五", 20), ("赵六", 16)]
adult_list = filter_adults(people)
sorted_list = sort_by_age(adult_list)
name_list = []
for person in sorted_list:
    name_list = name_list + [person[0]]
print("[完成] 成年人姓名（按年龄排序）=", name_list)

# 排查地图：
# 1. 人数不对 → 看 filter_adults 的 if age >= 18
# 2. 排序不对 → 看 sort_by_age 的两层 while 交换
# 3. 取值报错 → 看 person[0]/person[1] 的元组下标

# 按你的风格自查：
# □ 变量名 —— 全部完整单词
# □ 缩进 —— 4 空格
# □ 报错 —— 能看出是哪一步
# □ 打印 —— 符合 standard 强度（入口+关键，非每步）
