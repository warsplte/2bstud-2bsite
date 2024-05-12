#!/usr/bin/env python
# 定義 Python 直譯器路徑，讓系統知道要用哪個 Python 直譯器執行這個程式
# -*- coding: utf-8 -*- 
# 指定檔案編碼為 UTF-8，可以支援多國語言
from __future__ import unicode_literals
# 確保在 Python 2 和 3 中使用 unicode 字串

AUTHOR = 'cd2024_2a'  # 設定作者姓名
SITENAME = '2a cd2024 評分網誌'  # 設定網站名稱
# 不要用文章所在目錄作為類別
USE_FOLDER_AS_CATEGORY = False  # 設定不使用資料夾名稱作為文章類別

#PATH = 'markdown'  # 設定 Markdown 檔案存放路徑，這裡先註解掉，因為稍後會動態設定

# 開始將組員的個別網誌目錄納入分組倉儲中 and skip copying .md file under pages directory
# 這段程式碼的目的是將所有組員的網誌文章整合到一個資料夾中
import os  # 導入 os 模組，用於處理檔案和目錄
import shutil  # 導入 shutil 模組，用於複製檔案

# Directories you want to include (手動處理)
#input_directories = ['markdown', 'g10/41123199/markdown'] 
# 這裡原本是手動設定要包含的網誌目錄，現在改用程式動態產生
# 以下採程式方法建立 input_directorie 數列內容

def get_student_id(directory):
    # 從目錄名稱中取得學號，例如從 "g10/41123199/markdown" 中取得 "41123199"
    print(directory)  # 印出正在處理的目錄名稱
    parts = directory.split("/")  # 將目錄名稱以 "/" 分割成多個部分
    if len(parts) > 1:  # 如果分割後有多個部分，表示目錄名稱包含學號
        return parts[1]  # 回傳第二個部分，也就是學號
    else:  # 否則回傳 None
        return None

def read_slug(file_path):
    # 讀取 Markdown 檔案中的 Slug，Slug 是用來產生文章網址的一部分
    with open(file_path, "r", encoding="utf-8") as file:  # 開啟檔案，指定編碼為 UTF-8
        lines = file.readlines()  # 讀取所有行
        if len(lines) >= 6:  # 如果檔案至少有 6 行，表示可能包含 Slug
            slug_line = lines[5].strip()  # 取得第 6 行，並去除前後空白
            if slug_line.startswith("Slug:"):  # 如果這一行的開頭是 "Slug:"
                return slug_line[6:].strip()  # 回傳 "Slug:" 之後的內容，並去除前後空白
    return None  # 如果沒有找到 Slug，回傳 None

def update_slug_and_filename(source_file, student_id):
    # 更新 Slug 和檔名，在 Slug 和檔名中加入學號
    with open(source_file, "r", encoding="utf-8") as file:  # 開啟檔案，指定編碼為 UTF-8
        lines = file.readlines()  # 讀取所有行
        if len(lines) >= 6:  # 如果檔案至少有 6 行，表示可能包含 Slug
            slug_line = lines[5].strip()  # 取得第 6 行，並去除前後空白
            if slug_line.startswith("Slug:"):  # 如果這一行的開頭是 "Slug:"
                slug = slug_line[6:].strip()  # 取得 "Slug:" 之後的內容，並去除前後空白
                # 針對 Slug 沒有納入學號者, 以下程是將強行置入
                if not slug.startswith(student_id + "_"):  # 如果 Slug 沒有以學號開頭
                    lines[5] = "Slug: " + str(student_id) + "_" + str(slug) + "\n"  # 將學號加入 Slug
                    with open(source_file, "w", encoding="utf-8") as file:  # 開啟檔案，指定編碼為 UTF-8，並以寫入模式開啟
                        file.writelines(lines)  # 將修改後的內容寫入檔案

    filename = os.path.basename(source_file)  # 取得檔名
    # 針對 .md 檔案並未在最前面加入學號, 以下程式將強行置入
    if not filename.startswith(student_id + "_"):  # 如果檔名沒有以學號開頭
        new_filename = str(student_id) + "_" + str(filename)  # 將學號加入檔名
        new_source_file = os.path.join(os.path.dirname(source_file), new_filename)  # 組合新的檔案路徑
        os.rename(source_file, new_source_file)  # 重新命名檔案
        return new_source_file  # 回傳新的檔案路徑
    return source_file  # 如果檔名已經包含學號，直接回傳原本的檔案路徑

# 開啟檔案
with open('./downloads/2b.txt', 'r', encoding='utf-8') as file:  # 開啟存放學生資料的檔案，指定編碼為 UTF-8
    # 讀取每一行
    lines = file.readlines()  # 讀取檔案中的每一行

# 初始化存放學生資料的字典
student_data = {}  # 建立一個空的字典，用來存放學生資料

# 迴圈處理每一行
for line in lines:  # 逐行處理檔案中的每一行
    # 將每一行以逗號分隔
    data = line.strip().split(',')  # 將每一行去除前後空白，並以逗號 "," 分割成多個部分
    # 將學生資料存入字典
    student_data[data[0]] = data[1:]  # 將第一個部分 (學號) 作為 key，其餘部分作為 value 存入字典

# 初始化存放沒有資料的學生學號的列表
no_data_students = []  # 建立一個空的列表，用來存放沒有資料的學生學號

# 初始化存放目錄的列表，第一個元素為 "markdown"
input_directories = ["markdown"]  # 建立一個列表，用來存放所有要包含的網誌目錄，第一個元素是 "markdown"

# 迴圈處理每位學生
for student_id, data in student_data.items():  # 逐一處理字典中的每位學生
    # 如果學生資料缺少第二行的 Github 帳號，將其學號加入沒有資料的學生學號的列表
    if len(data) < 2 or data[1] == '':  # 如果學生資料少於 2 個部分，或者第二個部分 (Github 帳號) 是空的
        no_data_students.append(student_id)  # 將學號加入 no_data_students 列表
    else:  # 否則
        # 若有 github 帳號資料，組合目錄名稱並加入目錄列表中
        if (data[1] != "None") and (student_id != "None"):  # 如果 Github 帳號和學號都不是 "None"
            #print("g" + str(data[1]) + "/" + str(student_id) + "/markdown")
            directory_name = "g" + str(data[1]) + "/" + str(student_id) + "/markdown"  # 組合目錄名稱
            # 只有該組員的目錄存在, 才納入網誌檔案數列
            if os.path.exists(directory_name):  # 如果這個目錄存在
                input_directories.append(directory_name)  # 將目錄名稱加入 input_directories 列表
#print(input_directories)  # 印出 input_directories 列表，這裡先註解掉

# 列印沒有資料的學生學號
'''
print("以下為沒有資料的學生學號：")
for student_id in no_data_students:
    print(student_id)

# 列印建立的目錄列表
print("\n建立的目錄列表為：")
print(input_directories)
'''
# 結束建立 input_directories 數列

# Temporary directory to store combined Markdown files
combined_directory = 'combined_markdown'  # 設定一個暫存目錄，用來存放所有組員的網誌文章

# Create the combined directory if it doesn't exist
if not os.path.exists(combined_directory):  # 如果這個目錄不存在
    os.makedirs(combined_directory)  # 建立目錄
else:  # 否則
    # Clean the existing content of the combined directory
    for root, dirs, files in os.walk(combined_directory):  # 逐一處理目錄中的所有檔案和子目錄
        for file in files:  # 逐一處理檔案
            os.remove(os.path.join(root, file))  # 刪除檔案
        for dir in dirs:  # 逐一處理子目錄
            shutil.rmtree(os.path.join(root, dir))  # 刪除子目錄

'''
沒有自動置入學員學號的檔案複製處理方式
# Copy Markdown files from input directories to the combined directory
for directory in input_directories:
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                # Check if the file is not under the "pages" subdirectory
                if "pages" not in root.split(os.path.sep):
                    source_file = os.path.join(root, file)
                    destination_file = os.path.join(combined_directory, file)
                    shutil.copy(source_file, destination_file)
'''
# 強行置入學員學號於 Slug 與 .md 檔案名稱的處理方式
avoid_students = []  # 建立一個空的列表，用來存放要避開的學生學號
# 避開第一個 markdown 目錄
for directory in input_directories[1:]:  # 逐一處理 input_directories 列表中除了第一個目錄以外的所有目錄
    student_id = get_student_id(directory)  # 取得學號
    print(student_id)  # 印出學號
    if (student_id != "None") and (student_id not in avoid_students):  # 如果學號不是 "None"，而且不在 avoid_students 列表中
        for root, _, files in os.walk(directory):  # 逐一處理目錄中的所有檔案和子目錄
            for file in files:  # 逐一處理檔案
                if file.endswith('.md'):  # 如果檔案是 Markdown 檔案
                    if "pages" not in root.split(os.path.sep):  # 如果檔案不在 "pages" 子目錄中
                        source_file = os.path.join(root, file)  # 組合檔案路徑
                        updated_source_file = update_slug_and_filename(source_file, student_id)  # 更新 Slug 和檔名
                        destination_file = os.path.join(combined_directory, os.path.basename(updated_source_file))  # 組合目標檔案路徑
                        shutil.copy(updated_source_file, destination_file)  # 複製檔案

# Get the paths of the combined directories
combined_paths = os.path.abspath(combined_directory)  # 取得 combined_directory 的絕對路徑

# Set the Pelican PATH to the combined directory
PATH = combined_paths  # 將 Pelican 的 PATH 設定為 combined_directory 的絕對路徑

# 結束將組員的個別網誌目錄納入分組倉儲中

#OUTPUT_PATH = 'blog'  # 設定輸出的網站目錄，這裡先註解掉

TIMEZONE = 'Asia/Taipei'  # 設定時區為台北

DEFAULT_LANG = 'en'  # 設定預設語言為英文

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None  # 設定不產生 ATOM Feed
CATEGORY_FEED_ATOM = None  # 設定不產生類別 ATOM Feed
TRANSLATION_FEED_ATOM = None  # 設定不產生翻譯 ATOM Feed
AUTHOR_FEED_ATOM = None  # 設定不產生作者 ATOM Feed
AUTHOR_FEED_RSS = None  # 設定不產生作者 RSS Feed

# Blogroll
LINKS = (('Nature', 'https://www.nature.com/'),  # 設定外部連結
        ('Science', 'http://www.sciencemag.org/'),
        ('Sam Harris', 'https://www.samharris.org/'),
        ('Andreas Wagner', 'http://www.ieu.uzh.ch/wagner/'),
        ('American Scientist', 'https://www.americanscientist.org/'),
        ('Scientific American', 'https://www.scientificamerican.com/'),)

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),('Another social link', '#'),)  # 設定社群連結，這裡先註解掉

DEFAULT_PAGINATION = 10  # 設定每頁顯示的文章數量

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True  # 設定是否使用相對網址，這裡先註解掉

# 必須絕對目錄或相對於設定檔案所在目錄
PLUGIN_PATHS = ['plugin']  # 設定外掛程式路徑
PLUGINS = ['summary', 'tipue_search', 'sitemap', 'neighbors']  # 設定要使用的外掛程式

# for sitemap plugin
SITEMAP = {  # 設定 sitemap 外掛程式的參數
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# search is for Tipue search
DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'authors', 'archives', 'search'))  # 設定 Tipue search 外掛程式要搜尋的頁面

# for pelican-bootstrap3 theme settings
#TAG_CLOUD_MAX_ITEMS = 50  # 設定標籤雲的最大標籤數量，這裡先註解掉
DISPLAY_CATEGORIES_ON_SIDEBAR = True  # 設定在側邊欄顯示類別
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True  # 設定在側邊欄顯示最近文章
DISPLAY_TAGS_ON_SIDEBAR = True  # 設定在側邊欄顯示標籤
DISPLAY_TAGS_INLINE = True  # 設定在文章內顯示標籤
TAGS_URL = "tags.html"  # 設定標籤頁面的網址
CATEGORIES_URL = "categories.html"  # 設定類別頁面的網址
#MENUITEMS = [('About', '/blog/pages/about/index.html')]  # 設定選單項目，這裡先註解掉
#SHOW_ARTICLE_AUTHOR = True  # 設定是否顯示文章作者，這裡先註解掉

#MENUITEMS = [('Home', '/'), ('Archives', '/archives.html'), ('Search', '/search.html')]  # 設定選單項目，這裡先註解掉
# try to avoid "WARNING: Watched path does not exist " error
STATIC_PATHS = []  # 設定靜態檔案路徑，這裡設定為空列表，避免出現 "WARNING: Watched path does not exist " 錯誤
# to avoid arise categroy overwritten error
CATEGORY_SAVE_AS = None  # 設定類別頁面的儲存方式，這裡設定為 None，避免出現類別覆寫錯誤