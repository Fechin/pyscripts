#!/usr/bin/env python
# coding=utf-8
'''
@author Fechin 
@version V 1.0
@date 2014年 06月 10日 星期二 10:22:37 CST
'''

from BeautifulSoup import BeautifulSoup
import sys
import urllib
import urllib2
import cookielib
import logging
import json

reload( sys )
sys.setdefaultencoding( 'utf-8' )

# 用户名/身份证号
username = ''

# 登录密码，配置为空时取默认密码
password = ''

# 预约日期(yyyyMMdd)
_date = '20140614'

# 预约时段,可选值(早上，中午，晚上，不限)
_time = '早上'

# 科目类型，可选值(科目二，科目三)
car_type = '科目二'


class haveCar():
    def __init__( self ):

        self.viewstate = '/wEPDwUKMTg0NDI4MDE5OGRkFUZOE3C7QQL4pJ/OooIN7IVnK5Qfznhym5mN84V5JNQ='
        self.eventvalidation = '/wEWBgKyrJC6AwKl1bKzCQK1qbSRCwLoyMm8DwLi44eGDAKAv7D9CmhsXW9MljUvafu1DHCUaQFrdAWsE0NBXcwobLtWNjsS'

        # 登录地址
        self.login_url = 'http://yuanda.bjxueche.net'
        
        # 约车首页
        self.car_home = self.login_url + '/ych2.aspx'

        # 伪装浏览器
        self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6', 
            'Host' : 'yuanda.bjxueche.net',
            'Referer' : self.car_home,
            'Origin' : self.login_url
        }

        # 获取一个cookie对象
        self.cookie = cookielib.CookieJar()

        # 构建cookie处理器
        cookie_p = urllib2.HTTPCookieProcessor( self.cookie )

        # 装载cookie
        self.opener = urllib2.build_opener( cookie_p )

        # 日志工具
        self.logger = loggerHelper( '约车这等小事' )

        # 预约时段初始化 08:00-12:00 13:00-17:00 17:00-20:00
        self.timedict = { '早上':'812','中午':'15','晚上':'58','不限':'0'}

        # 预约科目类型
        self.cartypedict = { '科目二':'Km2Car2','科目三':'Km3Car2'}


    def get_value( self,_key,_dict ):
        if _key not in _dict.keys():
            self.logger.debug( '预约时段或科目类型配置有误!' )
            exit(0)
        else:
            return _dict.get(_key)

    def get_pass( self,_pass):
        if _pass == '':
            return username[8:14]  
        else:
            return _pass

    def get_html( self,url,_params = None,useFind = False,_args = 'body',_attrs = None):
        
        if _params is not None:
            _params = urllib.urlencode( _params )

        req = urllib2.Request( url,_params,self.headers )
        res = self.opener.open( req )
        html = res.read()

        if useFind == True:
            soup = BeautifulSoup( html )

            if _attrs is not None:
                html = soup.findAll( attrs=_attrs )
            else:
                html = soup.find(_args)
        return html

    def login_jx( self ):
        params ={
            '__VIEWSTATE' : self.viewstate,
            '__EVENTVALIDATION' : self.eventvalidation,
            'txtUserName' : username,
            'txtPassword' : self.get_pass(password),
            'BtnLogin' : '登  录'
        }

        self.get_html( self.login_url,params )

        if not 'LoginOn' in [c.name for c in self.cookie]:
            self.logger.debug( '登录失败' )
            exit(0)
        else:
            self.logger.debug( '用户：%s ,登录成功' %username )


    def get_stuinfo( self ):
        # 学员信息
        stu_info = self.login_url + '/GetStudentInfo.ashx'

        _str = self.get_html( stu_info )
        
        if '错误页' in _str:
            self.logger.debug( '登录超时，请重新登录' )
            exit(0)

        width = 80
        _title = '学习证号,姓名,总学时,训练,预约,违约,剩余,距离技能证书过期还剩,状态,车型,0'
        if _str is None:
            self.logger.debug( '获取用户信息失败' )
            exit(0)
        else:
            _iflst = _str.split( ',' )
            _ttlst = _title.split( ',' )
            print '^' * width

            for i in range( 0,len(_iflst),3 ):
                if i == 9:
                    print "> %10s:%-10s" % ( _ttlst[i],_iflst[i] )
                    break
                print "> %10s:%-10s %22s:%-20s %s:%-10s" % ( _ttlst[i],_iflst[i], _ttlst[i+1],_iflst[i+1],_ttlst[i+2],_iflst[i+2] )

            print '^' * width


    def start( self,yyrq,yysd,type ):

        # 可约列表
        car_list_url = self.login_url + '/Tools/km2.aspx'

        # 根据预约日期及预约时段查询
        attrs = { 'yyrq':yyrq }
        if not yysd == '0':
            attrs['yysd'] = yysd

        _tds = self.get_html( self.car_home,None,True,'',attrs )

        if len(_tds) == 0:
            self.logger.debug( '请检查您填写的预约日期或预约时间' )
            exit(0)

        # 检查是否有车可约，有则获取可约列表
        _params = {
            'date':'', #! is need ?
            'filters[yyrq]':yyrq,
            'filters[xnsd]':yysd,
            'filters[xllxid]':'1', #! what
            'filters[type]':type,
            'filters[orderby]':'',
            'filters[cnbh]':'',
            'orderBy':'',
            'pageno':1,
            'pagesize':10
        }
        _yeah_params = {
            'yyrqbegin':yyrq,
            'xnsd':yysd,
            'trainType':1, #! 1-5 1-7?
            'type':self.get_value( car_type,self.cartypedict )#! km2Car2
        }

        for td in _tds:
            if '有' in td:
                _car_str= self.get_html( car_list_url,_params )
                
                if _car_str is None or _car_str == 'null_0':
                    continue
                _car_str = _car_str[:_car_str.find( '_' )]

                _car_json = json.loads( _car_str )
                for _jlc in _car_json:
                    _yeah_params['jlcbh'] = _jlc['JLCBH']

                    wonderful = self.get_html( car_list_url,_yeah_params )

                    if '操作成功' in wonderful:
                        print '成功.'
                        exit(0)
                    else:
                        print wonderful 

class loggerHelper():
    '''
    日志记录帮助类
    '''
    def __init__( self , moduleName = 'jx' ):

        self.logger = logging.getLogger( moduleName )
        self.logger.setLevel( logging.DEBUG )

        ch = logging.StreamHandler()
        ch.setLevel( logging.DEBUG )

        formatter = logging.Formatter( '%(asctime)s - %(name)s : %(message)s' )
        ch.setFormatter( formatter )

        self.logger.addHandler( ch )
    def debug( self,msg ):
        self.logger.debug( msg )


if __name__ == '__main__':
    run = haveCar()
    run.login_jx()
    run.get_stuinfo()
    _timed = run.get_value( _time,run.timedict )
    run.start( _date,_timed,'km2Car' )
