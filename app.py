# -*- coding: utf-8 -*-
import os
import sys
import json
import requests
import re
import time
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, jsonify
import random
import urllib

app = Flask(__name__, static_url_path='')

@app.route('/tracking_kerry', methods=['GET'])
def tracking_kerry():
    data = request.args.get('tracking_id')
    status = get_tracking_kerry(data)
    print status
    if status == None or status == 1:
        message = {
            "messages": [
                {"text": u"เอ หาไม่เจอเลย บอกผิดรึเปล่าน้า?"}
            ]
        }
    elif status == 0:
        message = {
            "messages": [
                {"text": u"พัสดุอยู่ในสถานะ Pending นะ ตอนนี้ Tracky กำลังติดต่อให้อยู่ รออีกสักพัก กลับมาเช็คใหม่นะครับ"}
            ]
        }
    else:
        if status['tag'] == "Delivered":
          message = {
              "messages": [
                  {"text": u"พัสดุถึงที่หมายแล้ว"},
                  {"text": status['place']},
                  {"text": u"เวลา: " + status['date'] + " " + status['time']}
              ]
          }
        else:
          message = {
              "messages": [
                  {"text": u"สถานะ: " + status['tag'] + " (" + status['tag_th'] + ")" },
                  {"text": status['place']},
                  {"text": u"เวลา: " + status['date'] + " " + status['time']}
            ]
          }
    print message
    return jsonify(message)

def get_tracking_kerry(tracking_id):
    url = "https://track.aftership.com/kerry-logistics/"+tracking_id
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    recent = soup.find_all('li',{'class':'checkpoint'})
    if len(recent) <= 0:
        status_text = soup.find('p',{'id':'status-text'})
        print status_text
        if status_text:
            return 0
        return None
    recent = recent[0]
    place = recent.find('div',{'class':'checkpoint__content'}).find('div',{'class':'hint'}).get_text()
    datetime = recent.find('div',{'class':'checkpoint__time'})
    date = datetime.find('strong').get_text()
    tag = soup.find('p',{'class':'tag'}).get_text()
    time = datetime.find('div',{'class':'hint'}).get_text()
    if tag == "In Transit":
        tag_th = u"กำลังส่ง"
    elif tag == "Delivered":
        tag_th = u"ถึงที่หมาย"
    elif tag == "Out For Delivery":
        tag_th = u"กำลังจำหน่าย ตามบ้าน"
    time = datetime.find('div',{'class':'hint'}).get_text()
    return {"place": place, "date":date, "time":time, "tag":tag, "tag_th" :tag_th}

@app.route('/tracking', methods=['GET'])
def tracking():
    data = request.args.get('tracking_id')
    status = get_tracking(data)
    print status
    if status == None or status == 1:
        message = {
            "messages": [
                {"text": u"เอ หาไม่เจอเลย บอกผิดรึเปล่าน้า?"}
            ]
        }
    elif status == 0:
        message = {
            "messages": [
                {"text": u"พัสดุอยู่ในสถานะ Pending นะ ตอนนี้ Tracky กำลังติดต่อให้อยู่ รออีกสักพัก กลับมาเช็คใหม่นะครับ"}
            ]
        }
    else:
        if status['tag'] == "Delivered":
          message = {
              "messages": [
                  {"text": u"พัสดุถึงที่หมายแล้ว"},
                  {"text": status['place']},
                  {"text": u"เวลา: " + status['date'] + " " + status['time']}
              ]
          }
        else:
          message = {
              "messages": [
                  {"text": u"สถานะ: " + status['tag'] + " (" + status['tag_th'] + ")" },
                  {"text": status['place']},
                  {"text": u"เวลา: " + status['date'] + " " + status['time']}
              ]
          }
    print message
    return jsonify(message)

def get_tracking(tracking_id):
    url = "https://track.aftership.com/thailand-post/"+tracking_id
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    recent = soup.find_all('li',{'class':'checkpoint'})
    if len(recent) <= 0:
        status_text = soup.find('p',{'id':'status-text'})
        print status_text
        if status_text:
            return 0
        return None
    recent = recent[0]
    place = recent.find('div',{'class':'checkpoint__content'}).find('div',{'class':'hint'}).get_text()
    datetime = recent.find('div',{'class':'checkpoint__time'})
    date = datetime.find('strong').get_text()
    tag = soup.find('p',{'class':'tag'}).get_text()
    time = datetime.find('div',{'class':'hint'}).get_text()
    if tag == "In Transit":
        tag_th = u"กำลังส่ง"
    elif tag == "Delivered":
        tag_th = u"ถึงที่หมาย"
    elif tag == "Out For Delivery":
        tag_th = u"กำลังจำหน่าย ตามบ้าน"
    time = datetime.find('div',{'class':'hint'}).get_text()
    return {"place": place, "date":date, "time":time, "tag":tag, "tag_th" :tag_th}

if __name__ == '__main__':
    app.run(debug=True)
