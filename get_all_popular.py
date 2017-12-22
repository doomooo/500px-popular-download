# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 21:07:55 2017
本脚本仅供学习使用，请勿商用

本程序自动下载500px 所有热门图片，并且按照类目放入对应文件夹中


"""
import requests
import json
import time
import urllib.request

import threading

import os

max_page=100  #图片页面个数

time_interval=0.5

core_num=4

with open('categories.json','r') as ff:
    categories=json.load(ff)
    
for category in  categories:
    print(category)
    path=category
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
    else:
        continue

    
    def get_popular_photo(page,category):  #根据 目录 页数获得当前页面的所有图片
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',\
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection':'keep-alive',
            'Cookie':'optimizelyEndUserId=oeu1513674970221r0.5680820057707299; optimizelySegments=%7B%22569090246%22%3A%22false%22%2C%22569491641%22%3A%22direct%22%2C%22575800731%22%3A%22gc%22%2C%22589900200%22%3A%22true%22%7D; optimizelyBuckets=%7B%7D; _ga=GA1.2.2054774405.1513674982; _gid=GA1.2.2082149731.1513674982; device_uuid=5df55a84-dc4e-4396-91df-f866be52f6ee; __hstc=133410001.1b5ee8189dc2b96d0e9a7b9f9a40e021.1513675008578.1513675008578.1513675008578.1; __hssrc=1; hubspotutk=1b5ee8189dc2b96d0e9a7b9f9a40e021; _hpx1=BAh7C0kiD3Nlc3Npb25faWQGOgZFVEkiJWFmNTcyZDExYTdmOWU0YjM5YmVjNmE4OTYyMThmYWY3BjsAVEkiCWhvc3QGOwBGIg41MDBweC5jb21JIhl1c2Vfb25ib2FyZGluZ19tb2RhbAY7AEZUSSIYc3VwZXJfc2VjcmV0X3BpeDNscwY7AEZGSSIQX2NzcmZfdG9rZW4GOwBGSSIxR0NGaUdXWlNDRThBVXkrVjBtT2YxYXUyTVR3elhRZk91SnZWVUtXdDhtdz0GOwBGSSIRcHJldmlvdXNfdXJsBjsARkkiNS9waG90by8yMzk1NjE4ODMvcGVyZmVjdC1wYWlyLWJ5LXRpbW90aHktcG91bHRvbgY7AFQ%3D--b91a4f3b994a4a397acfdc4aa0a8f6a20a11a20a; amplitude_id500px.com=eyJkZXZpY2VJZCI6ImNjMmMzMGMwLWNmZTItNGRhZi04MzA2LWNlMjE2OGY3MGMxOFIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTUxMzY4MDIxMDM3MiwibGFzdEV2ZW50VGltZSI6MTUxMzY4MDUyNjI0OSwiZXZlbnRJZCI6MiwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjJ9; optimizelyPendingLogEvents=%5B%22n%3Doptly_activate%26u%3Doeu1513674970221r0.5680820057707299%26wxhr%3Dtrue%26time%3D1513680526.333%26f%3D9502403088%2C8746762262%2C9737453591%2C9372932120%2C9729990917%2C9502690399%2C9832741456%2C8478672984%2C9661320798%2C9738180735%2C9503661200%2C9732794009%2C8179770025%2C8781643456%2C9510832862%2C9494972573%2C8478040821%2C8560956350%2C8602833193%2C8484780344%2C9660800875%2C9518490284%2C8345881987%2C8740624971%2C9510101479%26g%3D%22%2C%22n%3Dhttps%253A%252F%252F500px.com%252Fphoto%252F239561883%252Fperfect-pair-by-timothy-poulton%26u%3Doeu1513674970221r0.5680820057707299%26wxhr%3Dtrue%26time%3D1513680526.3%26f%3D9502403088%2C8746762262%2C9737453591%2C9372932120%2C9729990917%2C9502690399%2C9832741456%2C8478672984%2C9661320798%2C9738180735%2C9503661200%2C9732794009%2C8179770025%2C8781643456%2C9510832862%2C9494972573%2C8478040821%2C8560956350%2C8602833193%2C8484780344%2C9660800875%2C9518490284%2C8345881987%2C8740624971%2C9510101479%26g%3D582890389%22%5D',
            'DNT':'1',
            'Host':'api.500px.com',
            'If-None-Match':'W/"290ac8cc4062b3cf343f3841aed29a04"',
            'Origin':'https://500px.com',
            'Referer':'https://500px.com/popular?personalized=true',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'X-CSRF-Token':'ERRyt1/PjMxruhSTT1VPBaOg4aUfZbsnJqmaym+ef6wJNRCuOZ2Eg2vpOwadNtDQCBbQmSw4vOmeMk+ayjONwA=='        
            }
    
        url='https://api.500px.com/v1/photos?rpp=50&feature=popular&image_size%5B%5D=1&image_size%5B%5D=2&image_size%5B%5D=32&image_size%5B%5D=31&image_size%5B%5D=33&image_size%5B%5D=34&image_size%5B%5D=35&image_size%5B%5D=36&image_size%5B%5D=2048&image_size%5B%5D=4&image_size%5B%5D=14&sort=&include_states=true&include_licensing=false&formats=jpeg%2Clytro&only='+category+'&exclude=&personalized_categories=true&page='+str(page)+'&rpp=50'
    
        req = urllib.request.Request(url=url, headers=headers)    
        webPage=urllib.request.urlopen(req)  
        data = webPage.read()  
        data = data.decode('UTF-8')  
        data=json.loads(data)
        data=data['photos']
        return data
    
    
    lock=threading.Lock()
    
    photo_polpular_info=[]
    def get_all_list(start_page,page_interval):
        global photo_polpular_info
        for i in range(start_page,max_page,page_interval):
            list_temp=get_popular_photo(i,category)
            if len(list_temp)==0:
                break
            lock.acquire()
            try:
                photo_polpular_info.extend(list_temp)
            finally:
                lock.release()      
            time.sleep(time_interval)
            print(i)
        return photo_polpular_info
    
      
    for i in range(core_num):
        t=threading.Thread(target=get_all_list,args=(i,core_num,))
        t.setDaemon(True)
        t.start()
        
        
    
    time.sleep(25)  #设置缓冲区域
    
        
                
    end_id=100000
    check_pic=0
    def download_500(star_id,id_interval):  #为了有助于 多线程，设置起点和间隔，所有线程下载间隔的图片
        global check_pic
        for i in range(star_id,end_id,id_interval):
            try:
                response = urllib.request.urlopen(photo_polpular_info[i]['image_url'][len(photo_polpular_info[i]['image_url'])-2])
                imgg = response.read()
                name=category+'/'+str(photo_polpular_info[i]['id'])+'.'+photo_polpular_info[i]['image_format']
                
                with open(name,'wb') as f:
                    f.write(imgg)
                
                time.sleep(time_interval)
                            
                if i %10 ==0:
                    print('目前已经完成 %s--第%d张图片，共计%d' %(category,i,len(photo_polpular_info)) )
            except:
                pass
                
            finally:
                pass
            if i==len(photo_polpular_info)-1:
                file_name = category+'/'+category+'.json'
                with open(file_name, 'w') as file_obj:
                    json.dump(photo_polpular_info, file_obj)
                    check_pic += 1
                        
            if (i+id_interval)>=len(photo_polpular_info):            
                break
            
                
                    
    
    all_pic=len(photo_polpular_info)  
    core_pic=all_pic//core_num
    
    threads = [] 
    for i in range(core_num) :
        threads.append(threading.Thread(target=download_500,args=(i,core_num,)))
    
    for t in threads:
        t.setDaemon(True)  #设置为守护线程，以免主线程结束，该线程也就结束了
        t.start()  
        
    i=check_pic
    while i<core_num:
        time.sleep(60)
        i=check_pic
        if check_pic==1:
            break
        
    
