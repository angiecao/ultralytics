import glob
import os
# xml文件的路径
xml_path = '/mnt/d/workspace/data/ZDSpassengerflow/'

#定义从xml获取信息的函数
def _read_anno(filename):

    import xml.etree.ElementTree as ET
    tree = ET.parse(filename)
    #获取宽w和高h
    a = tree.find('size')
    w,h = [int(a.find('width').text),
           int(a.find('height').text)]
    print(w,h)

    objects = []
    #这里是针对错误xml文件，图片的w和h都为0，这样的xml文件可以直接忽视，返回空列表
    if w == 0:
        return []
    #这里需要根据需要修改，因为我训练的目的是判断是否戴了头盔，因此从xml获取的name为none或者0的label都为0，其他的颜色或者1都为1
    for obj in tree.findall('object'):
        #获取name，我上边的实例图片中的红色区域
        name = obj.find('name').text
        #修改label，这里是不同数据集大融合的关键
        if name == 'head':
            label = 0
        elif name == 'blue_BH_badge':
            label = 1
        elif name == 'white_BH_badge':
            label = 2
        elif name == 'blue_XP_badge':
            label = 3
        elif name == 'white_XP_badge':
            label = 4
        elif name == 'black_XP_badge':
            label = 5
        #读取检测框的左上、右下角点的坐标
        bbox = obj.find('bndbox')
        x1, y1, x2, y2 = [float(bbox.find('xmin').text),
                          float(bbox.find('ymin').text),
                          float(bbox.find('xmax').text),
                          float(bbox.find('ymax').text)]
        #这里也很关键，yolov5需要中心点以及宽和高的标注信息，并且进行归一化，下边label后边的四个值即是归一化后保留4位有效数字的x，y，w，h
        obj_struct = [label,round((x1+x2)/(2.0*w),4), round((y1+y2)/(2.0*h),4), round((x2-x1)/(w),4),round((y2-y1)/(h),4)]
        print(obj_struct)

        objects.append(obj_struct)


    return objects
#接下来是写入txt文件中
if __name__ == '__main__':
    #定义一个空的字符串
    t = ''
    # txt文件存放的路径
    txt_path = "/mnt/d/workspace/data/ZDSpassengerflow/yolo/"
    #获取所有的xml文件路径
    allfilepath = []
    for file in os.listdir(xml_path):
        if file.endswith('.xml'):
            file = os.path.join(xml_path,file)
            allfilepath.append(file)
            # print(allfilepath)
        else:
            pass
     #生成需要的对应xml文件名的txt
    for file in allfilepath:
        print("file", file)
        #获取xml的文件名
        filename = file.split('/')[6]
        indexname = filename.split('.')[0]
        # print('indexname', indexname)
        result = _read_anno(file)
        # print('result', result)
        #跳过空列表
        if len(result)==0:
            continue
        #写入信息，注意每次循环结束都把t重新定义，result是一个二维列表（行数为目标个数，列对应label和位置信息），为了避免读取出错（还有一个原因是我菜），我们一个一个的写入。
        txtfile = open(os.path.join(txt_path,indexname+'.txt'), 'w')
        for line in result:
            for a in line:
                # print('a', a)
                t = t + str(a) + ' '
                # print('t', t)
                txtfile.writelines(t)
                t = ''
            txtfile.writelines('\n')
