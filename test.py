from observer import observer


def func_x(**kwargs):
    print(kwargs)


def func_y(**kwargs):
    print(kwargs)
    # return {"inject":{"new_var":1000,
    #                   "dx": 67}}


# @observer(mappings={"a":{"on-create":func_x,
#                                 "on-specific":{"target_value":6,
#                                                "function":func_y,
#                                                "update_value":3000}},
#                            "wx":{"on-change":func_x}})
# def test_prgm(a=0,b=0):
#     a = a
#     b = b
#     for i in range(3):
#         a += i
#         b = i
#
#     del(a)
#     a = 2
#     a = 2
#     a = 6
#     wx = (new_var * a) / 5
#     wx = wx - a

@observer(mappings={"a": {"on-create": func_x,
                          "on-specific": {"target_value": "hello",
                                          "function": func_y,
                                          "update_value": 3000},
                          "on-range": {"sequences": ["var->b"],
                                       "operation": "in",
                                       "target_value": 3,
                                       "function": func_x}}})
def test_prgm(a=None, b=None):
    b = ["hello", "a", "g", 3, 6, 67]
    a = "he"
    a += "ll"
    a += "o"
    print(a)


test_prgm(0, 3)

# class A:
#
#     @observer(mappings={"a": {"on-change": func_x,
#                                      "on-delete":func_y}})
#     def fg(self):
#         a=1
#         a=1
#         a=1
#         a=2
#         del(a)
#
#
# G = A()
# G.fg()


# from time import sleep
#
# @observer(mappings={"a":{"on-add":func_x,
#                                 "on-change":func_y}})
# def fn():
#     a = 3
#     i = 1
#     while(i):
#         i += 1
#         if i > 999:
#             break
#         else:
#             sleep(0.01)
#         if i%9 == 0:
#             a += 3
#
# fn()
