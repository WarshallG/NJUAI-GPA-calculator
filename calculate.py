import json


file_path = '保研学分计算课程.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

def greet():
    print('*' * 45)
    print("欢迎使用（极简）NJUAI保研学分绩计算程序！")
    print("请按照提示输入各门课程的分数。")
    print("输入-1表示未修读该课程。")
    print("您可以通过输入 q 来结束程序。")
    print('*' * 45)

def get_score(course):
    while True:
        try:
            user_input = input(f'{course}: ')
            if user_input.strip().lower() == 'q':
                print("程序已强制结束。")
                exit(0)
            score = eval(user_input)
            if not isinstance(score, (int, float)):
                raise TypeError("输入必须是数字。")
            if not (-1 <= score <= 100):
                raise ValueError("分数必须在-1到100之间，-1表示未修读该课程。")
            return score
        except KeyboardInterrupt:
            print("\n用户中断了输入，程序退出。")
            exit(0)
        except (SyntaxError, NameError, TypeError):
            print("输入格式错误，请输入一个数字，例如 85 或 -1。")
        except ValueError as e:
            print(f"输入值错误：{e}")

greet()

total_score = 0
total_credits = 0
record_dict = {}
for category, courses in data.items():
    print(f"\n课程类型: {category}")
    if category != '保研必修课':
        record_dict[category] = {}
        for course, credits in courses.items():
            score = get_score(course)
            if score == -1:
                continue
            if score < 60:
                print(f"Warning: {course} 的分数为 {score}，低于60分。这应该保不了研hhhh。")
                exit()
            total_score += score * credits / 20
            total_credits += credits
            record_dict[category][course] = {'分数': score, '学分': credits}
    else:
        score_list = []
        record_dict[category] = {}
        for course, credits in courses.items():
            score = get_score(course)
            if score == -1:
                continue
            if score < 60:
                print(f"Warning: {course} 的分数为 {score}，低于60分。这应该保不了研hhhh。")
                exit()
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
