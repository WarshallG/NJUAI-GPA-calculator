import json


file_path = '保研学分计算课程.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
print(data)


def get_score(course):
    while True:
        try:
            score = eval(input(f'{course}: '))
            if not (0 <= score <= 100):
                raise ValueError("分数必须在0到100之间")
            break
        except ValueError as e:
            print(f"输入错误: {e}，请重新输入。")
        except NameError:
            print("输入格式错误，请输入数字。")
total_score = 0
total_credits = 0
record_dict = {}
for category, courses in data.items():
    print(f"\n课程类型: {category}")
    if category != '保研必修课':
        record_dict[category] = {}
        for course, credits in courses.items():
            score = get_score(course)
            total_score += score * credits / 20
            total_credits += credits
            record_dict[category][course] = {'分数': score, '学分': credits}
    else:
        score_list = []
        record_dict[category] = {}
        for course, credits in courses.items():
            score = get_score(course)
            score_list.append((score, credits, course))
            record_dict[category][course] = {'分数': score, '学分': credits}
        score_list.sort(key=lambda x: x[0], reverse=True)
        print(f"保研必修课中，分数最高的六门课程为: {[course for _, _, course in score_list[:6]]}，分数分别为: {[score for score, _, _ in score_list[:6]]}\n")
        total_score += sum([score * credits / 20 for score, credits, _ in score_list[:6]])
        total_credits += sum([credits for _, credits, _ in score_list[:6]])

print('='* 40)
print(f"保研GPA: {total_score / total_credits:.6f}")
output_file = '保研学分计算记录.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(record_dict, f, ensure_ascii=False, indent=4)
print(f"记录已保存到 {output_file}")
print('='* 40)



        