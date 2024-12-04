from tinydb import TinyDB


#A区域-缓存
db_A = TinyDB('DB/db_A.json')
#B区域-缓存
db_B = TinyDB('DB/db_B.json')
#C区域-缓存
db_C = TinyDB('DB/db_C.json')


#农产品
db_Crop = TinyDB('DB/db_Crop.json')
#肥料
db_Feiliao = TinyDB('DB/db_Feiliao.json')
#药剂
db_Yaoji = TinyDB('DB/db_Yaoji.json')
#药剂功能
db_Yaoji_Effect = TinyDB('DB/db_Yaoji_Effect.json')


#全国地区
db_Soil = TinyDB('DB/db_Soil.json')
#土壤开始各项参数（A、B、C）
db_Soil_Start = TinyDB('DB/db_Soil_Start.json')
#土壤相关设备
db_Soil_Device_info = TinyDB('DB/db_Soil_Device_info.json')
db_Lora_Device_info = TinyDB('DB/db_Lora_Device_info.json')

#华中地区-土壤肥力区间
db_Soil_Central_China = TinyDB('DB/db_Soil_Central_China.json')
#东北地区-土壤肥力区间
db_Soil_Northeast_China = TinyDB('DB/db_Soil_Northeast_China.json')
#华北地区-土壤肥力区间
db_Soil_North_China = TinyDB('DB/db_Soil_North_China.json')
#华南地区-土壤肥力区间
db_Soil_South_China = TinyDB('DB/db_Soil_South_China.json')
#西北地区-土壤肥力区间
db_Soil_Northwest_China = TinyDB('DB/db_Soil_Northwest_China.json')
#西南地区-土壤肥力区间
db_Soil_Southwest_China = TinyDB('DB/db_Soil_Southwest_China.json')


#虫情数据表
db_Insect_info = TinyDB('DB/db_Insect_info.json')
db_Insect_Check = TinyDB('DB/db_Insect_Check.json')

#气象数据表
db_Weather_info = TinyDB('DB/db_Weather_info.json')
db_Weather_Check = TinyDB('DB/db_Weather_Check.json')

#随机事件数据表
db_Incident_info = TinyDB('DB/db_Incident_info.json')
db_Incident_Check = TinyDB('DB/db_Incident_Check.json')

#温室环境


#杂项
db_Sundry = TinyDB('DB/db_Sundry.json')
#解决方案
db_Solution = TinyDB('DB/db_Solution.json')

# Xiaomai_Info = TinyDB('Crop_DB/Xiaomai/Xiaomai_Info.json')  #小麦信息
# Xiaomai_Soil_Back = TinyDB('Crop_DB/Xiaomai/Xiaomai_Soil_Back.json')  #小麦土壤反馈
# Xiaomai_Check_Config = TinyDB('Crop_DB/Xiaomai/Xiaomai_Check_Config.json')  #小麦校验配置
# Xiaomai_Check_F = TinyDB('Crop_DB/Xiaomai/Xiaomai_Check_F.json')  #小麦肥料校验
# Xiaomai_Check_S = TinyDB('Crop_DB/Xiaomai/Xiaomai_Check_S.json')  #小麦补水校验
# Xiaomai_Check_G = TinyDB('Crop_DB/Xiaomai/Xiaomai_Check_G.json')  #小麦调节剂校验
# Xiaomai_Check_Y = TinyDB('Crop_DB/Xiaomai/Xiaomai_Check_Y.json')  #小麦农药校验
# Xiaomai_Check_M = TinyDB('Crop_DB/Xiaomai/Xiaomai_Check_M.json')  #小麦微量肥料校验
#
#
# Yumi_Info = TinyDB('Crop_DB/Yumi/Yumi_Info.json')  #玉米信息
# Yumi_Soil_Back = TinyDB('Crop_DB/Yumi/Yumi_Soil_Back.json')
# Yumi_Check_Config = TinyDB('Crop_DB/Yumi/Yumi_Check_Config.json')
# Yumi_Check_F = TinyDB('Crop_DB/Yumi/Yumi_Check_F.json')
# Yumi_Check_S = TinyDB('Crop_DB/Yumi/Yumi_Check_S.json')
# Yumi_Check_G = TinyDB('Crop_DB/Yumi/Yumi_Check_G.json')
# Yumi_Check_Y = TinyDB('Crop_DB/Yumi/Yumi_Check_Y.json')
# Yumi_Check_M = TinyDB('Crop_DB/Yumi/Yumi_Check_M.json')
#
#
# Dadou_Info = TinyDB('Crop_DB/Dadou/Dadou_Info.json')
# Dadou_Soil_Back = TinyDB('Crop_DB/Dadou/Dadou_Soil_Back.json')
# Dadou_Check_Config = TinyDB('Crop_DB/Dadou/Dadou_Check_Config.json')
# Dadou_Check_F = TinyDB('Crop_DB/Dadou/Dadou_Check_F.json')
# Dadou_Check_S = TinyDB('Crop_DB/Dadou/Dadou_Check_S.json')
# Dadou_Check_G = TinyDB('Crop_DB/Dadou/Dadou_Check_G.json')
# Dadou_Check_Y = TinyDB('Crop_DB/Dadou/Dadou_Check_Y.json')
# Dadou_Check_M = TinyDB('Crop_DB/Dadou/Dadou_Check_M.json')

