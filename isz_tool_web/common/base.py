
import logging
import configparser
import pymysql
from xlrd import open_workbook
import os
from email.mime.text import MIMEText
from email.header import Header
import smtplib,datetime


logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
path = os.path.dirname(
    os.path.join(
        os.path.split(
            os.path.realpath(__file__))[0])) + '\\test.log'
fileHandler = logging.FileHandler(path)
consoleHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(process)s - %(levelname)s : %(message)s')
fileHandler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)



def log(func):
    def wrapper(*args, **kwargs):
        logger.info(func.__doc__)
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            return e
    return wrapper



def consoleLog(msg, level='i'):
    """
    对错误的记录，写进log文件中
    则调用此方法，定义为error级别
    :param msg: 需要写入的描述，如’合同删除后deleted未变成0‘
    :param level: 定义日志级别，分为i:info  w:warning  e:error
    """
    if level is 'i':
        logger.info(msg)
    elif level is 'w':
        logger.warning(msg)
    elif level is 'e':
        logger.error('one assert at : \n%s\n' % msg)

def get_conf(section, option, valueType=str):
    """
    获取配置文件值
    :param section: 配置文件的片段
    :param option: 配置文件对应的key
    :param valueType: 默认值
    :return:
    """
    config = configparser.ConfigParser()
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0]) + '\conf.ini'
    config.read(path,encoding="utf-8")
    if valueType is str:
        value = config.get(section, option)
        return value
    elif valueType is int:
        value = config.getint(section, option)
        return value
    elif valueType is bool:
        value = config.getboolean(section, option)
        return value
    elif valueType is float:
        value = config.getfloat(section, option)
        return value
    else:
        value = config.get(section, option)
        return value.decode('utf-8')


# def set_conf(section,k,v):
#     """
#     写入值到配置文件中
#     :param section: 配置文件中的片段名称
#     :param value: 配置文件中的key
#     :return:
#     """
#     config = configparser.ConfigParser()
#     path = os.path.join(os.path.split(os.path.realpath(__file__))[0]) + '\conf.ini'
#     config.read(path,encoding="utf-8")
#     config.set(section, k, v)
#     config.write(open(path, 'w'))
#
def set_conf(section,**value):
    """
    写入值到配置文件中
    :param section: 配置文件中的片段名称
    :param value: 配置文件中的key
    :return:
    """
    config = configparser.ConfigParser()
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0]) + '\conf.ini'
    config.read(path,encoding="utf-8")
    for k, v in value.items():
        config.set(section, k, v)
    config.write(open(path, 'w'))

sqlConn = pymysql.connect(host=get_conf('db','host'), user=get_conf('db','user'), password=get_conf('db','password'), db=get_conf('db','db'), charset=get_conf('db','charset'), port=3306)
sqlCursor = sqlConn.cursor()

def searchSQL(sql):
    """
    :param sql: 需要执行的SQL
    :return:
    """
    sqlCursor.execute(sql)
    value = sqlCursor.fetchall()
    return value

def get_count(sql):
    """返回查询数量"""
    count = sqlCursor.execute(sql)
    return count


def get_xlrd(xls_name,xls_sheet,value=False):
    """
    :param xls_name: 用例表格名称
    :param xls_sheet: 用例表格页签名称
    :return:
    """
    "read xled"
    cls = []
    xlsPath = os.path.join(get_conf("caseroute","path"), "caseFile",  xls_name)
    file = open_workbook(xlsPath)
    sheets = file.sheet_by_name(xls_sheet)
    nrows = sheets.nrows
    if value:
        for i in range(nrows):
            if nrows - i > 1:
                cls.append(sheets.row_values(i+1))
    else:
        for i in range(nrows):
            cls.append(sheets.row_values(i))
    return cls


def host_set(condition):
    """
    插入地址到本地hosts
    :param condition: 预发还是测试环境的标识
    :return:
    """
    set_conf('testCondition', test=condition)
    filepath = r'C:\Windows\System32\drivers\etc\hosts'
    hosts = None
    f = open(filepath, 'w')
    if condition == 'test':
        set_conf('db', host='192.168.0.208', user='zhonglinglong', password='zll.123', db='isz_erp_npd', charset='utf8')
        set_conf('dbservice', host='192.168.0.208', user='zhonglinglong', password='zll.123', db='isz_rsm', charset='utf8')
        hosts = get_conf('host','test')
    elif condition == 'mock':
        set_conf('db', host='192.168.0.208', user='zhonglinglong', password='zll.123', db='isz_erp', charset='utf8')
        set_conf('dbservice', host='192.168.0.208', user='zhonglinglong', password='zll.123', db='isz_rsm_pre', charset='utf8')
        hosts = get_conf('host','mock')
    f.write(hosts)
    f.close()

def send_email(info,sendMe=False):
    """
    发送邮件
    :param info: 需要发送的内容
    :param sendMe:
    :return:
    """
    msg = MIMEText(info, 'plain', 'utf-8')
    user = 'zhonglinglong@ishangzu.com'
    pwd = 'Long268244'
    smtp_server = 'smtp.mxhichina.com'
    time = str(datetime.date.today() - datetime.timedelta(days=1))
    msg['From'] = '爱上租-技术部-内部产品测试组-钟玲龙<%s>' % user
    if sendMe:
        msg['Subject'] = Header('%s服务系统接口报错信息' % time, 'utf-8').encode()
        to_addr = ['zhonglinglong@ishangzu.com']
        msg['To'] = ('zhonglinglong<%s>' % to_addr[0])
    else:
        msg['Subject'] = Header('%s服务系统接口自动化报告' % time, 'utf-8').encode()
        to_addr = ['zhonglinglong@ishangzu.com']
        msg['To'] = ('zhonglinglong<%s>' % (to_addr[0]))
    msg['From'] = user
    server = smtplib.SMTP(smtp_server, 25)
    # server.set_debuglevel(1)
    server.login(user, pwd)
    server.sendmail(user, to_addr, msg.as_string())
    server.quit()


