# sort_dict = {1: "_salary_to_filter", 2: "experience", 3: "has_test", 4: "accept_temporary"}
# lst = set([1, 4])
# acc = list(sort_dict.get(i) for i in lst)
# for i in acc:
#     print(type(i))
# #
# import requests
# p = {
#     "text": "python",
#     "page": 0,
#     "per_page": 5,
#     'area': 113
# }
# param_list = [23]
# sort_dict = {2: "has_test", 3: "accept_temporary", 4: "date_published"}
# attr = list(sort_dict.get(i) for i in param_list)
# attr = [i for i in attr if i is not None]
# print(attr)
# print(None in attr)
d = {"a": 1, "b": 10, "c": 1010, "d": 9000}
def max_values(d: dict) -> tuple:
    sorted_list = sorted(d.items(), key=lambda item: item[1], reverse=True)
    return (sorted_list[0][1], sorted_list[1][1])

print(max_values(d))