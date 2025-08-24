import xml.etree.ElementTree as ET
import math

def function(xml_path, txt_path, classnames):
    output_lines=[]

    if xml_path==None:
        with open(txt_path, 'w') as f:
            f.write("")
        return
    
    tree = ET.parse(xml_path)
    root = tree.getroot()

    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)

    for elem in root:
        if elem.tag == 'object':
            classnum=-1
            for subelem in elem:

                if subelem.tag == 'name':
                    if subelem.text in classnames:
                        classnum = classnames.index(subelem.text)

                elif subelem.tag == 'bndbox':
                    xmin, ymin, xmax, ymax = 0, 0, 0, 0
                    for subsub in subelem:
                        if subsub.tag == 'xmin':
                            xmin = float(subsub.text)
                        elif subsub.tag == 'ymin':
                            ymin = float(subsub.text)
                        elif subsub.tag == 'xmax':
                            xmax = float(subsub.text)
                        elif subsub.tag == 'ymax':
                            ymax = float(subsub.text)
                    
                    # 转换为4个边框点的坐标 (归一化)
                    x1 = xmin / width
                    y1 = ymin / height
                    x2 = xmax / width
                    y2 = ymin / height
                    x3 = xmax / width
                    y3 = ymax / height
                    x4 = xmin / width
                    y4 = ymax / height
                    
                    # 确保坐标在0-1范围内
                    x1 = max(0, min(1, x1))
                    y1 = max(0, min(1, y1))
                    x2 = max(0, min(1, x2))
                    y2 = max(0, min(1, y2))
                    x3 = max(0, min(1, x3))
                    y3 = max(0, min(1, y3))
                    x4 = max(0, min(1, x4))
                    y4 = max(0, min(1, y4))
                    
                    output_lines.append([classnum, x1, y1, x2, y2, x3, y3, x4, y4])

                elif subelem.tag == 'robndbox':
                    cx, cy, w, h, angle = 0, 0, 0, 0, 0
                    for subsub in subelem:
                        if subsub.tag == 'cx':
                            cx = float(subsub.text)
                        elif subsub.tag == 'cy':
                            cy = float(subsub.text)
                        elif subsub.tag == 'w':
                            w = float(subsub.text)
                        elif subsub.tag == 'h':
                            h = float(subsub.text)
                        elif subsub.tag == 'angle':
                            angle = float(subsub.text)
                        
                    # 归一化坐标
                    cx_norm = cx / width
                    cy_norm = cy / height
                    w_norm = w / width
                    h_norm = h / height
                    
                    # 计算旋转矩形的4个角点
                    angle_rad = math.radians(angle)
                    cos_a = math.cos(angle_rad)
                    sin_a = math.sin(angle_rad)
                    
                    # 相对于中心的偏移量
                    half_w = w_norm / 2
                    half_h = h_norm / 2
                    
                    # 计算4个角点的相对坐标
                    x1_rel = -half_w * cos_a - (-half_h) * sin_a
                    y1_rel = -half_w * sin_a + (-half_h) * cos_a
                    
                    x2_rel = half_w * cos_a - (-half_h) * sin_a
                    y2_rel = half_w * sin_a + (-half_h) * cos_a
                    
                    x3_rel = half_w * cos_a - half_h * sin_a
                    y3_rel = half_w * sin_a + half_h * cos_a
                    
                    x4_rel = -half_w * cos_a - half_h * sin_a
                    y4_rel = -half_w * sin_a + half_h * cos_a
                    
                    # 转换为绝对坐标
                    x1 = cx_norm + x1_rel
                    y1 = cy_norm + y1_rel
                    x2 = cx_norm + x2_rel
                    y2 = cy_norm + y2_rel
                    x3 = cx_norm + x3_rel
                    y3 = cy_norm + y3_rel
                    x4 = cx_norm + x4_rel
                    y4 = cy_norm + y4_rel
                    
                    # 确保坐标在0-1范围内
                    x1 = max(0, min(1, x1))
                    y1 = max(0, min(1, y1))
                    x2 = max(0, min(1, x2))
                    y2 = max(0, min(1, y2))
                    x3 = max(0, min(1, x3))
                    y3 = max(0, min(1, y3))
                    x4 = max(0, min(1, x4))
                    y4 = max(0, min(1, y4))
                    
                    output_lines.append([classnum, x1, y1, x2, y2, x3, y3, x4, y4])

    with open(txt_path, 'w') as f:
        for ann in output_lines:
            values = [f"{v:.10f}" for v in ann[1:]]
            line = f"{int(ann[0])} " + " ".join(values) + "\n"
            f.write(line)

if __name__ == "__main__":
    function("1.xml","1.txt",["t","w"])