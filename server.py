#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask,jsonify,request,abort,Response
from time import strftime,localtime
from uuid import uuid4
import json

# 实例化http服务
app = Flask(__name__)

# 业务逻辑
class Task(object):
    def __init__(self,content):
        self.id = str(uuid4())
        self.content = content
        self.created_at = strftime("%y-%m-%d:%H:%M:%S")
        self.is_finished = False
        self.finished_at = None

    def finish(self):
        self.is_finished = True
        self.finished_at = strftime("%y-%m-%d:%H:%M:%S")

    def json(self):
        return {
            'id':self.id,
            'content':self.content,
            'created_at':self.created_at,
            'is_finished':self.is_finished,
            'finished_at':self.finished_at,
        }

# 模拟数据库接口
tasks_db = {'0':Task('test')}
get_task = tasks_db.get

# 接收请求和做出响应
# 展示
@app.route('/task')
def show():
    return jsonify(data=[task.json() for task in tasks_db.values()])

# 添加
@app.route('/task',methods=['POST'])
def add():
    content = request.form.get('content',None)
    if not content:
        abort(400)
    task = Task(content)
    tasks_db[task.id] = task
    return Response()

# 修改
@app.route('/task/<tid>/finish',methods=['PUT'])
def finish(tid):
    task = get_task(tid)
    if task:
        task.finish()
        tasks_db[tid] = task
        return Response()
    abort(404)

# 删除
@app.route('/task/<tid>',methods=['DELETE'])
def delete(tid):
    task = get_task(tid)
    if task:
        tasks_db.pop(tid)
        return Response()
    abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)

