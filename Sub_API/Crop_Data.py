from flask_restful import Resource
from flask import request
from tinydb import Query
from DB_TinyDB import *



# 农作物主要信息
class Crop_info(Resource):


    def post(self,prefix):


        if prefix == 'info':

            data = request.json

            aim = data['aim']   #目标表
            key = data['key']   #字段
            value = data['value']    #参数

            return

        if prefix == 'back':

            data = request.json

            aim = data['aim']   #目标表
            key = data['key']   #字段
            value = data['value']    #参数

            return

        if prefix == 'check':
            data = request.json

            aim = data['aim']  # 目标表
            check = data['check'] #校验类型
            key = data['key']  # 字段
            value = data['value']  # 参数

            return

        if prefix == 'config':
            data = request.json

            aim = data['aim']  # 目标表

            key = data['key']  # 字段
            value = data['value']  # 参数
            return

# 农作物校验
class Crop_check(Resource):


    def post(self,prefix):


        if prefix == 'F':

            data = request.json

            key = data['key']  # 字段
            value = data['value']  # 参数

            return

        if prefix == 'G':

            data = request.json

            key = data['key']  # 字段
            value = data['value']  # 参数

            return

        if prefix == 'M':

            data = request.json

            key = data['key']  # 字段
            value = data['value']  # 参数

            return

        if prefix == 'S':

            data = request.json

            key = data['key']  # 字段
            value = data['value']  # 参数

            return

        if prefix == 'Y':

            data = request.json

            key = data['key']  # 字段
            value = data['value']  # 参数

            return

# 农作物校验系数配置
class Crop_check_config(Resource):
    class Crop_check(Resource):

        def post(self, prefix):

            if prefix == 'F':
                data = request.json

                key = data['key']  # 字段
                value = data['value']  # 参数

                return

            if prefix == 'G':
                data = request.json

                key = data['key']  # 字段
                value = data['value']  # 参数

                return

            if prefix == 'M':
                data = request.json

                key = data['key']  # 字段
                value = data['value']  # 参数

                return

            if prefix == 'S':
                data = request.json

                key = data['key']  # 字段
                value = data['value']  # 参数

                return

            if prefix == 'Y':
                data = request.json

                key = data['key']  # 字段
                value = data['value']  # 参数

                return

# 农作物土壤反馈
class Crop_soil_back(Resource):


    def post(self,prefix):


        if prefix == 'F':

            data = request.json

            key = data['key']  # 字段
            value = data['value']  # 参数

            return

        if prefix == 'G':

            data = request.json

            key = data['key']  # 字段
            value = data['value']  # 参数

            return

        if prefix == 'M':

            data = request.json

            key = data['key']  # 字段
            value = data['value']  # 参数

            return

        if prefix == 'S':

            data = request.json

            key = data['key']  # 字段
            value = data['value']  # 参数

            return

        if prefix == 'Y':

            data = request.json

            key = data['key']  # 字段
            value = data['value']  # 参数

            return



# 新增农作物
class Crop_add(Resource):


    def post(self,prefix):


        if prefix == 'info':

            data = request.json

            aim = data['aim']   #目标表
            key = data['key']   #字段
            value = data['value']    #参数

            return

        if prefix == 'back':

            data = request.json

            aim = data['aim']   #目标表
            key = data['key']   #字段
            value = data['value']    #参数

            return

        if prefix == 'check':
            data = request.json

            aim = data['aim']  # 目标表
            check = data['check'] #校验类型
            key = data['key']  # 字段
            value = data['value']  # 参数

            return

        if prefix == 'config':
            data = request.json

            aim = data['aim']  # 目标表

            key = data['key']  # 字段
            value = data['value']  # 参数
            return

# 删除农作物
class Crop_del(Resource):


    def post(self,prefix):


        if prefix == 'info':

            data = request.json

            aim = data['aim']   #目标表
            key = data['key']   #字段
            value = data['value']    #参数

            return

        if prefix == 'back':

            data = request.json

            aim = data['aim']   #目标表
            key = data['key']   #字段
            value = data['value']    #参数

            return

        if prefix == 'check':
            data = request.json

            aim = data['aim']  # 目标表
            check = data['check'] #校验类型
            key = data['key']  # 字段
            value = data['value']  # 参数

            return

        if prefix == 'config':
            data = request.json

            aim = data['aim']  # 目标表

            key = data['key']  # 字段
            value = data['value']  # 参数
            return