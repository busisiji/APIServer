from tinydb import Query
from DB_TinyDB import *
#
Q = Query()
# # Nzw = 'CR01'
# # Check_config = db_Crop.search(Q.ID == Nzw)[0]['Check_config']
# # print(Check_config)
# #
# #
# #
# # Check_Data = (TinyDB(f'Crop_DB/{Check_config}.json').search(Q.ID == 'Check_F'))[0]
# # print(Check_Data)
#
#
# i = 'J04'
# Check_G = 'CK05'
#
#
# Check_G_data = Xiaomai_Check_G.search((Q.ID == i) & (Q.Type == Check_G))
# print(Check_G_data)
#
# # Datas = db_C.all()[0]
# # # Plot_map = db_C[f'{Zzqy}']
# # # print('对应共享数据表：', Plot_map)
# # nzw = Datas['Nzw'] # 当前农作物
# # print('当前农作物: ', nzw)
# # Key = 'CC'
# # Value= 333
# #
# # DB = TinyDB(f'DB/db_C.json')
# # print(DB_Aim.get(doc_ids=[0]))
#
# # db_Yaoji_Effect_Lsatone = TinyDB('DB/db_Yaoji_Effect.json').all()[-1:][0]
# # ID = 'E' + str(int((db_Yaoji_Effect_Lsatone['ID'])[1:3]) + 1)
# # Effect = int(db_Yaoji_Effect_Lsatone['Effect']) + 1
#
# # DB = TinyDB(f'DB/db_Soil_Central_China.json')
# # Names = [i['Name'] for i in DB.search(Q.Name.exists())]
# #
# # print(Names)
# #
# # print(DB.search(Q.Name == '潮土'))
#
#
# #     if Key in doc:
# #         del doc[Key]
# #     return doc
# #
# # def update_key(doc):
# #     doc[Key] = Key  # 更新email字段的值
# #     return doc
#
#
# # DB_Aim.update({Key: 222}, doc_ids=[1])
# # DB.remove((Q.Nzw == 'CR01') & (Q.Qy == 'C3'))
# # DB.update({Key: Value}, ((Q.Nzw  == 'CR01') & (Q.Qy == 'C3')))
# # DB_Aim.update(remove_key)
#
# # import requests
# #
# # # 基础URL
# # base_url = 'http://127.0.0.1:6017/basics_feiliao/feiliao'
# #
# # # 自定义查询参数
# # params = {
# #     'Name': '尿素',
# #     'Key': 'all'
# # }
# #
# # # 发送GET请求，并将params作为查询参数传递
# # response = requests.get(base_url, params=params)
# #
# # # 检查请求是否成功
# # if response.status_code == 200:
# #     # 打印响应内容
# #     print(response.text)
# # else:
# #     # 打印错误信息
# #     print(f'请求失败，状态码：{response.status_code}')
#
# # 如果响应是JSON格式，你可以这样解析它
# # try:
# #     data = response.json()
# #     print(data)
# # except json.JSONDecodeError:
# #     print("响应内容不是有效的JSON格式")
#
# # A = ['小麦', '玉米', '大豆', '水稻', '棉花', '草莓', '黄瓜', '番茄', '辣椒', '西瓜', '菠菜', '茄子']
# # A.append()
#
#
#
# # B = '西'
# #
# # if B in A:
# #     print(True)
# # else:
# #     print(False)
#
# # Check_Y_data = Xiaomai_Check_Y.search(Q.Type == 'CK04')
# # print(Check_Y_data)
# #
# # # for i in Check_Y_data:
# # #     print(i['ID'])
# # #     if i['ID'] == 'J01':
# # #         print(True)
# # #     else:
# # #         print(False)
# #
# # #
# # A = {'a': 10, 'b': 2}
# #
# # for i in A:
# #     print(i)
#
# #
# # print(ny_list)
# # Check_Y_data = ['J01', 'J02', 'J03']  # 示例列表
#
# # 使用 any() 函数检查列表中是否包含 'J01'
# # if any(i == 'J01' for i in Check_Y_data):
# #     print(True)
# # else:
# #     print(False)
#
# # A = 'J01'
# #
# # if 'J01' in ny_list:
# #     print(True)
# # else:
# #     print(False)
# # print(Check_Y_data.get('ID', None))
#
# # print(db_C.all()[0]['feedback_N'])
#
# # Szjd = 'ST02'
# # feiliao_type = 'N'
# #
# # feiliao_liang = float(Xiaomai_Info.search(Q.ID == Szjd)[0].get(feiliao_type, '0'))  # 当前阶段肥料量占比
# # print('当前阶段肥料量占比: ', feiliao_liang)

if '干旱' == '旱':
    print(True)


# def find_differences(list1, list2):
#     set1 = set(list1)
#     set2 = set(list2)
#
#     # 找出在list1但不在list2中的元素
#     diff1 = set1 - set2
#     return diff1
#
#
# # 示例
# list1 = []
# list2 = []
#
# diff1 = find_differences(list1, list2)
# print((diff1))
# # print("在list2但不在list1中的元素:", diff2)


# def contains_all_elements(arr1, arr2):
#     set1 = set(arr1)
#     set2 = set(arr2)
#     return set1.issubset(set2)
#
#
# # 示例
# arr1 = [1, 2, 3, 6]
# arr2 = [1, 2, 3, 4, 5]
# print(contains_all_elements(arr1, arr2))  # 输出: True


# G_Ftion_list = Xiaomai_Check_G.search(Q.ID == 'CK03')[0]['Ftion']
# print(G_Ftion_list)
