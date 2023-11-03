# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/2 00:35
@Auth ： 浮生半日闲
@File ： utility.py
@IDE ： PyCharm
@Motto：Code changes Everything

"""

import ephem
import math


class MxzCalendar(object):
    def __init__(self):

        # 天干
        self.heavenlyStem = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

        # 地支
        self.terrestrialBranch = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

        self.monthCn = ["正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月",
                        "十二月"]

        self.dateCn = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                       "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                       "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]

        # 六十甲子表
        self.gz = [''] * 60
        for i in range(60):
            self.gz[i] = self.heavenlyStem[i % 10] + self.terrestrialBranch[i % 12]

    def lunar_calendar(self, nian, typeValue=1):  # typeValue=1时截止到次年冬至朔，=0时截止到次年冬至朔次月
        dzs = self.findDZS(nian)
        shuoMonth = dzs  # 计算用朔，date格式
        shuoMonthJulianDate = [ephem.julian_date(dzs)]  # 存储ut+8 julianDate，起冬至朔
        next_dzsJulianDate = ephem.julian_date(self.findDZS(nian + 1))  # 次年冬至朔
        i = -1  # 中气序，从0起计
        j = -1  # 计算连续两个冬至月中的合朔次数，从0起计
        zry = 0
        flag = False
        # 查找所在月及判断置闰
        while not self.date_compare(shuoMonthJulianDate[j + typeValue], next_dzsJulianDate):  # 从冬至月起查找，截止到次年冬至朔
            i += 1
            j += 1
            shuoMonth = ephem.next_new_moon(shuoMonth)  # 次月朔
            shuoMonthJulianDate.append(ephem.julian_date(shuoMonth))
            # 查找本月中气，若无则置闰
            if j == 0:
                continue  # 冬至月一定含中气，从次月开始查找
            angle = (-90 + 30 * i) % 360  # 本月应含中气，起冬至
            qJulianDate = self.solar_terms(nian, angle)
            # 不判断气在上月而后气在后月的情况，该月起的合朔次数不超过气数，可省去
            if self.date_compare(qJulianDate, shuoMonthJulianDate[j + 1]) and flag == False:  # 中气在次月，则本月无中气
                zry = j + 1  # 置闰月
                i -= 1
                flag = True  # 仅第一个无中气月置闰
        # 生成农历月序表
        ymb = []
        for k in range(len(shuoMonthJulianDate)):
            ymb.append(self.monthCn[(k - 2) % 12])  # 默认月序
            if j + typeValue == 13:  # 仅12次合朔不闰，有闰时修改月名
                if k + 1 == zry:
                    ymb[k] = '闰' + self.monthCn[(k - 1 - 2) % 12]
                elif k + 1 > zry:
                    ymb[k] = self.monthCn[(k - 1 - 2) % 12]
        return ymb, shuoMonthJulianDate  # 月名表，合朔julianDate日期表

    def solar_to_lunar_calendar(self, date):  # 默认输入ut+8时间
        if date[0] == '0':
            return '不存在公元0年'
        julianDate = ephem.julian_date(date) - 8 / 24  # ut
        year, month, day = self.julian_to_date(julianDate, 8).triple()
        # 判断所在年
        dzs = self.findDZS(year)  # 本年冬至朔
        next_dzs = self.findDZS(year + 1)  # 次年冬至朔
        this_dzsJulianDate = ephem.julian_date(dzs)
        next_dzsJulianDate = ephem.julian_date(next_dzs)
        nian = year  # 农历年
        if self.date_compare(julianDate, next_dzsJulianDate):  # 该日在次年
            nian += 1
        if not self.date_compare(julianDate, this_dzsJulianDate):  # 该日在上年
            nian -= 1
        # 判断所在月
        ymb, shuoMonthJulianDate = self.lunar_calendar(nian)
        szy = self.findSZY(julianDate, shuoMonthJulianDate)
        # 判断节气月
        if year < 0:
            year += 1
        jqy, jqr = self.julian_to_date(self.solar_terms(year, month * 30 + 255), 8).triple()[1:]
        if int(jqy) != month:
            month -= (int(jqy) - month)
        if day >= int(jqr):
            ygz = self.gz[(year * 12 + 12 + month) % 60]
        else:
            ygz = self.gz[(year * 12 + 11 + month) % 60]
        # 以正月开始的年干支
        if szy < 3:
            nian -= 1  # 正月前属上年
        if nian < 0:
            nian += 1
        ngz = self.gz[(nian - 4) % 60]
        rgz = self.gz[math.floor(julianDate + 8 / 24 + 0.5 + 49) % 60]
        rq = self.date_differ(julianDate, shuoMonthJulianDate[szy])  # 月内日期
        return date + ' 为农历：' + ngz + '年 ' + ygz + '月 ' + rgz + '日 ' + ymb[szy] + self.dateCn[rq] + '\n'

    def lunar_to_solar_calendar(self, nian, date):  # 正月开始的年
        date1 = date.split('闰')[-1]
        year = nian
        yx = self.monthCn.index(date1[:-2])
        if yx + 1 > 10:
            year += 1  # 计算用年，起冬至朔
        if year == 0:
            return '不存在公元0年'
        yx = (yx + 2) % 12  # 子正转为寅正
        if "闰" in date:
            yx += 1
        # 查找所在月
        ymb, shuoMonthJulianDate = self.lunar_calendar(year, 0)
        szy = 0
        for i in range(len(ymb)):
            if ymb[i] == date1[:-2]:  # 按月序查找
                if ymb[i + 1] == date[:-2] or '闰' in date:
                    szy += 1  # 可能为闰月（不闰则计算次月）
                break
            szy += 1
        # 获得农历日期
        try:
            rq = self.dateCn.index(date[-2:])
        except:
            rgz = self.gz.index(date[-2:])
            sgz = math.floor(shuoMonthJulianDate[szy] + 8 / 24 + 0.5 + 49) % 60
            rq = (rgz - sgz) % 60
            if self.date_compare(shuoMonthJulianDate[szy] + rq, shuoMonthJulianDate[szy + 1]):
                print('该月无' + date[-2:])
            else:
                print(date[-2:] + '为该月' + self.dateCn[rq] + '日')
        date2 = str(self.julian_to_date(shuoMonthJulianDate[szy] + rq, 8))[:-9]
        return '农历' + str(nian) + '年' + date + ' 为公历：' + date2

    @staticmethod
    def julian_to_date(julianDate, ut=0):
        return ephem.Date(julianDate + ut / 24 - 2415020)

    @staticmethod
    def equinox_solstice_julian_date(year, angle):
        if 0 <= angle < 90:
            date = ephem.next_vernal_equinox(year)
        elif 90 <= angle < 180:
            date = ephem.next_summer_solstice(year)
        elif 180 <= angle < 270:
            date = ephem.next_autumn_equinox(year)
        else:
            date = ephem.next_winter_solstice(year)
        julianDate = ephem.julian_date(date)
        return julianDate

    @staticmethod
    def date_differ(julianDate1, julianDate2):
        return math.floor(julianDate1 + 8 / 24 + 0.5) - math.floor(julianDate2 + 8 / 24 + 0.5)

    # 计算二十四节气
    def solar_longitube(self, julianDate):
        date = self.julian_to_date(julianDate)
        s = ephem.Sun(date)  # date应为UT时间
        sa = ephem.Equatorial(s.ra, s.dec, epoch=date)
        se = ephem.Ecliptic(sa)
        L = se.lon / ephem.degree / 180 * math.pi
        return L

    def solar_terms(self, year, angle):
        if angle > 270:
            year -= 1  # 岁首冬至
        if year == 0:
            year -= 1  # 公元0改为公元前1
        julianDate = self.equinox_solstice_julian_date(str(year), angle)  # 初值
        if angle >= 270:
            julianDate0 = self.equinox_solstice_julian_date(str(year), (angle - 90) % 360)
            if julianDate < julianDate0:  # 非年末冬至
                julianDate = self.equinox_solstice_julian_date(str(year + 1), angle)  # 转入次年
        julianDate1 = julianDate
        while True:
            julianDate2 = julianDate1
            L = self.solar_longitube(julianDate2)
            julianDate1 += math.sin(angle * math.pi / 180 - L) / math.pi * 180
            if abs(julianDate1 - julianDate2) < 0.00001:
                break  # 精度小于1 second
        return julianDate1  # UT

    def date_compare(self, julianDate1, julianDate2):  # 输入ut，返回ut+8的比较结果
        if self.date_differ(julianDate1, julianDate2) >= 0:
            return True  # julianDate1 >= julianDate 2
        else:
            return False

    def findSZY(self, julianDate, shuoMonthJulianDate):  # 查找julianDate所在的农历月份
        szy = -1
        for i in range(len(shuoMonthJulianDate)):
            if self.date_compare(julianDate, shuoMonthJulianDate[i]):
                szy += 1  # date所在的阴历月序，起冬至朔
        return szy

    def findDZS(self, year):  # 寻找年前冬至月朔日
        if year == 1:
            year -= 1  # 公元元年前冬至在公元前1年
        dz = ephem.next_solstice((year - 1, 12))  # 年前冬至
        jd = ephem.julian_date(dz)
        # 可能的三种朔日
        date1 = ephem.next_new_moon(self.julian_to_date(jd - 0))
        jd1 = ephem.julian_date(date1)
        date2 = ephem.next_new_moon(self.julian_to_date(jd - 29))
        jd2 = ephem.julian_date(date2)
        date3 = ephem.next_new_moon(self.julian_to_date(jd - 31))
        jd3 = ephem.julian_date(date3)
        if self.date_compare(jd, jd1):  # 冬至合朔在同一日或下月
            return date1
        elif self.date_compare(jd, jd2) and (not self.date_compare(jd, jd1)):
            return date2
        elif self.date_compare(jd, jd3):  # 冬至在上月
            return date3
