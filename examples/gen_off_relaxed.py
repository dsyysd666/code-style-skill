"""筛选成年人姓名并按年龄排序（off 打印 + relaxed 语法）。"""
# 按你的风格：全名变量 + 每块一行注释（off / relaxed，硬规矩除外）


def filter_adults(people):
    """筛选出成年人。people 是 (姓名, 年龄) 元组列表。"""
    adult_list = [person for person in people if person[1] >= 18]
    return adult_list


def sort_by_age(adult_list):
    """按年龄升序排序。"""
    sorted_list = sorted(adult_list, key=lambda person: person[1])
    return sorted_list


# 第 1 步：准备数据
people = [("张三", 17), ("李四", 25), ("王五", 20), ("赵六", 16)]
adult_list = filter_adults(people)
sorted_list = sort_by_age(adult_list)
name_list = [person[0] for person in sorted_list]
print("成年人姓名（按年龄排序）=", name_list)

# 排查地图：
# 1. 人数不对 → 看 filter_adults 的推导式条件 person[1] >= 18
# 2. 排序不对 → 看 sorted 的 key=lambda person: person[1]

# 按你的风格自查：
# □ 变量名 —— 全部完整单词
# □ 缩进 —— 4 空格
# □ 报错 —— 能看出是哪一步
# □ 打印 —— 符合 off 强度（只在结果处）
