import cv2
import pyautogui as pg
import time
import os
import numpy as np
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def initialization():
    pg.FAILSAFE = True
    pg.PAUSE = 1
    script_dir = r'D:\Personal\Desktop\Python\Muou_Demo\photos\root'
    to_width, to_height = pg.size()
    logging.info(f"屏幕分辨率为: {to_width}x{to_height}")
    return script_dir


def load_image(ph_name, script_dir):
    image_path = os.path.join(script_dir, f'{ph_name}.png')
    logging.info(f"图片路径: {image_path}")

    if not os.path.exists(image_path):
        logging.warning(f"文件不存在: {image_path}")
        return None

    try:
        image = cv2.imread(image_path)
        if image is not None:
            logging.info(f"找到了,位于: {image.shape}")
            return image
        else:
            logging.warning("没找到.")
            return None
    except Exception as e:
        logging.error(f"加载图像时发生错误: {e}")
        return None


def locate_image_on_screen(template):
    screenshot = pg.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    threshold = 0.8
    if max_val >= threshold:
        h, w, _ = template.shape
        top_left = max_loc
        center = (top_left[0] + w // 2, top_left[1] + h // 2)
        logging.info(f"图像位于: {top_left}, 中心位置: {center}, 匹配度: {max_val:.2f}")
        return center
    else:
        logging.info("未在屏幕上找到图像")
        return None


def run_task(task_name, ph_names_offsets, script_dir):
    logging.info(f"开始执行任务: {task_name}")
    for ph_name, offset in ph_names_offsets:
        template = load_image(ph_name, script_dir)
        if template is None:
            continue  # 如果图像未找到，继续下一个
        attempt_count = 0
        while attempt_count < 100:
            center = locate_image_on_screen(template)
            if center:
                adjusted_center = (center[0] + offset[0], center[1] + offset[1])
                try:
                    pg.click(adjusted_center)
                    time.sleep(1)
                except Exception as e:
                    logging.error(f"点击时发生错误: {e}")
                break
            else:
                time.sleep(5)
                attempt_count += 1
        if attempt_count >= 100:
            logging.warning(f"未找到图像 {ph_name}，重试次数超过上限，跳过。")
    logging.info(f"任务 {task_name} 完成")


# 进行初始化
script_dir = initialization()

# 执行任务
anpei_offsets = [
    ('pdx', (0, 0)), ('dl', (0, 0)), ('ap', (0, 0)), ('txl', (0, 0)),
    ('znrs', (0, 5)), ('hmc', (0, 0)), ('lshmc', (0, 0)), ('ztdc', (60, 0)),
    ('xz', (0, 0)), ('pdx2', (0, 0)), ('tcdl', (0, 0))
]

wanwu_offsets = [
    ('pdx', (0, 0)), ('dl', (0, 0)), ('ww', (0, 0)), ('txl', (0, 0)),
    ('znrs', (0, 5)), ('hmc', (0, 0)), ('lshmc', (0, 0)), ('ztdc', (60, 0)),
    ('xz', (0, 0)), ('pdx2', (0, 0)), ('tcdl', (0, 0))
]

wansong_offsets = [
    ('pdx', (0, 0)), ('dl', (0, 0)), ('ws', (0, 0)), ('txl', (0, 0)),
    ('znrs', (0, 5)), ('hmc', (0, 0)), ('lshmc', (0, 0)), ('ztdc', (60, 0)),
    ('xz', (0, 0)), ('pdx2', (0, 0)), ('tcdl', (0, 0))
]

run_task("安配", anpei_offsets, script_dir)
run_task("万物", wanwu_offsets, script_dir)
run_task("万送", wansong_offsets, script_dir)

print("所有历史花名册下载完成")
