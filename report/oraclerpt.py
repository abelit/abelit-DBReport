# -*- coding:utf-8 -*-
'''
@project: '__dbreport__.py'
@modules: report.oraclerpt
@description:

@author: abelit
@email: ychenid@live.com
@created:Mar 5, 2018

@licence: GPL
'''

__version__ = '''$Id$'''
# from reportlab.lib.testutils import outputfile,setOutDir
# setOutDir(__name__)
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.frames import Frame
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.flowables import Spacer, Preformatted
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate, NextPageTemplate
from reportlab.platypus import tableofcontents, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import  Table, TableStyle
from reportlab.lib import colors
from reportlab.graphics import shapes
from reportlab.graphics.widgets import signsandsymbols
# 导入生产条形码的工具包
from reportlab.graphics.barcode import eanbc, qr
from reportlab.graphics.shapes import Drawing, Image, Rect
from reportlab.graphics import renderPDF

# 导入注册字体的模块
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import Image as platImage

from math import sqrt
import datetime, calendar, time
import random
import io

# 导入画图模块
import matplotlib.pyplot as plt
# import matplotlib.dates as mdates

# 导入自定义模块
# 导入数据库信息提取模块
from report.database import Oracle
# 导入系统获取操作系统信息模块
from report.host import HostMetric
from config import settings

# 注册字体
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
pdfmetrics.registerFont(TTFont('msyh', settings.path_settings['font'] + 'msyh.ttf'))


myFontName = 'msyh'

class BarCodes:
    barcode_value = ''
    for i in range(10):
        barcode_value = barcode_value + str(random.randint(0, 9))

    def genEan13Barcode(self, canvas, x, y, width=50, height=10, barcode_value=barcode_value):
        # draw the eanbc13 code
        barcode_eanbc13 = eanbc.Ean13BarcodeWidget(barcode_value)
        d = Drawing(width=width, height=height)
        d.add(barcode_eanbc13)
        renderPDF.draw(d, canvas, x, y)

    def genEan8Barcode(self, canvas, x, y, width, height, barcode_value="1234567890"):
        # draw the eanbc8 code
        barcode_eanbc8 = eanbc.Ean8BarcodeWidget(self.barcode_value)
        d = Drawing(width=width, height=height)
        d.add(barcode_eanbc8)
        renderPDF.draw(d, canvas, x, y)

    def genQrCode(self, canvas, x, y, width, height, qr_value='http://www.dataforum.org'):
        # draw a QR code
        qr_code = qr.QrCodeWidget(qr_value)
        bounds = qr_code.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        d = Drawing(width, height, transform=[45. / width, 0, 0, 45. / height, 0, 0])
        d.add(qr_code)
        renderPDF.draw(d, canvas, x, y)


class DrawShape:
    def drawArrow(self, xdraw, ydraw, size, rotate, x, y, color):
        # drawArrow(10,20,20,90,0,-15,colors.green)
        # drawArrow(10,20,20,-90,-20,-5,colors.red)
        # 画绿色向上箭头
        d = shapes.Drawing(xdraw, ydraw)
        ao = signsandsymbols.ArrowOne()
        ao.fillColor = color
        ao.size = size
        d.rotate(rotate)
        ao.x, ao.y = x, y
        d.add(ao)

        return d

    def drawAlert(self, xdraw, ydraw, size, x, y, strokewidth, color):
        # drawAlert(20,20,20,0,0,4,colors.red)
        # drawAlert(20,20,20,0,0,0,colors.green)
        # 画告警图
        d = Drawing(xdraw, ydraw)
        ds = signsandsymbols.DangerSign()
        ds.x, ds.y = x, y
        ds.size = size
        ds.strokeWidth = strokewidth
        ds.fillColor = color
        d.add(ds)

        return d

    def drawSmile(self, xdraw, ydraw, size, x, y):
        # drawSmile(20,20,20,0,0)
        d = Drawing(xdraw, ydraw)
        ds = signsandsymbols.SmileyFace()
        ds.x, ds.y = x, y
        ds.size = size
        d.add(ds)

        return d

    def drawCrossbox(self, xdraw, ydraw, size, x, y, crosscolor, fillcolor):
        # drawCrossbox(20,20,20,0,0,colors.red,colors.white)
        # drawCrossbox(20,20,20,0,0,colors.green,colors.green)
        # 画Xbox信息
        d = Drawing(xdraw, ydraw)
        ds = signsandsymbols.Crossbox()
        ds.x, ds.y = x, y
        ds.size = size
        ds.crosswidth = 3
        ds.crossColor = crosscolor
        ds.fillColor = fillcolor
        d.add(ds)

        return d

    def drawBattery(self, xdraw, ydraw, pct, pctcolor):
        # drawBattery(25,20,5,colors.green)
        # 画使用率图
        d = Drawing(xdraw, ydraw)
        r = Rect(0, 0, 25 * pct, ydraw)
        r.fillColor = pctcolor
        r.strokeColor = colors.green
        r.strokeWidth = 0

        s = Rect(0, 0, xdraw, ydraw)
        s.fillColor = colors.white
        s.strokeColor = colors.green
        d.add(s)
        d.add(r)

        return d

def plot_curve(x, y, title, xlabel, ylabel):
    plt.figure(figsize=(20, 5))
#     xs = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in x]
#     plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
#     plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    plt.title(title)
    plt.plot(x, y, 'o-')
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
#     plt.show()
    imgdata = io.BytesIO()
    plt.savefig(imgdata, format='png')
    imgdata.seek(0)  # rewind the data

    img = platImage(imgdata, 600, 180)

    return img


#
def makeHeaderStyle(level, fontName=myFontName):
    "Make a header style for different levels."

    assert level >= 0, "Level must be >= 0."

    PS = ParagraphStyle
    size = 24.0 / sqrt(1 + level)
    style = PS(name='Heading' + str(level),
               fontName=fontName,
               fontSize=size,
               leading=size * 1.2,
               spaceBefore=size / 4.0,
               spaceAfter=size / 8.0)
    return style


def makeBodyStyle(fontName=myFontName, firstLineIndent=20):
    "Body text style - the default will do"
#     return ParagraphStyle('body')
    styleSheet = getSampleStyleSheet()
    myBodyStyle = styleSheet['BodyText']
    myBodyStyle.fontName = fontName
    myBodyStyle.leading = 14
    myBodyStyle.firstLineIndent = firstLineIndent
    myBodyStyle.wordWrap = 'CJK'

    return myBodyStyle


def makeTitleStyle(fontSize=18, fontName=myFontName):
    "Title text style - the default will do"
#     return ParagraphStyle('body')
    styleSheet = getSampleStyleSheet()
    myTitleStyle = styleSheet['Title']
    myTitleStyle.fontName = fontName
    myTitleStyle.fontSize = fontSize

    return myTitleStyle

def makeListTitleStyle(fontSize=18, fontName=myFontName):
    "Title text style - the default will do"
    styleSheet = getSampleStyleSheet()
    myTitleStyle = styleSheet['Title']
    myTitleStyle.alignment = TA_LEFT
    myTitleStyle.fontName = fontName
    myTitleStyle.fontSize = fontSize

    return myTitleStyle

def makeTocHeaderStyle(level, delta, epsilon, fontName=myFontName):
    "Make a header style for different levels."

    assert level >= 0, "Level must be >= 0."

    PS = ParagraphStyle
    size = 12
    style = PS(name='Heading' + str(level),
               fontName=fontName,
               fontSize=size,
               leading=size * 1.2,
               spaceBefore=size / 4.0,
               spaceAfter=size / 8.0,
               firstLineIndent=-epsilon,
               leftIndent=level * delta + epsilon)

    return style

def makeTableTitleStyle(fontSize=12, fontName=myFontName):
    styleSheet = getSampleStyleSheet()
    myTitleStyle = styleSheet['BodyText']
    myTitleStyle.alignment = TA_CENTER
    myTitleStyle.leading = 18
    myTitleStyle.fontName = fontName
    myTitleStyle.fontSize = fontSize

    return myTitleStyle

def makeTable(data, title=None, note=None, colwidth=None):
    lst = []

#     if colwidth is not None:
#         cw = list(colwidth)
#         for i in range(len(cw)-1):
#             cw[i] = cw[i] * tablewidth
#         colwidth = tuple(cw)
    t = Table(data, colWidths=colwidth)
    ts = TableStyle(
    [('LINEABOVE', (0, 0), (-1, 0), 2, colors.green),
     ('LINEABOVE', (0, 1), (-1, -1), 0.25, colors.black),
     ('LINEBELOW', (0, -1), (-1, -1), 3, colors.green, 'butt'),
     ('LINEBELOW', (0, -1), (-1, -1), 1, colors.white, 'butt'),
     ('FONT', (0, 0), (-1, 0), 'msyh'),
    ('FONT', (0, 0), (-1, -1), 'msyh'),
     ('FONTSIZE', (0, 0), (-1, -1), 8),
     ('ALIGN', (2, 1), (-1, -1), 'LEFT'),
     ('TEXTCOLOR', (0, 1), (0, -1), colors.black),
     ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0, 0.7, 0.7))]
    )
    t.setStyle(ts)
    if title is not None:
        lst.append(Paragraph(title, makeTableTitleStyle()))
    lst.append(t)
    if note is not None:
        lst.append(Paragraph(note, makeBodyStyle()))
    lst.append(Spacer(0, 0.5 * cm))
    return lst

def wrapTable(data, cols=None, style=makeBodyStyle(firstLineIndent=0)):
    ''' To auto wrap text in the cells of the table.
    usage: data = wrapTable(data, cols=[1,2])
    '''
    formated_data = []

    collist = []
    if isinstance(cols, int):
        collist.append(cols)
        cols = tuple(collist)

    for dvalue in data:
        nvalue = list(dvalue)
        if cols is not None:
            for i in cols:
                nvalue[i] = Paragraph(nvalue[i], style)
        formated_data.append(nvalue)

    return formated_data

class MyDocTemplate(BaseDocTemplate):
    "The document template used for all PDF documents."

    _invalidInitArgs = ('pageTemplates',)

    def __init__(self, conf, filename, **kw):
        frame_first_page = Frame(2.5 * cm, 2.5 * cm, 15 * cm, 25 * cm, id='first')
        frame_remaining_pages = Frame(2.5 * cm, 2.5 * cm, 16 * cm, 25 * cm, id='remaining')
        frame_last_page = Frame(2.5 * cm, 2.5 * cm, 15 * cm, 25 * cm, id='last')
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        firstpage_template = PageTemplate(id='first_page', frames=frame_first_page, onPage=self.on_first_page)
        mainpage_template = PageTemplate(id='remaining_pages', frames=frame_remaining_pages, onPage=self.on_remaining_pages)
        lastpage_template = PageTemplate(id='last_page', frames=frame_last_page, onPage=self.on_last_page)

        self.addPageTemplates([firstpage_template, mainpage_template, lastpage_template])
        
        self.rptsettings = conf.getReportSetting()
        
        #print(self.rptsettings)

    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            styleName = flowable.style.name
            if styleName[:7] == 'Heading':
                key = str(hash(flowable))
                self.canv.bookmarkPage(key)

                # Register TOC entries.
                level = int(styleName[7:])
                text = flowable.getPlainText()

                pageNum = self.page - 1
                # Try calling this with and without a key to test both
                # Entries of every second level will have links, others won't
                if level % 2 == 1:
                    self.notify('TOCEntry', (level, text, pageNum, key))
                else:
                    self.notify('TOCEntry', (level, text, pageNum))

                key = str(hash(flowable))
                canvas = self.canv
                canvas.setFont(myFontName, 12)

                # 在页眉生成格式为标题1的标题内容
                global gtext
                if text and level == 0:
                    gtext = text
                canvas.drawString(1.1 * inch, 11.10 * inch, gtext)

                # 生成标签
                canvas.bookmarkPage(key)
                canvas.addOutlineEntry(text, key, level=level, closed=0)

    def on_first_page(self, canvas, doc):
        canvas.saveState()

        # 封面字体及字体大小
        canvas.setFont(myFontName, 19)

        # 封面背景
        canvas.setFillColorRGB(0.9, 0.9, 0.9)
        canvas.setStrokeColorRGB(0.6, 0.6, 0.6)
        canvas.rect(0 * cm, 0.5 * cm, 25 * cm, 30 * cm, fill=1)

        # 封面上下彩线
        count = 0
        for i in range(0, 12):
            if count % 2 == 0:
                canvas.setStrokeColorRGB(0.6, 0.6, 0.6)
                # 设置线的粗细
                canvas.setLineWidth(1)
            else:
                canvas.setStrokeColorRGB(0.0, 0.3, 0.6)
                canvas.setLineWidth(3)

            # 绘制顶部线
            canvas.line(0 * inch, (0.0 + i * 0.025) * inch, 8.5 * inch, (0 + i * 0.025) * inch)
            # 绘制底部线
            canvas.line(0 * inch, (11.4 + i * 0.025) * inch, 8.5 * inch, (11.4 + i * 0.025) * inch)
            count = count + 1

        # 封面标题
        date_range = calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month)
        start_date = str(1)
        end_date = str(date_range[1])
        title = self.rptsettings['report_title']
        title1 = self.rptsettings['report_title1']
        if self.rptsettings['report_title2'] and self.rptsettings['report_title2'] != '':
            title2 = self.rptsettings['report_title2']
        else:
            title2 = '（' + year + '/' + month + '/' + start_date + '-' + year + '/' + month + '/' + end_date + '）'

        #print((8.3-(8.3/21.5)*title.__len__())/2)
        canvas.setFillColorRGB(0, 0.3, 0.6)
        canvas.setFont(myFontName, 28)
        # width = 8.3*inch
        canvas.drawString(((8.3-(8.3/21.5)*title.__len__())/2)*inch, 10 * inch, title)
        canvas.drawString(((8.3-(8.3/21.5)*title1.__len__())/2) * inch, 9.5 * inch, title1)
        canvas.setFillColorRGB(0, 0, 0)
        canvas.setFont(myFontName, 16)
        canvas.drawString(2.8 * inch, 9 * inch, title2)


        # 封面中间部分，图片和部分文字
        canvas.setFillColorRGB(0.0, 0.3, 0.6)
        canvas.setStrokeColorRGB(0.0, 0.3, 0.6)
        canvas.drawImage(self.rptsettings['cover_logo'], 0 * inch, 3.5 * inch, 600, 330)
        canvas.line(0 * inch, 8.1 * inch, 8.5 * inch, 8.1 * inch)
        canvas.line(0 * inch, 3.5 * inch, 8.5 * inch, 3.5 * inch)
        canvas.setFillColorRGB(0.6, 0.6, 0.6)
        canvas.drawString(0.5 * inch, 5 * inch, '集成技术解决方案')
        canvas.drawString(0.5 * inch, 4.7 * inch, '虚拟化、云计算和大数据')
        canvas.drawString(0.5 * inch, 4.4 * inch, '数据库高端运维服务')
        canvas.drawString(0.5 * inch, 4.1 * inch, '系统、网络与安全')

        # 封面右下角
        canvas.drawImage(self.rptsettings['company_logo'], 6.8 * inch, 0.75 * inch, 25, 25)
        canvas.setStrokeColorRGB(0, 0, 0)
        canvas.setFillColorRGB(0, 0.3, 0.6)
        canvas.setFont(myFontName, 12)
        canvas.drawString(7.2 * inch, 0.95 * inch, self.rptsettings['company_name_short'])
        canvas.setFont(myFontName, 11)
        canvas.drawString(7.2 * inch, 0.77 * inch, 'Vision-IT')
        canvas.setStrokeColorRGB(0, 0.3, 0.6)
        canvas.setFillColorRGB(0, 0, 0)
        canvas.setFont(myFontName, 10)
        canvas.drawString(6.2 * inch, 0.55 * inch, self.rptsettings['company_name'])
        canvas.drawString(6.4 * inch, 0.4 * inch, self.rptsettings['company_website'])
        canvas.setFont(myFontName, 18)
        canvas.setFillColorRGB(0, 0, 0)
        canvas.drawString(1.75 * inch, 3 * inch, '专业运维团队，24X7小时服务，让您更放心！')

        canvas.restoreState()

    def on_last_page(self, canvas, doc):
        canvas.saveState()

        # 封面字体及字体大小
        canvas.setFont(myFontName, 19)

        # 封面背景
        canvas.setFillColorRGB(0.9, 0.9, 0.9)
        canvas.setStrokeColorRGB(0.6, 0.6, 0.6)
        canvas.rect(0 * cm, 0.5 * cm, 25 * cm, 30 * cm, fill=1)

        # 封面中间部分，图片和部分文字
        for i in range(0, 25):
            if i % 2 == 0:
                canvas.setStrokeColorRGB(0.8, 0.8, 0.8)
            else:
                canvas.setStrokeColorRGB(0.8, 0.8, 0.8)

            canvas.setLineWidth((0.025 + 0.01 * i) * inch)
            canvas.line(0 * inch, (8 - (0.05 * i + 0.01 * i * (i + 1) / 2)) * inch, 8.5 * inch, (8 - (0.05 * i + 0.01 * i * (i + 1) / 2)) * inch)

        canvas.setStrokeColorRGB(0.0, 0.3, 0.6)
        canvas.setLineWidth(3)
        canvas.line(0 * inch, 8.1 * inch, 8.5 * inch, 8.1 * inch)
        canvas.line(0 * inch, 3.5 * inch, 8.5 * inch, 3.5 * inch)

        # 封面上下彩线
        count = 0
        for i in range(0, 12):
            if count % 2 == 0:
                canvas.setStrokeColorRGB(0.6, 0.6, 0.6)
                # 设置线的粗细
                canvas.setLineWidth(1)
            else:
                canvas.setStrokeColorRGB(0.0, 0.3, 0.6)
                canvas.setLineWidth(3)

            # 绘制顶部线
            canvas.line(0 * inch, (0.0 + i * 0.025) * inch, 8.5 * inch, (0 + i * 0.025) * inch)
            # 绘制底部线
            canvas.line(0 * inch, (11.4 + i * 0.025) * inch, 8.5 * inch, (11.4 + i * 0.025) * inch)
            count = count + 1

        # 封面右下角
        canvas.drawImage(self.rptsettings['company_logo'], 0.5 * inch, 1.25 * inch, 25, 25)
        canvas.setStrokeColorRGB(0, 0, 0)
        canvas.setFillColorRGB(0, 0.3, 0.6)
        canvas.setFont(myFontName, 12)
        canvas.drawString(0.9 * inch, 1.45 * inch, self.rptsettings['company_name_short'])
        canvas.setFont(myFontName, 11)
        canvas.drawString(0.9 * inch, 1.27 * inch, self.rptsettings['company_name_short_en'])
        canvas.setStrokeColorRGB(0, 0.3, 0.6)
        canvas.setFillColorRGB(0, 0, 0)
        canvas.setFont(myFontName, 12)
        canvas.drawString(0.5 * inch, 1.05 * inch, self.rptsettings['company_name'])
        canvas.setFont(myFontName, 8)
        canvas.drawString(0.5 * inch, 0.9 * inch, '网站：' + self.rptsettings['company_website'])
        canvas.drawString(0.5 * inch, 0.75 * inch, '地址：' + self.rptsettings['company_address'])
        canvas.drawString(0.5 * inch, 0.6 * inch, '电话：' + self.rptsettings['company_telephone'])

        BarCodes().genEan13Barcode(canvas, 6.5 * inch, 0.6 * inch, 50, 8)


        canvas.restoreState()


    def on_remaining_pages(self, canvas, doc):
        canvas.saveState()

        canvas.setFont(myFontName, 9)
        canvas.line(1 * inch, 1 * inch, 7.3 * inch, 1 * inch)
        canvas.line(1 * inch, 11 * inch, 7.3 * inch, 11 * inch)
        canvas.drawString(4 * inch, 0.75 * inch, "Page %d" % (doc.page - 1))

        canvas.restoreState()

    def set_content(self):
        # 设置目录索引等级，这里以设置为一级标题、二级标题、三级标题
#         print(self.rptsettings)
        if self.rptsettings['content_level'] and self.rptsettings['content_level'] != '':
            maxLevels = self.rptsettings['content_level']
        else:
            maxLevels = 3

        # Create styles to be used for document headers
        # on differnet levels.
        headerLevelStyles = []
        for i in range(maxLevels):
            headerLevelStyles.append(makeHeaderStyle(i))
            
        return maxLevels,headerLevelStyles


class OracleReport:
    """Test story with TOC and a cascaded header hierarchy.

    The story should contain exactly one table of contents that is
    immediatly followed by a list of of cascaded levels of header
    lines, each nested one level deeper than the previous one.

    Features to be visually confirmed by a human being are:

        1. TOC lines are indented in multiples of 1 cm.
        2. Wrapped TOC lines continue with additional 0.5 cm indentation.
        3. Only entries of every second level has links
        ...
    """

    def __init__(self,conf,filename):
        doc = MyDocTemplate(conf,filename)
        self.maxLevels,self.headerLevelStyles = doc.set_content()
        self.dbsettings = conf.getDatabaseSetting()
        self.rptsettings = conf.getReportSetting()
        self.pkgsettings = conf.getPackageSetting()
        
        self.doc = doc


    def makeFirstPart(self):
        story = []

        return story

    def makeAuthorPart(self):
        story = []
        # 换页，开始新内容
        # 使用内容模版开始写内容
        story.append(NextPageTemplate('remaining_pages'))
        story.append(PageBreak())
        story.append(Paragraph('版权信息', makeListTitleStyle()))
        for cprt in self.rptsettings['copyright']:
            story.append(Paragraph(cprt, makeBodyStyle()))

        story.append(Spacer(0, 0.5 * cm))
        story.append(Paragraph('文档属性', makeListTitleStyle()))
        data = [('文档属性', '内容')]
        data.extend([('文档名称', self.rptsettings['report_title'] + self.rptsettings['report_title1']),
                     ('文档版本号', self.rptsettings['report_version']),
                     ('文档状态', '正式巡检报告'),
                     ('文档特性', '自动化'),
                     ('生成日期', time.strftime('%Y-%m-%d', time.localtime(time.time())))])
        story.extend(makeTable(data, colwidth=(80, 364)))

        story.append(Spacer(0, 0.5 * cm))
        story.append(Paragraph('作者信息', makeListTitleStyle()))
        data = [('姓名', '公司', '职位', '邮箱', '电话')]
        data.extend([('陈英', '贵州维讯信息技术有限公司', '系统工程师', 'ychenid@live.com', '15285649896')])
        story.extend(makeTable(data, colwidth=(48, 136, 64, 116, 80)))

        return story

    def makeCopInfo(self):
        inPath=self.rptsettings['flowshape']
        story = []
        # 换页
        story.append(PageBreak())
        story.append(Paragraph('1. 故障响应流程', makeListTitleStyle()))
        inPath = inPath
        img = Image(0, 0, 450, 300, inPath)
        d = Drawing(300, 300)
        d.add(img)
#         d.translate(420, 0)
#         d.scale(2, 2)
#         d.rotate(0)
        story.append(d)

        story.append(Spacer(0, 1 * cm))
        story.append(Paragraph('2. 项目服务工程师', makeListTitleStyle()))
        data = [('姓名', '公司', '职位', '邮箱', '电话')]
        data.extend(self.rptsettings['author'])
        story.extend(makeTable(data, colwidth=(48, 136, 64, 116, 80)))

        story.append(Paragraph('3. 报告审核签署', makeListTitleStyle()))
        story.append(Spacer(0, 0.2 * cm))
        story.append(Preformatted('文档名称：' + self.rptsettings['report_title'] + self.rptsettings['report_title1'], makeBodyStyle()))
        story.append(Preformatted('副本数量：' + str(self.rptsettings['report_copy']) + '份', makeBodyStyle()))
        story.append(Preformatted('出版单位：' + str(self.rptsettings['company_name']), makeBodyStyle()))
        story.append(Preformatted('出版日期：' + time.strftime('%Y-%m-%d', time.localtime(time.time())), makeBodyStyle()))
        story.append(Spacer(0, 1.5 * cm))
        story.append(Preformatted(80 * str(' ') + '巡检人：_____________     日期：_____________' , makeBodyStyle()))
        story.append(Preformatted(80 * str(' ') + '审定人：_____________     日期：_____________' , makeBodyStyle()))

        return story

    def makeSignature(self):
        story = []
        # 换页
        story.append(PageBreak())


    def makeContentPart(self):
        # Create styles to be used for TOC entry lines
        # for headers on differnet levels.
        tocLevelStyles = []
        d, e = tableofcontents.delta, tableofcontents.epsilon
        for i in range(self.maxLevels):
            tocLevelStyles.append(makeTocHeaderStyle(i, d, e))

        # Build story.
        story = []

        # 生成目录
        story.append(PageBreak())
        story.append(Paragraph(self.rptsettings['content_name'], makeTitleStyle()))
        story.append(Spacer(0, 1 * cm))
        toc = tableofcontents.TableOfContents()
        toc.levelStyles = tocLevelStyles
        story.append(toc)

        return story

    def makeManagedResourcetPart(self):
        story = []
        # 换页，开始新内容
        story.append(PageBreak())
        story.append(Paragraph('1. 运维资源对象', self.headerLevelStyles[0]))
        i_count = 1
        data = [('编号', '实例名称', '业务名称', '数据库名', '主机', '数据库版本')]
        for db in self.dbsettings.values():
            data.extend([(i_count, db['instance_name'], db['dbtitle'], db['dbname'], db['host'], db['dbversion'])])
            i_count += 1

        story.extend(makeTable(data, title='表1 数据库资源对象', colwidth=(32, 64, 120, 64, 100, 70)))
        return story

    def makeDBSummaryPart(self):
        story = []
        # 换页，开始新内容
        story.append(PageBreak())
        story.append(Paragraph('2. 数据库运行状态概览', self.headerLevelStyles[0]))

        d = DrawShape()
        status_online = d.drawArrow(10, 20, 20, 90, 0, -15, colors.green)
        status_offline = d.drawArrow(10, 20, 20, -90, -20, -5, colors.red)
        resource_usage = d.drawBattery(25, 20, 0.05, colors.green)
        crossbox_failure = d.drawCrossbox(20, 20, 20, 0, 0, colors.red, colors.white)
        crossbox_success = d.drawCrossbox(20, 20, 20, 0, 0, colors.green, colors.green)

        alert_failure = d.drawAlert(20, 20, 20, 0, 0, 4, colors.red)
        alert_success = d.drawAlert(20, 20, 20, 0, 0, 0, colors.green)

        i_count = 1
        data = [('实例', '状态', '库', '监听', 'CPU', '内存', '磁盘', '日志', '表空间', '告警', '备份', 'OGG', 'DG')]
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            dbdata = ['', '', '', '', '', '', '', '', '', '', '', '', '']
            dbdata[0] = db['instance_name']

            try:
                inststatus = oracle.instance_status()
                dbstatus = oracle.database_status()

                if inststatus[0][3] == 'OPEN':
                    dbdata[1] = status_online
                else:
                    dbdata[1] = status_offline

                if dbstatus[0][2] == 'READ WRITE':
                    dbdata[2] = status_online
                else:
                    dbdata[2] = status_offline

                dbdata[3] = status_online

                dbdata[4] = '?'
                dbdata[5] = '?'
                dbdata[6] = '?'
                dbdata[7] = '?'
                dbdata[8] = '?'
                dbdata[9] = '?'
                dbdata[10] = '?'
                dbdata[11] = '?'
                dbdata[12] = '?'
            except Exception:
                dbdata[1] = status_offline
                dbdata[2] = status_offline
                dbdata[3] = status_offline
                dbdata[4] = '?'
                dbdata[5] = '?'
                dbdata[6] = '?'
                dbdata[7] = '?'
                dbdata[8] = '?'
                dbdata[9] = '?'
                dbdata[10] = '?'
                dbdata[11] = '?'
                dbdata[12] = '?'

            data.extend([(dbdata[0], dbdata[1], dbdata[2], dbdata[3], dbdata[4], dbdata[5], dbdata[6], dbdata[7], dbdata[8], dbdata[9], dbdata[10], dbdata[11], dbdata[12])])
            i_count += 1

#         for db in self.dbsettings.values():
#             data.extend([('prod1',status_online,status_online,status_offline,resource_usage,resource_usage,resource_usage,
#                           status_online,status_online,alert_failure,crossbox_failure,status_online,status_online)])
#             i_count += 1
        story.extend(makeTable(data, title='表2.1 数据库资源状态', colwidth=(56, 32, 32, 32, 32, 32, 32, 32, 40, 32, 32, 32, 32)))


        i_number = 1
        for db in self.dbsettings.values():
            hostmetric = HostMetric(db['host'], db['host_username'], db['host_password'], db['host_port'], self.pkgsettings['syslogin'])

            #print(hostmetric)
            story.append(Paragraph('(' + str(i_number) + ')' + db['dbtitle'] + '服务器当前状态', makeBodyStyle()))
            title = ''

            # 获取服务器负载信息
            data = [['Server', '1 mins', '5 mins', '15 mins']]
            try:
                results = hostmetric.get_load_metric()
                results = [db['dbtitle'], results[0][0], results[0][1], results[0][2]]
                note = ''
            except Exception:
                results = ['', '', '', '']
                note = '注释：服务器连接异常，请检查服务器运行是否正常。'

            data.append(results)

            story.append(Paragraph('>> 负载', makeBodyStyle()))
            story.extend(makeTable(data, title, note, colwidth=(80, 125, 120, 120)))

            # 获取CPU信息
            data = [['Server', 'CPU Used Ratio']]
            try:
                resutls = hostmetric.get_cpu_metric()

                results = [db['dbtitle'], resutls]
                note = ''
            except Exception:
                results = ['', '']
                note = '注释：服务器连接异常，请检查服务器运行是否正常。'

            data.append(results)
            story.append(Paragraph('>> CPU', makeBodyStyle()))
            story.extend(makeTable(data, title, note, colwidth=(80, 365)))

            # 获取内存信息
            data = [['Server', 'MemTotal', 'MemFree', 'Mem Used Rate']]
            try:
                results = hostmetric.get_mem_metric()
                results = [db['dbtitle'], results['MemTotal'], results['MemFree'], results['MemUsedRate']]
                note = ''
            except Exception:
                results = ['', '', '', '']
                note = '注释：服务器连接异常，请检查服务器运行是否正常。'

            data.append(results)
            story.append(Paragraph('>> 内存', makeBodyStyle()))
            story.extend(makeTable(data, title, note, colwidth=(80, 120, 120, 125)))

            # 获取磁盘使用信息
            data = [['FileSystem', 'Size', 'Used', 'Avail', 'Use%', 'Mounted on']]
            try:
                results = hostmetric.get_disk_metric()
                results = results[1:]
                note = ''
            except Exception:
                results = ['', '', '', '', '', '']
                note = '注释：服务器连接异常，请检查服务器运行是否正常。'

            data.extend(results)

            story.append(Paragraph('>> 磁盘', makeBodyStyle()))
            story.extend(makeTable(data, title, note, colwidth=(220, 32, 32, 32, 48, 96)))

            # 获取网卡使用信息
            data = [['Face', 'Bytes', 'Drop']]
            try:
                results = hostmetric.get_net_metric()
                results = results[1:]
                note = ''
            except Exception:
                results = ['', '', '']
                note = '注释：服务器连接异常，请检查服务器运行是否正常。'

            data.extend(results)
            story.append(Paragraph('>> 网络', makeBodyStyle()))
            story.extend(makeTable(data, title, note, colwidth=(100, 175, 175)))

            i_number += 1

        return story

    def makeStoragePart(self):
        story = []
        story.append(PageBreak())
        story.append(Paragraph('3. 数据库存储结构', self.headerLevelStyles[0]))

        i_number = 1

        story.append(Paragraph('3.1. 数据库物理存储结构', self.headerLevelStyles[1]))
        story.append(Paragraph('3.1.1 控制文件', self.headerLevelStyles[2]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '表3.' + str(i_number) + ' ' + db['dbtitle'] + '控制文件及副本'
            data = [('STATUS', 'NAME', 'SIZE')]

            try:
                results = oracle.controlfile()
                i_count = 0
                for i in results:
                    if i[0] is None:
                        i_count = i_count + 1
                note = '注释：' + db['dbtitle'] + '共有' + str(len(results)) + '个数据控制文件，其中有效文件有' + str(i_count) + '个，无效文件有' + str(len(results) - i_count) + '个。'
            except Exception:
                results = [('', '', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            results = wrapTable(results, cols=(1))
            data.extend(results)


            story.extend(makeTable(data, title, note, colwidth=(64, 300, 80)))
            i_number += 1

        story.append(Paragraph('3.1.2 日志文件', self.headerLevelStyles[2]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '表3.' + str(i_number) + ' ' + db['dbtitle'] + '日志文件'
            data = [('GROUP', 'STATUS', 'TYPE', 'MEMBER')]

            try:
                results = oracle.logfile()
                logcount = oracle.logcount()

                i_count = 0
                for i in results:
                    if i[1] is None:
                        i_count = i_count + 1
                note = '注释：' + db['dbtitle'] + '共有' + str(logcount[0][0]) + '日志组，' + str(len(results)) + '个日志文件文件，其中有效文件有' + str(i_count) + '个，无效文件有' + str(len(results) - i_count) + '个。'
            except Exception:
                results = [('', '', '', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            results = wrapTable(results, cols=(3))
            data.extend(results)


            story.extend(makeTable(data, title, note, colwidth=(64, 80, 80, 220)))
            i_number += 1

        story.append(Paragraph('3.1.3 数据文件', self.headerLevelStyles[2]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '表3.' + str(i_number) + ' ' + db['dbtitle'] + '数据文件存储结构'
            data = [('ID', 'NAME', 'STATUS', 'SIZE', 'MAXSIZE', 'EXTENSIBLE')]

            try:
                results = oracle.datafile()
                i_count = 0
                for i in results:
                    if i[2] == 'ONLINE' or i[2] == 'SYSTEM':
                        i_count = i_count + 1
                note = '注释：' + db['dbtitle'] + '共有' + str(len(results)) + '个数据文件，其中在线文件有' + str(i_count) + '个，离线文件有' + str(len(results) - i_count) + '个。'
            except Exception:
                results = [('', '', '', '', '', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            results = wrapTable(results, cols=(1))
            data.extend(results)


            story.extend(makeTable(data, title, note, colwidth=(32, 150, 64, 64, 64, 81)))
            i_number += 1

        story.append(Paragraph('3.2. 数据库逻辑存储结构', self.headerLevelStyles[1]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '表3.' + str(i_number) + ' ' + db['dbtitle'] + '表空间及使用情况'
            data = [('NAME', 'STATUS', 'TOTAL', 'USED', 'FREE', 'USEDPCT')]

            try:
                results = oracle.tablespace()
                i_count = 0
                for i in results:
                    if i[1] == 'ONLINE':
                        i_count = i_count + 1
                note = '注释：' + db['dbtitle'] + '共有' + str(len(results)) + '个表空间，其中在线有' + str(i_count) + '个，离线有' + str(len(results) - i_count) + '个。'
            except Exception:
                results = [('', '', '', '', '', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            results = wrapTable(results, cols=(0))
            data.extend(results)
            story.extend(makeTable(data, title, note, colwidth=(118, 81, 64, 64, 64, 64)))
            i_number += 1
        return story

    def makeDBObjectPart(self):
        story = []
        story.append(PageBreak())
        story.append(Paragraph('4. 数据库对象监测', self.headerLevelStyles[0]))
        story.append(Paragraph('4.1 数据库无效对象', self.headerLevelStyles[1]))
        i_number = 1
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '表4.' + str(i_number) + ' ' + db['dbtitle'] + '数据库无效对象'

            data = [('OWER', 'NAME', 'TYPE', 'STATUS')]

            try:
                results = oracle.invalid_objects()
                note = '注释：' + db['dbtitle'] + '共有' + str(len(results)) + '个无效对象。'
            except Exception:
                results = [('', '', '', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            results = wrapTable(results, cols=(0))
            data.extend(results)
            story.extend(makeTable(data, title, note, colwidth=(90, 164, 100, 100)))
            i_number += 1

        story.append(Paragraph('4.2. 数据库无效触发器', self.headerLevelStyles[1]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '表4.' + str(i_number) + ' ' + db['dbtitle'] + '数据库无效触发器'

            data = [('OWER', 'TRIGGER', 'TABLE', 'STATUS')]
            try:
                results = oracle.disabled_triggers()
                note = '注释：' + db['dbtitle'] + '共有' + str(len(results)) + '个无效触发器。'
            except Exception:
                results = [('', '', '', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            results = wrapTable(results, cols=(0))
            data.extend(results)
            story.extend(makeTable(data, title, note, colwidth=(90, 164, 100, 100)))
            i_number += 1

        story.append(Paragraph('4.3. 数据库无效索引', self.headerLevelStyles[1]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])

            title = '表4.' + str(i_number) + ' ' + db['dbtitle'] + '无效索引'

            data = [('OWER','NAME', 'TABLE', 'TABLESPACE', 'STATUS')]

            try:
                results = oracle.invalid_indexes()
                note = '注释：' + db['dbtitle'] + '共有' + str(len(results)) + '个无效索引。'
            except Exception:
                results = [('', '', '', '','')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            results = wrapTable(results, cols=(0,2))
            data.extend(results)
            story.extend(makeTable(data, title, note, colwidth=(80,90, 104, 80, 80)))
            i_number += 1

        story.append(Paragraph('4.4. 数据库无效约束', self.headerLevelStyles[1]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])

            title = '表4.' + str(i_number) + ' ' + db['dbtitle'] + '无效约束'

            data = [('OWER', 'NAME', 'TABLE', 'TYPE', 'STATUS')]
            try:
                results = oracle.disabled_constraints()
                note = '注释：' + db['dbtitle'] + '共有' + str(len(results)) + '个无效约束。'
            except Exception:
                results = [('', '', '', '', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            results = wrapTable(results, cols=(0, 1))
            data.extend(results)
            story.extend(makeTable(data, title, note, colwidth=(80, 84, 80, 100, 100)))
            i_number += 1

        story.append(Paragraph('4.5. 数据库组件对象', self.headerLevelStyles[1]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])

            title = '表4.' + str(i_number) + ' ' + db['dbtitle'] + '数据库组件'

            data = [('ID', 'NAME', 'VERSION', 'STATUS')]
            try:
                results = oracle.register()
                note = '注释：' + db['dbtitle'] + '共有' + str(len(results)) + '个组件。'
            except Exception:
                results = [('', '', '', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            results = wrapTable(results, cols=(0, 1))
            data.extend(results)
            story.extend(makeTable(data, title, note, colwidth=(80, 134, 130, 100)))
            i_number += 1

        return story

    def makePerformancePart(self):
        story = []
        story.append(PageBreak())
        story.append(Paragraph('5. 数据库性能分析', self.headerLevelStyles[0]))
        i_number = 1

        story.append(Paragraph('5.1 SQL性能统计', self.headerLevelStyles[1]))

        story.append(Paragraph('5.1.1 最近CPU消耗最高的前10条SQL', self.headerLevelStyles[2]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '表5.' + str(i_number) + ' ' + db['dbtitle'] + '数据库CPU消耗之SQL'

            data = [('SQL_ID', 'SQL_TEXT', 'CPU_TIME', 'DISK_READ_TIME', 'COUNTS')]

            try:
                results = oracle.sql_cpu_top_hist()
                note = '注释：以上列出的是最近消耗CPU资源排名前十的SQL语句'
            except Exception:
                results = [('', '', '', '', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            results = wrapTable(results, cols=(1))
            data.extend(results)
            story.extend(makeTable(data, title, note, colwidth=(64, 178, 64, 100, 48)))
            i_number += 1

        story.append(Paragraph('5.1.2 最近物理读消耗最高的前10条SQL', self.headerLevelStyles[2]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '表5.' + str(i_number) + ' ' + db['dbtitle'] + '数据库IO消耗之SQL'

            data = [('SQL_ID', 'SQL_TEXT', 'DISK_GETS_TIME', 'CPU_TIME', 'COUNTS')]

            try:
                results = oracle.sql_disk_top_hist()
                note = '注释：以上列出的是最近消耗IO资源排名前十的SQL语句'
            except Exception:
                results = [('', '', '', '', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            results = wrapTable(results, cols=(1))
            data.extend(results)
            story.extend(makeTable(data, title, note, colwidth=(64, 178, 84, 80, 48)))
            i_number += 1

        story.append(Paragraph('5.1.3 最近逻辑读消耗最高的前10条SQL', self.headerLevelStyles[2]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '表5.' + str(i_number) + ' ' + db['dbtitle'] + '数据库逻辑读消耗之SQL'

            data = [('SQL_ID', 'SQL_TEXT', 'BUFFER_GETS_TIME', 'CPU_TIME', 'COUNTS')]

            try:
                results = oracle.sql_buffer_top_hist()
                note = '注释：以上列出的是最近逻辑读资源消耗排名前十的SQL语句'
            except Exception:
                results = [('', '', '', '', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            results = wrapTable(results, cols=(1))
            data.extend(results)
            story.extend(makeTable(data, title, note, colwidth=(64, 178, 84, 80, 48)))
            i_number += 1

        story.append(Paragraph('5.1.4 最近物执行次数最多的前10条SQL', self.headerLevelStyles[2]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '表5.' + str(i_number) + ' ' + db['dbtitle'] + '数据库SQL执行次数统计'

            data = [('SQL_ID', 'SQL_TEXT', 'EXECUTIONS', 'CPU_TIME', 'COUNTS')]

            try:
                results = oracle.sql_executions_top_hist()
                note = '注释：以上列出的是最近消执行次数排名前十的SQL语句'
            except Exception:
                results = [('', '', '', '', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            results = wrapTable(results, cols=(1))
            data.extend(results)
            story.extend(makeTable(data, title, note, colwidth=(64, 178, 84, 80, 48)))
            i_number += 1

        story.append(Paragraph('5.1.5 最近排序消耗最高的前10条SQL', self.headerLevelStyles[2]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '表5.' + str(i_number) + ' ' + db['dbtitle'] + '数据库SQL排序资源统计'

            data = [('SQL_ID', 'SQL_TEXT', 'SORTS', 'CPU_TIME', 'COUNTS')]

            try:
                results = oracle.sql_sorts_top_hist()
                note = '注释：以上列出的是最近排序资源消耗排名前十的SQL语句'
            except Exception:
                results = [('', '', '', '', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            results = wrapTable(results, cols=(1))
            data.extend(results)
            story.extend(makeTable(data, title, note, colwidth=(64, 178, 84, 80, 48)))
            i_number += 1

        story.append(PageBreak())
        story.append(Paragraph('5.2 日志增量统计', self.headerLevelStyles[1]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '图5.' + str(i_number) + ' ' + db['dbtitle'] + '数据库日志增长统计'

            ptitle = 'Log Increase'
            xlabel = 'Date'
            ylabel = 'Log Size(G)'
            try:
                results = oracle.log_increase()

                if len(results) > 30:
                    results = results[-30:]

                data = []
                date = []

                for i in results:
                    data.append(i[1])
                    date.append(i[0])
                note = '注释：上图为数据库每日日志增长量。'
            except Exception:
                data = []
                date = []
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            story.append(plot_curve(date, data, ptitle, xlabel, ylabel))
            story.append(Paragraph(title, makeTableTitleStyle()))
            story.append(Paragraph(note, makeBodyStyle()))

            i_number += 1

        story.append(Paragraph('5.3 数据库关键指标分析', self.headerLevelStyles[1]))
        story.append(Paragraph('5.3.1 Buffer Cache命中率', self.headerLevelStyles[2]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '图5.' + str(i_number) + ' ' + db['dbtitle'] + 'Buffer Cache命中率'

            ptitle = 'Buffer Cache Hit Ratio'
            xlabel = ''
            ylabel = 'Ratio(%)'
            try:
                results = oracle.buffer_hit_hist()

                if len(results) > 30:
                    results = results[-30:]

                data = []
                date = []

                for i in results:
                    data.append(i[3])
                    date.append(i[0])
                note = '注释：上图为数据库最近Buffer Cache命中率情况，命中率越高，表示缓存在内存中的数据使用效率越高，当改值小于95%时，物理IO等待可能会出现，要分析该命中率低的原因。'
            except Exception:
                data = []
                date = []
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            story.append(plot_curve(date, data, ptitle, xlabel, ylabel))
            story.append(Paragraph(title, makeTableTitleStyle()))
            story.append(Paragraph(note, makeBodyStyle()))

            i_number += 1

        story.append(Paragraph('5.3.2 Library Cache命中率', self.headerLevelStyles[2]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '图5.' + str(i_number) + ' ' + db['dbtitle'] + 'Library Cache命中率'

            ptitle = 'Library Cache Hit Ratio'
            xlabel = ''
            ylabel = 'Ratio(%)'
            try:
                results = oracle.libraycache_hit_hist()

                if len(results) > 30:
                    results = results[-30:]

                data = []
                date = []

                for i in results:
                    data.append(i[3])
                    date.append(i[0])
                note = '注释：上图为数据库Library Cache命中率。这个比例通常应该保持在90%以上，否则就是库缓存太小或没有使用绑定变量。'
            except Exception:
                data = []
                date = []
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            story.append(plot_curve(date, data, ptitle, xlabel, ylabel))
            story.append(Paragraph(title, makeTableTitleStyle()))
            story.append(Paragraph(note, makeBodyStyle()))

            i_number += 1

        story.append(Paragraph('5.3.3 软解析率', self.headerLevelStyles[2]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '图5.' + str(i_number) + ' ' + db['dbtitle'] + '软解析率'

            ptitle = 'Soft Parse Ratio'
            xlabel = ''
            ylabel = 'Ration(%)'
            try:
                results = oracle.soft_parse_hist()

                if len(results) > 30:
                    results = results[-30:]

                data = []
                date = []

                for i in results:
                    data.append(i[3])
                    date.append(i[0])
                note = '注释：上图为数据库软解析率。这个值小于<95%说明硬解析有点多，需要注意。如果低于80%，执行计划的共享就出了严重问题，解决方法当然还是加大库缓存或使用绑定变量。'
            except Exception:
                data = []
                date = []
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            story.append(plot_curve(date, data, ptitle, xlabel, ylabel))
            story.append(Paragraph(title, makeTableTitleStyle()))
            story.append(Paragraph(note, makeBodyStyle()))

            i_number += 1

        story.append(Paragraph('5.3.4 内存排序率', self.headerLevelStyles[2]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '图5.' + str(i_number) + ' ' + db['dbtitle'] + '内存排序率'

            ptitle = 'Memory Sorts Ratio'
            xlabel = ''
            ylabel = 'Ratio'
            try:
                results = oracle.memory_sort_hist()

                if len(results) > 30:
                    results = results[-30:]

                data = []
                date = []

                for i in results:
                    data.append(i[3])
                    date.append(i[0])
                note = '注释：上图为数据库内存排序率。'
            except Exception:
                data = []
                date = []
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            story.append(plot_curve(date, data, ptitle, xlabel, ylabel))
            story.append(Paragraph(title, makeTableTitleStyle()))
            story.append(Paragraph(note, makeBodyStyle()))

            i_number += 1


        story.append(Paragraph('5.4 数据库等待与事件分析', self.headerLevelStyles[1]))
        story.append(Paragraph('5.4.1 数据库等待（按等待类划分）', self.headerLevelStyles[2]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '表5.' + str(i_number) + ' ' + db['dbtitle'] + '数据库排名前十的等待（等待类）'

            data = [('WAIT_CLASS', 'TOTAL_WAITS')]

            try:
                results = oracle.wait_class_hist()
                note = '注释：以上列出的是排名前十的等待事件。'
            except Exception:
                results = [('', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            results = wrapTable(results, cols=(0))
            data.extend(results)
            story.extend(makeTable(data, title, note, colwidth=(354, 100)))
            i_number += 1

        story.append(Paragraph('5.4.2 数据库等待（按事件划分）', self.headerLevelStyles[2]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '表5.' + str(i_number) + ' ' + db['dbtitle'] + '数据库排名前20的等待（事件）'

            data = [('EVENT_NAME', 'TOTAL_WAITS')]

            try:
                results = oracle.event_top_hist()
                note = '注释：以上列出的是排名前20的等待事件。'
            except Exception:
                results = [('', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            results = wrapTable(results, cols=(0))
            data.extend(results)
            story.extend(makeTable(data, title, note, colwidth=(354, 100)))
            i_number += 1

        story.append(Paragraph('5.5 数据库undo使用统计', self.headerLevelStyles[1]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '图5.' + str(i_number) + ' ' + db['dbtitle'] + '数据库undo使用情况'

            ptitle = 'Undo Usage'
            xlabel = ''
            ylabel = 'Number Of Blocks'
            try:
                results = oracle.undo_usage_hist()

                if len(results) > 30:
                    results = results[-30:]

                date = []
                activeblks = []
                unexpiredblks = []
                expiredblks = []
                for i in results:
                    date.append(i[0])
                    activeblks.append(i[1])
                    unexpiredblks.append(i[2])
                    expiredblks.append(i[3])
                note = '注释：上图为数据库最近Undo使用情况，其中横坐标表示收集数据的事件，纵坐标表示块的数量，activeblks表示正在使用的undo块，unexpiredblks表示占用时间在undo rentention以内的undo块。根据Undo使用情况来对其大小进行适当调整，满足事务需要。'
            except Exception:
                activeblks = []
                unexpiredblks = []
                expiredblks = []
                date = []
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            plt.figure(figsize=(20, 5))
            plt.plot([], [], color='m', label='activeblks')
            plt.plot([], [], color='c', label='unexpiredblks')
            plt.plot([], [], color='r', label='expiredblks')
            plt.stackplot(date, [activeblks, unexpiredblks, expiredblks], colors=['m', 'c', 'r'])

            plt.title('Undo Usage')
            plt.xlabel('Date')
            plt.ylabel('Number of Blks')
            plt.gcf().autofmt_xdate()
            plt.legend()

            imgdata = io.BytesIO()
            plt.savefig(imgdata, format='png')
            imgdata.seek(0)  # rewind the data

            img = platImage(imgdata, 600, 180)

            story.append(img)
            story.append(Paragraph(title, makeTableTitleStyle()))
            story.append(Paragraph(note, makeBodyStyle()))

            i_number += 1

        story.append(Paragraph('5.6 数据库总体性能', self.headerLevelStyles[1]))
        story.append(Paragraph('5.6.1 数据库负载情况', self.headerLevelStyles[2]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '图5.' + str(i_number) + ' ' + db['dbtitle'] + '数据库负载'

            ptitle = 'DB LOAD'
            xlabel = 'Date'
            ylabel = ''
            try:
                results = oracle.db_load_hist()

                if len(results) > 30:
                    results = results[-30:]

                data = []
                date = []

                for i in results:
                    data.append(i[1])
                    date.append(i[0])
                note = '注释：上图为数据库负载。'
            except Exception:
                data = []
                date = []
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            story.append(plot_curve(date, data, ptitle, xlabel, ylabel))
            story.append(Paragraph(title, makeTableTitleStyle()))
            story.append(Paragraph(note, makeBodyStyle()))

            i_number += 1

        story.append(Paragraph('5.6.2 数据库CPU使用情况', self.headerLevelStyles[2]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            title = '图5.' + str(i_number) + ' ' + db['dbtitle'] + 'CPU使用率'

            ptitle = 'CPU Usage Ratio'
            xlabel = 'Date'
            ylabel = 'Ratio'
            try:
                results = oracle.cpu_usage_hist()

                if len(results) > 30:
                    results = results[-30:]

                data = []
                date = []

                for i in results:
                    data.append(i[6])
                    date.append(i[2])
                note = '注释：上图为数据库CPU使用率。'
            except Exception:
                data = []
                date = []
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            story.append(plot_curve(date, data, ptitle, xlabel, ylabel))
            story.append(Paragraph(title, makeTableTitleStyle()))
            story.append(Paragraph(note, makeBodyStyle()))

            i_number += 1


        return story


    def makeBackupPart(self):
        story = []
        story.append(PageBreak())

        i_number = 1
        story.append(Paragraph('6. 数据库备份监测', self.headerLevelStyles[0]))
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])

            title = '表6.' + str(i_number) + ' ' + db['dbtitle'] + '数据库物理备份（RMAN）'
            data = [('DATABASE', 'TYPE', 'STATUS', 'ELAPSEDTIME', 'STARTTIME', 'INPUT_GB', 'OUTPUT_GB')]
            try:
                results = oracle.rman_backup()

                icount = 0

                for i in results:
                    if i[2] == 'COMPLETED':
                        icount += 1
                note = '注释：' + db['dbtitle'] + '最近1个月共有' + str(len(results)) + '次备份。其中成功备份' + str(icount) + '次, 失败备份' + str(len(results) - icount) + '次。'
            except Exception as e:
                print(e)
                results = [('', '', '', '', '', '', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            if len(results) > 20:
                results = results[0:10] + [('...','...','...','...','...','...','...')] + results[-10:]

            results = wrapTable(results)
            data.extend(results)
            story.extend(makeTable(data, title, note, colwidth=(48, 64, 67, 64, 83, 64, 64)))

            i_number += 1
            title = '表6.' + str(i_number) + ' ' + db['dbtitle'] + '数据库RMAN备份集'
            data = [('SET', 'TYPE', 'STATUS', 'STARTTIME', 'ELAPSED', 'SIZE', 'PATH')]
            try:
                results = oracle.rman_backupset()
                icount = 0
                for i in results:
                    if i[2] == 'AVAILABLE':
                        icount += 1
                note = '注释：' + db['dbtitle'] + '最近一个月共有' + str(len(results)) + '个备份集。其中可用备份集' + str(icount) + '个, 不可用备份' + str(len(results) - icount) + '个。'
            except Exception as e:
                print(e)
                results = [('', '', '', '', '', '', '')]
                note = '注释：数据库连接异常，无法获取相关信息，重试之前请保证数据库连接正常。'

            if len(results) > 20:
                results = results[0:10] + [('...','...','...','...','...','...','...')] + results[-10:]
            results = wrapTable(results, cols=(6))
            data.extend(results)
            story.extend(makeTable(data, title, note, colwidth=(32, 32, 56, 88, 61, 32, 154)))

            i_number += 1

        return story

    def makeCurrentStatus(self):
        pass

    def makeLastPart(self):
        # 生产最后一页封面
        story = []
        story.append(NextPageTemplate('last_page'))
        story.append(PageBreak())
        story.append(Spacer(0, 0 * cm))

        return story


    def run(self, mode=None):
        # 添加文章各个部分
        story = []
        story.extend(self.makeFirstPart())
        story.extend(self.makeAuthorPart())
        story.extend(self.makeCopInfo())
        story.extend(self.makeContentPart())
        story.extend(self.makeManagedResourcetPart())
        story.extend(self.makeDBSummaryPart())
        if mode == 'month':
            story.extend(self.makeStoragePart())
            story.extend(self.makeDBObjectPart())
            story.extend(self.makePerformancePart())
            story.extend(self.makeBackupPart())

        if mode == 'now':
            story.append(self.makeCurrentStatus())

        story.extend(self.makeLastPart())

        # 创建pdf文档
        self.doc.multiBuild(story)
      


if __name__ == '__main__':
    from utils import rptlogging
    # 导入配置文件
    from config import settings
    import os,sys
    
#     print(sys.path)
    
    path=settings.path_settings['resource'] + 'myreport.pdf'
    myconf = settings.ReportSetting(settings.path_settings['config'] + 'dbreport_gs.json')
    
    pdf = OracleReport(myconf,filename=path)
    
    logger = rptlogging.rptlogger(settings.ReportSetting().getPackageSetting()['logfile'])
    logger.info('Start generating report of database based on pdf format...')
    
    pdf.run()
    
    logger.info("Create pdf format report file: " + '"' + os.path.basename(path) + '" successfully' + " and it is saved to " + '"' + path + '".')

