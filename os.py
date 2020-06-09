
import os
import uuid
import requests
import hashlib
from multiprocessing import Pool
print("MY NAME IS AYLİN DURAN , MY ID IS 170709058")
print("parent proc ID: ", os.getppid())
print("proc ID", os.getpid())

child = os.fork()

cpu = os.cpu_count()
files = []
hash = []

def download_file(url, file_name=None):
    r = requests.get(url, allow_redirects=True)
    file = file_name if file_name else str(uuid.uuid4())
    open(file, 'wb').write(r.content)
    return file

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def hash_check(hash, hash_list):
    same_hash_index=[]
    for i in hash_list:
        if hash==i:
            same_hash_index.append(hash_list.index(i))
    if len(same_hash_index)>1:
        print("same files are :","\n")
        for i in range(len(same_hash_index)):
            print("{0} ".format(files[i]))


url = ["http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
"https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png",
"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024pxHawai%27i.jpg",
"http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024pxHawai%27i.jpg"]

if child == 0:
    print("child proc ID", os.getpid())
    for i in url:
        files.append(download_file(i))
    for i in files:
        hash.append(md5(i))
    with Pool(cpu) as p:
        print(p.starmap(hash_check, [(hash[0],hash),(hash[1],hash),(hash[2],hash),(hash[3],hash),(hash[4],hash)]))

    os._exit(0)

print("here is parent proc")
child_proc_exit_status = os.wait()
print("child exit with status: ", child_proc_exit_status[1])
