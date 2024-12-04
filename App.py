from flask import Flask
from flask_restful import Api
# from flask_cors import CORS

from modbus_config import server

app = Flask(__name__)
api = Api(app)
# CORS(app, resources={r"/*": {"origins": "*"}})


from Function.Cultivate import Cultivate    #种植模拟
from Function.Weather import Weather   #气象模拟
from Function.Insect import Insect     #虫情模拟
from Function.Incident import Incident    #随机事件
from Function.Greenhouse import Greenhouse    #温室环境
from Function.Artificial import Artificial    #人工干预


from Sub_API.DB_Data import Basics_Field, Basics_Corp, Basics_Feiliao, Basics_Yaoji, Soil, Soil_info, Soil_Device_info, Soil_Start, Sundry  #更改基础信息 API
from Sub_API.Crop_Data import Crop_info, Crop_check, Crop_check_config, Crop_soil_back, Crop_add, Crop_del  #更改农作物信息 API



api.add_resource(Cultivate, '/cultivate/<prefix>')
api.add_resource(Weather, '/weather/<prefix>')
api.add_resource(Insect, '/insect/<prefix>')
api.add_resource(Incident, '/incident/<prefix>')
api.add_resource(Greenhouse, '/greenhouse/<prefix>')
api.add_resource(Artificial, '/artificial/<prefix>')


api.add_resource(Basics_Field, '/basics_field/<prefix>')
api.add_resource(Basics_Corp, '/basics_corp/<prefix>')
api.add_resource(Basics_Feiliao, '/basics_feiliao/<prefix>')
api.add_resource(Basics_Yaoji, '/basics_yaoji/<prefix>')
api.add_resource(Soil, '/soil/<prefix>')
api.add_resource(Soil_info, '/soil_info/<prefix>')
api.add_resource(Soil_Device_info, '/soil_device_info/<prefix>')
api.add_resource(Soil_Start, '/db_Soil_Start/<prefix>')
api.add_resource(Sundry, '/db_Sundry/<prefix>')


api.add_resource(Crop_info, '/crop_info/<prefix>')
api.add_resource(Crop_check, '/crop_check/<prefix>')
api.add_resource(Crop_check_config, '/crop_check_config/<prefix>')
api.add_resource(Crop_soil_back, '/crop_soil_back/<prefix>')
api.add_resource(Crop_add, '/crop_add/<prefix>')
api.add_resource(Crop_del, '/crop_del/<prefix>')




if __name__ == "__main__":
    app.run(host='0.0.0.0',port=6017)
