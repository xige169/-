from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
import torch
from xueyuan import *

device = "cuda" if torch.cuda.is_available() else "cpu"

model_path = 'E:/Qwen2.5'
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype="auto",
).to(device)

tokenizer = AutoTokenizer.from_pretrained(model_path)

def Edge_driver():
    # 初始化 Edge 浏览器
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    return driver


def login(driver):
    #点击下拉式菜单
    while True:
        try:
            dropdown_input = driver.find_element(By.CSS_SELECTOR, '.el-select .el-input__inner')
            actions = ActionChains(driver)
            actions.move_to_element(dropdown_input).click().perform()
            break
        except Exception as e:
            print(f'下拉式菜单发生错误:{e}')
            time.sleep(1)
    #选择菜单内容
    while True:
        try:
            academy_xpath = '/html/body/div[2]/div[1]/div[1]/ul/li/span'
            academys_element = driver.find_elements('xpath', academy_xpath)

            found = False

            for academy in academys_element:
                if my_academy == academy.text:
                    academy.click()
                    found = True
                    break
            if not found:
                print('未找到匹配的学院，请检查学院是否输入正确...')
            else :
                break
        except Exception as e:
            print(f'学院选择发生错误,请稍后...')
            time.sleep(1)

    # 定位输入框并输入内容
    while True:
        try:
            input_box = driver.find_element("xpath", '/html/body/div[1]/div/div[2]/form/div[2]/div/div/input')
            input_box.clear()  # 清空输入框
            input_box.send_keys(my_id)  # 输入内容
            print("学号已成功输入")
            break
        except Exception as e:
            print(f"学号输入框定位失败,请稍后...")
            time.sleep(1)
    #输入姓名
    while True:
        try:
            input_box = driver.find_element("xpath", '/html/body/div[1]/div/div[2]/form/div[3]/div/div/input')
            input_box.clear()  # 清空输入框
            input_box.send_keys(my_name)  # 输入内容
            print("姓名已成功输入")
            break
        except Exception as e:
            print(f"姓名输入框定位失败,请稍后...")
            time.sleep(1)
    #点击登录
    while True:
        try:
            button = driver.find_element('xpath', '/html/body/div[1]/div/div[2]/form/div[4]/div/button')
            button.click()
            print('点击登录成功')
            time.sleep(1)
            # 检查是否存在错误提示信息
            error_message_xpath = '/html/body/div[5]/p'
            error_message = driver.find_elements('xpath', error_message_xpath)
            if error_message:
                print(f"登录失败，错误信息: {error_message[0].text}")
                print('请在网页手动输入登录信息')
            else:
                print("登录成功！")
            break
        except Exception as e:
            print(f"登录按钮定位失败,请稍后...")
            time.sleep(1)

    return None

def click_examine(driver):
    while True:
        # exam_button = None
        try:
            if examine == "24-25学年第二学期期末考试":
                exam_button = driver.find_element(By.CLASS_NAME, "box1")
            elif examine == "期末考试":
                exam_button = driver.find_element(By.CLASS_NAME, "box2")
            elif examine == "第七届国家安全知识竞赛":
                exam_button = driver.find_element(By.CLASS_NAME, "box3")

            # 确保找到按钮后点击
            if exam_button:
                exam_button.click()
                print(f"已成功点击: {examine}")
                break
        except Exception as e:
            print(f"等待考试项目加载...")
            time.sleep(1)  # 等待元素加载

    while True:
        confirm_button_xpath = '/html/body/div/div/div[3]/button'
        try:
            confirm_button = driver.find_element('xpath', confirm_button_xpath)
            if confirm_button:
                confirm_button.click()
                print('进入考试')
                break
        except:
            print('等待页面加载')
            time.sleep(1)

    return None



def use_model_answer_question(type_question,question,options_question):


    prompt = (
        f'回答以下题目\n'
        f'题目类型:{type_question}\n'
        f'题目:{question}\n'
        f'选项:{" ".join(opt.text for opt in options_question)}\n'
        f'请以下面的格式回答:\n'
        f'请直接给出答案，多选题的答案直接用空格分隔，例如：答案：A 或 答案：A B\n'
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=200)

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer_option = answer.split('\n')[6] #从ai的回复中提取出答案
    print(answer_option)
    return answer_option


def get_question_and_answer(driver):
    type_question=None
    while True:
        try:#                                        /html/body/div/div/div[4]/div[1]  /html/body/div/div/div[4]/div[1]
            element = driver.find_element('xpath', '/html/body/div/div/div[4]/div[1]')
            if '单选题' in element.text:
                type_question = '单选题'
            elif '多选题' in element.text:
                type_question = '多选题'
            elif '判断题' in element.text:
                type_question = '判断题'
            if type_question !=None:
                print(f'题目类型为{type_question}')
                break

        except:
            print('题目还没有加载出来,请稍后..')
            time.sleep(1)

    while True:
        try:#                                        /html/body/div/div/div[4]/div[2]/div  /html/body/div/div/div[4]/div[2]/div
            element = driver.find_element('xpath', '/html/body/div/div/div[4]/div[2]/div')
            question = element.text
            break
        except:
            print('题目还没有加载出来,请稍后..')
            time.sleep(1)

    options_question = None
    while True:
        try:
            if type_question == '单选题':
                options_question = driver.find_elements('xpath', '/html/body/div/div/div[4]/div[3]/div[1]/div/label/span[2]/div')
            elif type_question == '多选题':
                options_question = driver.find_elements('xpath', '/html/body/div/div/div[4]/div[3]/div[1]/div/div/label/span[2]/div')
            elif type_question == '判断题':
                options_question = driver.find_elements('xpath','/html/body/div/div/div[4]/div[3]/div[2]/div/label/span[2]')
            break
        except:
            print('题目还没有加载出来,请稍后..')
            time.sleep(1)

    print(f"({type_question})",end='')
    print(question)
    for idx, option in enumerate(options_question):
        print(f"{option.text}")

    answer_option = use_model_answer_question(type_question,question,options_question)
    # print(len(answer_option))
    answers = answer_option[3::1].split()
    if answers:
        while True:
            try:
                for answer in answers:
                    answer_index = ord(answer)-64
                    if type_question == '判断题':
                        option_button_xpath = f'/html/body/div/div/div[4]/div[3]/div[2]/div/label[{answer_index}]/span[1]/span'
                    elif type_question == '多选题':
                        option_button_xpath = f'/html/body/div/div/div[4]/div[3]/div[1]/div/div[{answer_index}]/label/span[1]/span'
                    elif type_question == '单选题':
                        option_button_xpath = f'/html/body/div/div/div[4]/div[3]/div[1]/div[{answer_index}]/label/span[1]/span'

                    option_button = driver.find_element('xpath',option_button_xpath)
                    option_button.click()
                #点击下一题
                next_question_button = driver.find_element('xpath', '/html/body/div/div/div[4]/button[2]')
                next_question_button.click()
                break
            except Exception as e:
                print(f'点击发生错误：{e}')
                time.sleep(1)
    else:
        print('回答无效，人类作答...')
        current_question = None
        while True:
            try:
                current_question = driver.find_element('xpath', '/html/body/div/div/div[4]/div[2]/div').text
                if current_question != question:
                    break
            except Exception as e:
                print(e)
    return None










if __name__=='__main__':
    driver = Edge_driver()
    try:
        #http://aqjy.hfut.edu.cn
        #https://www.mxdm6.com/
        driver.get("http://aqjy.hfut.edu.cn")
        login(driver)
        click_examine(driver)
        for page in range(50):
            get_question_and_answer(driver)

        input()
    except Exception as e:
        print(e)

    print('ok')
