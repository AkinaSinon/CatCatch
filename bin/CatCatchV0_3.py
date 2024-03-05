import os
import shutil
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

 # @author (^･ｪ･^)Cat~
 # @date 2024-01-13

def copy_file(args):
    # 复制单个文件函数
    source_file_path, destination_file_path = args
    buffer_size = 1024 * 1024  # 1 MB 缓冲区大小（根据需要进行调整）

    with open(source_file_path, 'rb') as source_file, open(destination_file_path, 'wb') as dest_file:
        shutil.copyfileobj(source_file, dest_file)

def copy_folder(source_folder, destination_folder):
    # 复制整个文件夹函数【多线程哒】
    folder_name = os.path.basename(source_folder)
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    destination_path = os.path.join(destination_folder, f"{folder_name}-{timestamp}")

    # 统计文件总数
    total_files = sum([len(files) for _, _, files in os.walk(source_folder)])
    current_file = 0

    print(f">> 开始复制文件夹... (＾◡＾)っ\n目标文件夹创建时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n")
    executor = ProcessPoolExecutor()

    try:
        futures = []
        for foldername, subfolders, filenames in os.walk(source_folder):
            for filename in filenames:
                source_file_path = os.path.join(foldername, filename)
                relative_path = os.path.relpath(source_file_path, source_folder)
                destination_file_path = os.path.join(destination_path, relative_path)

                # 确保目标文件夹存在
                os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)

                args = (source_file_path, destination_file_path)
                future = executor.submit(copy_file, args)
                futures.append(future)

                current_file += 1
                progress = (current_file / total_files) * 100
                print(f"\r>> 复制进度：{progress:.2f}% ╰(￣ω￣ｏ)", end='', flush=True)

        for future in as_completed(futures):
            future.result()

        print("\n==>> 文件夹Copy完成~ (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")

    finally:
        executor.shutdown()

if __name__ == "__main__":
    # 源文件夹路径
    source_folder_path = "D:\\Ai'sCatIntheBox\\JavaProject\\gitlab\\intelligent-community"

    # 目标文件夹路径
    destination_folder_path = "D:\\Butterfly"

    # 如若目标文件夹不存在,则创建它╰(￣ω￣ｏ)
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path)

    # 复制文件夹
    copy_folder(source_folder_path, destination_folder_path)
