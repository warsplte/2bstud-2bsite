#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'cd2024_2a'
SITENAME = '2a cd2024 評分網誌'
# 不要用文章所在目錄作為類別
USE_FOLDER_AS_CATEGORY = False

#PATH = 'markdown'

# 開始將組員的個別網誌目錄納入分組倉儲中 and skip copying .md file under pages directory
import os
import shutil

# Directories you want to include (手動處理)
#input_directories = ['markdown', 'g10/41123199/markdown']
# 以下採程式方法建立 input_directorie 數列內容

def get_student_id(directory):
    print(directory)
    parts = directory.split("/")
    if len(parts) > 1:
        return parts[1]
    else:
        return None

def read_slug(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if len(lines) >= 6:
            slug_line = lines[5].strip()
            if slug_line.startswith("Slug:"):
                return slug_line[6:].strip()
    return None

def update_slug_and_filename(source_file, student_id):
    with open(source_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if len(lines) >= 6:
            slug_line = lines[5].strip()
            if slug_line.startswith("Slug:"):
                slug = slug_line[6:].strip()
                # 針對 Slug 沒有納入學號者, 以下程是將強行置入
                if not slug.startswith(student_id + "_"):
                    lines[5] = "Slug: " + str(student_id) + "_" + str(slug) + "\n"
                    with open(source_file, "w", encoding="utf-8") as file:
                        file.writelines(lines)

    filename = os.path.basename(source_file)
    # 針對 .md 檔案並未在最前面加入學號, 以下程式將強行置入
    if not filename.startswith(student_id + "_"):
        new_filename = str(student_id) + "_" + str(filename)
        new_source_file = os.path.join(os.path.dirname(source_file), new_filename)
        os.rename(source_file, new_source_file)
        return new_source_file
    return source_file
# 開啟檔案
with open('./downloads/2b.txt', 'r', encoding='utf-8') as file:
    # 讀取每一行
    lines = file.readlines()

# 初始化存放學生資料的字典
student_data = {}

# 迴圈處理每一行
for line in lines:
    # 將每一行以逗號分隔
    data = line.strip().split(',')
    # 將學生資料存入字典
    student_data[data[0]] = data[1:]

# 初始化存放沒有資料的學生學號的列表
no_data_students = []

# 初始化存放目錄的列表，第一個元素為 "markdown"
input_directories = ["markdown"]

# 迴圈處理每位學生
for student_id, data in student_data.items():
    # 如果學生資料缺少第二行的 Github 帳號，將其學號加入沒有資料的學生學號的列表
    if len(data) < 2 or data[1] == '':
        no_data_students.append(student_id)
    else:
        # 若有 github 帳號資料，組合目錄名稱並加入目錄列表中
        if (data[1] != "None") and (student_id != "None"):
            #print("g" + str(data[1]) + "/" + str(student_id) + "/markdown")
            directory_name = "g" + str(data[1]) + "/" + str(student_id) + "/markdown"
            # 只有該組員的目錄存在, 才納入網誌檔案數列
            if os.path.exists(directory_name):
                input_directories.append(directory_name)
#print(input_directories)

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
combined_directory = 'combined_markdown'

# Create the combined directory if it doesn't exist
if not os.path.exists(combined_directory):
    os.makedirs(combined_directory)
else:
    # Clean the existing content of the combined directory
    for root, dirs, files in os.walk(combined_directory):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))

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
avoid_students = []
# 避開第一個 markdown 目錄
for directory in input_directories[1:]:
    student_id = get_student_id(directory)
    print(student_id)
    if (student_id != "None") and (student_id not in avoid_students):
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):
                    if "pages" not in root.split(os.path.sep):
                        source_file = os.path.join(root, file)
                        updated_source_file = update_slug_and_filename(source_file, student_id)
                        destination_file = os.path.join(combined_directory, os.path.basename(updated_source_file))
                        shutil.copy(updated_source_file, destination_file)

# Get the paths of the combined directories
combined_paths = os.path.abspath(combined_directory)

# Set the Pelican PATH to the combined directory
PATH = combined_paths

# 結束將組員的個別網誌目錄納入分組倉儲中

#OUTPUT_PATH = 'blog'

TIMEZONE = 'Asia/Taipei'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Nature', 'https://www.nature.com/'),
        ('Science', 'http://www.sciencemag.org/'),
        ('Sam Harris', 'https://www.samharris.org/'),
        ('Andreas Wagner', 'http://www.ieu.uzh.ch/wagner/'),
        ('American Scientist', 'https://www.americanscientist.org/'),
        ('Scientific American', 'https://www.scientificamerican.com/'),)

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# 必須絕對目錄或相對於設定檔案所在目錄
PLUGIN_PATHS = ['plugin']
PLUGINS = ['summary', 'tipue_search', 'sitemap', 'neighbors']

# for sitemap plugin
SITEMAP = {
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
DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'authors', 'archives', 'search'))

# for pelican-bootstrap3 theme settings
#TAG_CLOUD_MAX_ITEMS = 50
DISPLAY_CATEGORIES_ON_SIDEBAR = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_TAGS_INLINE = True
TAGS_URL = "tags.html"
CATEGORIES_URL = "categories.html"
#MENUITEMS = [('About', '/blog/pages/about/index.html')]
#SHOW_ARTICLE_AUTHOR = True

#MENUITEMS = [('Home', '/'), ('Archives', '/archives.html'), ('Search', '/search.html')]
# try to avoid "WARNING: Watched path does not exist " error
STATIC_PATHS = []
# to avoid arise categroy overwritten error
CATEGORY_SAVE_AS = None