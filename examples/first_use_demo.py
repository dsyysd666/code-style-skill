"""姓名问候接口模块。"""
# 按你的风格：完整语义名 + docstring + 具体异常捕获（standard / strict，C 工程型）
import logging

logger = logging.getLogger(__name__)


def build_greeting(person_name):
    """根据姓名生成问候语。

    Args:
        person_name: 用户姓名，不能为空字符串或 None。

    Returns:
        一句问候语。

    Raises:
        ValueError: 姓名为空时。
    """
    logger.info("收到姓名参数：%r", person_name)
    if person_name is None or person_name == "":
        logger.error("姓名为空：person_name=%r，期望非空字符串", person_name)
        raise ValueError("姓名不能为空，收到：%r" % person_name)
    greeting = "你好，" + person_name + "！"
    logger.info("生成问候语：%s", greeting)
    return greeting


if __name__ == "__main__":
    print(build_greeting("张三"))

# 排查地图：
# 1. 抛 ValueError → 看 build_greeting 的 person_name 空值校验
# 2. 问候语格式不对 → 看 greeting 字符串拼接那行

# 按你的风格自查：
# □ 变量名 —— 完整语义名
# □ docstring —— 每个函数都有
# □ 异常 —— 捕获具体类型、信息带当前值
# □ 打印 —— standard 强度（info/error 分级）
