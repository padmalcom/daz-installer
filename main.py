from glob import glob
import os
import patoolib
import shutil
from tqdm import tqdm

ARCHIVE_EXT = 'zip', 'rar', '7z'
TARGET_FOLDERS = ['My Library', 'Content']

src_folder = "D:\\Daz3d\\newcontent"
dest_folder = "E:\\DAZ\\My Library"

folders = glob(src_folder + os.sep + "*\\")

# statistics
input_folder_cnt = len(folders)
input_archive_cnt = 0
extracted_archive_cnt = 0
copied_folder_cnt = 0


def find_archives_and_extract(folder:str) -> []:
	res = []
	for ext in ARCHIVE_EXT:
		archives = glob(folder + os.sep + "*." + ext)
		for a in archives:
			last_folder = os.path.dirname(a)
			a_file_name = os.path.splitext(os.path.basename(a))[0]
			target_dir = os.path.join(last_folder, a_file_name)
			if not os.path.exists(target_dir):
				patoolib.extract_archive(a, outdir=target_dir, verbosity=1)
				global extracted_archive_cnt
				extracted_archive_cnt += 1
			res.append(target_dir)
	return res
	
# extract archives on depth 0
input_archives = find_archives_and_extract(src_folder)
input_archive_cnt = len(input_archives)
folders.extend(input_archives)

content_folders = []
print("Looking for content in root folders...")
for f in tqdm(folders):
	find_archives_and_extract(f)
	sub_folders = glob(f + "*\\")
	while len(sub_folders) > 0:
		new_subfolders = []
		for sf in sub_folders:
			last_folder = os.path.basename(os.path.normpath(sf))
			if last_folder in TARGET_FOLDERS:
				content_folders.append(sf)
			else:
				new_subfolders.extend(glob(sf + "*\\"))
		sub_folders.clear()
		sub_folders.extend(new_subfolders)
print("Found", len(content_folders), "content folders.")

print("Copying content to daz library...")		
for cf in tqdm(content_folders):
	sub_folders = glob(cf + os.sep + "*\\")
	for sf in sub_folders:
		dest = os.path.join(dest_folder, os.path.basename(os.path.normpath(sf)))
		try:
			new_dest = shutil.copytree("\\\\?\\" + sf, dest, dirs_exist_ok=True)
			copied_folder_cnt += 1
		except shutil.Error as error:
			print("Error while copying folder:", error)
			
print("There were", input_folder_cnt, "input folders and", input_archive_cnt, "input archives. We extracted", extracted_archive_cnt, "archives and copied", copied_folder_cnt, "folders.")

