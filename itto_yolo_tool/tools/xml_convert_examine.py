import cv2
import numpy as np

def function(pic_path,txt_path,classnames):
    with open(pic_path, 'rb') as f:
            img_array = np.frombuffer(f.read(), dtype=np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    img_height, img_width = image.shape[:2]

    with open(txt_path, 'r') as f:
        lines = f.readlines()
    

    # 绘制每个标注
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 9:  # class_id + 8个坐标值
            print(f"{txt_path}内数据量不够，无法绘图")
            continue
        
        class_id = int(parts[0])
        points = list(map(float, parts[1:]))
        
        # 将归一化坐标转换为像素坐标
        pixel_points = []
        for i in range(0, len(points), 2):
            x = int(points[i] * img_width)
            y = int(points[i+1] * img_height)
            pixel_points.append((x, y))
        
        # 绘制四边形
        if len(pixel_points) == 4:
            # 绘制边框
            for i in range(4):
                cv2.line(image, pixel_points[i], pixel_points[(i+1)%4], (0, 255, 0), 2)
            
            # 绘制顶点
            for point in pixel_points:
                cv2.circle(image, point, 3, (0, 0, 255), -1)
            
            # 添加类别标签
            if(class_id < len(classnames) and class_id>=0):
                class_name = classnames[class_id]
            else:
                class_name = f"Class_{class_id}"
                print("存在未标注图片:",pic_path)
            cv2.putText(image, class_name, pixel_points[0], 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    
    # 显示图像
    cv2.imshow('YOLO Annotations', image)

    if cv2.waitKey(0) == ord("q"):
        cv2.destroyAllWindows()
        return False
    else:
        return True
