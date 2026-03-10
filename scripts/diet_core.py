# -*- coding: utf-8 -*-
"""
SlimGuard Diet Core - 饮食管理核心逻辑
参考 edict 架构：数据驱动，无废话输出
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

MEMORY_DIR = Path(__file__).parent / "memory"
DB_PATH = Path(__file__).parent / "tools" / "food_database.json"


def _ensure_memory_files():
    """初始化记忆文件"""
    files = {
        "user_profile.json": {
            "name": "用户", 
            "gender": "女", 
            "age": 30, 
            "height": 165, 
            "weight": 70,
            "goal_weight": 60
        },
        "goals.json": {
            "calorie_goal": 1800, 
            "protein_goal": 60, 
            "carbs_goal": 200, 
            "fat_goal": 60,
            "water_goal": 2000
        },
        "meals.json": {"records": []},
        "water.json": {"records": []},
        "exercise.json": {"records": []},
        "weight.json": {"records": []}
    }
    
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    for filename, default in files.items():
        filepath = MEMORY_DIR / filename
        if not filepath.exists():
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(default, f, ensure_ascii=False, indent=2)


def _search_food(food_name: str, amount: int = 1, unit: str = "个") -> Optional[Dict]:
    """查询食物营养数据"""
    if not DB_PATH.exists():
        return None
    
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)
    
    query = food_name.lower()
    for category, foods in db.items():
        for name, nutrition in foods.items():
            if query in name.lower() or name.lower() in query:
                cal = nutrition.get("calories", 0)
                
                # 份量转换
                unit_weights = {
                    "个": 50, "片": 30, "碗": 150, "杯": 200,
                    "份": 100, "块": 40, "袋": 30, "勺": 15
                }
                base_grams = unit_weights.get(unit, 100)
                grams = amount * base_grams
                
                return {
                    "name": name,
                    "amount": amount,
                    "unit": unit,
                    "grams": grams,
                    "calories": int(cal * grams / 100),
                    "protein": round(nutrition.get("protein", 0) * grams / 100, 1),
                    "carbs": round(nutrition.get("carbs", 0) * grams / 100, 1),
                    "fat": round(nutrition.get("fat", 0) * grams / 100, 1)
                }
    
    return None


def _parse_meal_message(message: str) -> List[Dict]:
    """解析饮食消息"""
    foods = []
    chinese_units = ["个", "片", "碗", "杯", "份", "块", "袋", "勺"]
    unit_pattern = "|".join(chinese_units)
    
    # 模式：数字 + 单位 + 食物名
    pattern = rf'(\d+)\s*({unit_pattern})\s*([^\s\d，,，和]+)'
    matches = re.findall(pattern, message)
    
    for match in matches:
        try:
            amount = int(match[0])
            unit = match[1]
            food_name = match[2].strip()
            if food_name and amount > 0:
                foods.append({"name": food_name, "amount": amount, "unit": unit})
        except:
            continue
    
    return foods


def record_meal(message: str) -> str:
    """记录饮食"""
    _ensure_memory_files()
    foods = _parse_meal_message(message)
    
    if not foods:
        return "❌ 格式：`吃了 2 片面包` 或 `早餐 1 个鸡蛋`"
    
    results = []
    total_cal = 0
    
    for food in foods:
        result = _search_food(food["name"], food["amount"], food["unit"])
        if result:
            results.append(result)
            total_cal += result["calories"]
            _save_record("meals.json", {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "foods": [result]})
    
    if results:
        response = ""
        for r in results:
            response += f"✅ {r['name']} x{r['amount']}{r['unit']} - {r['calories']}kcal\n"
        response += f"\n小计：{total_cal}kcal"
        return response
    
    return "❌ 未找到食物数据"


def query_calorie(food_name: str) -> str:
    """查询热量"""
    _ensure_memory_files()
    result = _search_food(food_name, 1, "")
    
    if result:
        return f"📊 {result['name']} (100g): {result['calories']}kcal | 蛋白质{result['protein']}g | 碳水{result['carbs']}g | 脂肪{result['fat']}g"
    
    return f"❌ 未找到 '{food_name}' 的数据"


def record_water(message: str) -> str:
    """记录饮水"""
    _ensure_memory_files()
    
    match = re.search(r'(\d+)\s*(?:ml|毫升)', message, re.IGNORECASE)
    if not match:
        match = re.search(r'(\d+)', message)
    
    if match:
        amount = int(match.group(1))
        _save_record("water.json", {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "amount": amount})
        
        today = datetime.now().strftime("%Y-%m-%d")
        total = _get_today_total("water.json", "amount", today)
        goal = _get_goal("water_goal", 2000)
        
        return f"💧 {total}ml / {goal}ml"
    
    return "❌ 格式：`喝了 300ml 水`"


def record_exercise(message: str) -> str:
    """记录运动"""
    _ensure_memory_files()
    
    calories_map = {
        "跑步": 10, "慢跑": 8, "快走": 5, "走路": 3,
        "游泳": 9, "骑车": 6, "瑜伽": 4, "健身": 7, "跳绳": 12
    }
    
    cal_per_min = 5
    for k, v in calories_map.items():
        if k in message:
            cal_per_min = v
            break
    
    match = re.search(r'(\d+)\s*(?:分钟|分)', message)
    if match:
        minutes = int(match.group(1))
        calories = minutes * cal_per_min
        _save_record("exercise.json", {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "activity": message[:20],
            "minutes": minutes,
            "calories": calories
        })
        return f"🏃 {minutes}分钟 - {calories}kcal"
    
    return "❌ 格式：`跑步 30 分钟`"


def record_weight(message: str) -> str:
    """记录体重"""
    _ensure_memory_files()
    
    match = re.search(r'(\d+\.?\d*)\s*(?:公斤|kg)', message, re.IGNORECASE)
    if match:
        weight = float(match.group(1))
        _save_record("weight.json", {"date": datetime.now().strftime("%Y-%m-%d"), "weight": weight})
        
        goal = _get_goal("goal_weight", 60)
        return f"⚖️ {weight}kg (目标：{goal}kg)"
    
    return "❌ 格式：`体重 65kg`"


def generate_report() -> str:
    """生成每日报告"""
    _ensure_memory_files()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 获取今日数据
    meals = _get_today_records("meals.json", today)
    water = _get_today_total("water.json", "amount", today)
    exercise = _get_today_total("exercise.json", "calories", today)
    
    # 计算营养
    total_cal = total_protein = total_carbs = total_fat = 0
    meal_count = len(meals)
    
    for meal in meals:
        for food in meal.get("foods", []):
            total_cal += food.get("calories", 0)
            total_protein += food.get("protein", 0)
            total_carbs += food.get("carbs", 0)
            total_fat += food.get("fat", 0)
    
    # 获取目标
    calorie_goal = _get_goal("calorie_goal", 1800)
    water_goal = _get_goal("water_goal", 2000)
    
    # 生成报告
    response = f"📊 今日饮食报告 - {today}\n"
    response += "=" * 30 + "\n"
    response += f"🍽️ {meal_count}餐 | 总热量：{total_cal}kcal\n"
    response += f"   蛋白质：{int(total_protein)}g | 碳水：{int(total_carbs)}g | 脂肪：{int(total_fat)}g\n\n"
    response += f"💧 饮水：{water}ml / {water_goal}ml\n"
    response += f"🏃 运动：{exercise}kcal\n\n"
    
    balance = calorie_goal - total_cal + exercise
    response += f"📈 热量余额：{balance}kcal"
    
    return response


def _save_record(filename: str, data: Dict):
    """保存记录"""
    filepath = MEMORY_DIR / filename
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            records = json.load(f)
        records["records"].append(data)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    except:
        pass


def _get_today_records(filename: str, date: str) -> List[Dict]:
    """获取今日记录"""
    filepath = MEMORY_DIR / filename
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            records = json.load(f)
        return [r for r in records.get("records", []) if r.get("time", "").startswith(date)]
    except:
        return []


def _get_today_total(filename: str, field: str, date: str) -> int:
    """获取今日总计"""
    records = _get_today_records(filename, date)
    return sum(r.get(field, 0) for r in records)


def _get_goal(key: str, default: int) -> int:
    """获取目标值"""
    try:
        with open(MEMORY_DIR / "goals.json", "r", encoding="utf-8") as f:
            goals = json.load(f)
        return goals.get(key, default)
    except:
        return default


def handle_message(message: str) -> str:
    """主入口 - 自动识别意图"""
    msg_lower = message.lower()
    
    # 意图识别
    if any(k in message for k in ["吃了", "早餐", "午餐", "晚餐"]):
        return record_meal(message)
    elif any(k in message for k in ["热量", "卡路里"]):
        food = re.sub(r'.*?(热量 | 卡路里).*', '', message).strip()
        return query_calorie(food) if food else "❌ 请指定食物"
    elif any(k in msg_lower for k in ["喝水", "ml", "毫升"]):
        return record_water(message)
    elif any(k in message for k in ["运动", "跑步", "分钟"]):
        return record_exercise(message)
    elif any(k in message for k in ["体重", "公斤", "kg"]):
        return record_weight(message)
    elif any(k in message for k in ["报告", "总结", "统计"]):
        return generate_report()
    else:
        return "你好，我是 SlimGuard 🥗\n\n示例：\n• \"早餐吃了 2 片面包\"\n• \"米饭热量多少\"\n• \"今天的报告\""


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(handle_message(" ".join(sys.argv[1:])))
    else:
        print("SlimGuard Diet Core v2.0")
        print("Usage: python diet_core.py \"吃了 1 个鸡蛋\"")
