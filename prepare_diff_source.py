# -*- coding: utf-8 -*-
import os, sys, hashlib, re

def genRandom():
	return shell_exec("openssl rand -base64 32 | md5").strip()

def shell_exec(cmd):
	cmd_ = os.popen(cmd)
	result = ''
	if cmd_:
		result = cmd_.read()
		cmd_.close()
	return result.strip()

def is_dir(path):
	return os.path.isdir(path)

def is_file(path):
	return os.path.isfile(path)

def md5file(fname):
   if not is_file(fname):
	   return None
   hash_md5 = hashlib.md5()
   size_ = 128 * hash_md5.block_size
   with open(fname, "rb") as f:
      for chunk in iter(lambda: f.read(size_), b""):
         hash_md5.update(chunk)
   return hash_md5.hexdigest()

def get_script_name():
	return sys.argv[0]

def genPath(desirePath):
   try:
      os.makedirs(desirePath)
   except Exception as e:
      pass

# -------------------------------------
# $ git credential-osxkeychain erase
# host=github.com
# protocol=https
# <press return>
# -------------------------------------
current_path = shell_exec('cd ~;pwd').strip()
base_path = current_path+'/.tmp_work_for_git_'+genRandom()
compare_dir = current_path+'/Downloads/GITHUB_PROJECT_COMPARE/'
if len(sys.argv) >= 5:
	chkl={}
	github_id = sys.argv[1]
	compare = [int(sys.argv[3]),int(sys.argv[4])]
	project_id = sys.argv[2]
	random_str = genRandom()
	path_ = ""+base_path+"/"+random_str+""
	code = ""
	code += "rm -rf "+base_path+"; mkdir -p "+base_path+"/"+random_str+";"
	code += "cd "+base_path+"/"+random_str+";git clone https://github.com/"+github_id+"/"+project_id+".git/;cd `ls`; git config pager.diff false; git config --global core.pager cat; git log | grep '^commit';"
	list_ = shell_exec(code).split('\n')
	shell_exec("rm -rf "+compare_dir)
	shell_exec("mkdir -p "+compare_dir)
	cnt = 0
	for no in compare:
		if len(list_) > no and list_[no].find(' ') > -1:
			cnt += 1
			kks = list_[no].split(' ')[1]
			cl = str(cnt)
			shell_exec("cp -R "+path_+" "+base_path+"/"+cl)
			shell_exec("cd "+base_path+"/"+cl+"/"+project_id+";git checkout "+kks)
			shell_exec("mv "+base_path+"/"+cl+"/"+project_id+" "+compare_dir+"/"+cl)
			shell_exec("rm -rf "+compare_dir+"/"+cl+"/.git")
			chkl[str(cnt)]=kks
	if cnt < 2:
		shell_exec("rm -rf "+compare_dir)
		print '-'*80
		print 'Index number of this project is out of range'
		print '-'*80
	else:
		fde = ['1', '2']
		cnt = 0
		for nn in fde:
			for root, dirs, files in os.walk(compare_dir+""+nn):
				for file in files:
					filepath = str(root+'/'+file)
					pppth = filepath[len(compare_dir)+1:len(filepath)]
					pth1 = (compare_dir+""+fde[cnt])
					pth2 = (compare_dir+""+fde[0])
					if cnt == 0:
						pth2 = (compare_dir+""+fde[cnt+1])
					pl1 = pth1+pppth
					pl2 = pth2+pppth
					oo_p1=pth1+'_/'
					if not is_dir(oo_p1):
						shell_exec('mkdir -p '+oo_p1)
					md1 = md5file(pl1)
					md2 = md5file(pl2)
					if md1 and md2 and (md1==md2):
						pass
					else:
						shell_exec('cp '+pl1+' '+oo_p1+(pppth.replace('/','／')))
			cnt+=1
		print '-'*80
		for no in shell_exec('ls '+compare_dir).split('\n'):
			old_name = None
			new_name = None
			chkk = chkl[no.replace('_', '')]
			chkk = ''
			if no.find('_') != -1:
				old_name = no
				new_name = 'trimmed_'+(no.replace('_',''))+'_'+chkk
			else:
				old_name = no
				new_name = 'rawdata_'+no+'_'+chkk
			if old_name and new_name:
				shell_exec('cd '+compare_dir+';mv '+old_name+' '+new_name)
		print '-'*80
		print 'Files are downloaded on '+compare_dir+'\n'
		for no in shell_exec('ls '+compare_dir).split('\n'):
			print compare_dir+no
		print '-'*80
	shell_exec("rm -rf "+base_path)
else:
	print '-'*80
	print 'python '+get_script_name()+' github_account_id project_id commit_number commit_number'
	print ''
	print 'github_account_id: github account id'
	print 'project_id: project name'
	print 'commit_number: if you give 0 then it means the first one of all commits'
	print 'commit_number: if you give 1 then it means the second one of all commits'
	print ''
	print '[Usage]'
	print '1. place '+get_script_name()+' file on your pc'
	print '2. turn on terminal app and type below'
	print '   python '+get_script_name()+' kstost PrepareDiffSource 0 1'
	print '-'*80
