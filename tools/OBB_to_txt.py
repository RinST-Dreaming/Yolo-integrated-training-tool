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
                    
                    # 转换为YOLO格式 (归一化坐标)
                    x_center = (xmin + xmax) / 2 / width
                    y_center = (ymin + ymax) / 2 / height
                    bbox_width = (xmax - xmin) / width
                    bbox_height = (ymax - ymin) / height
                    
                    # 确保坐标在0-1范围内
                    x_center = max(0, min(1, x_center))
                    y_center = max(0, min(1, y_center))
                    bbox_width = max(0, min(1, bbox_width))
                    bbox_height = max(0, min(1, bbox_height))
                    
                    output_lines.append([classnum, x_center, y_center, bbox_width, bbox_height])

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
                        
                    angle_rad = math.radians(angle)
                    output_lines.append([classnum, cx_norm, cy_norm, w_norm, h_norm, angle_rad])

    with open(txt_path, 'w') as f:
        for ann in output_lines:
            if len(ann) <= 5:  # 常规边界框
                line = f"{int(ann[0])} {ann[1]:.6f} {ann[2]:.6f} {ann[3]:.6f} {ann[4]:.6f}\n"
            else:  # 旋转边界框
                values = [f"{v:.6f}" for v in ann[1:]]
                line = f"{int(ann[0])} " + " ".join(values) + "\n"
            f.write(line)

if __name__ == "__main__":
    function("1.xml","1.txt",["t","w"])