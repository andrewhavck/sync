#!/usr/bin/python

#_ sync.py v.1                                                             #11/10/2008

#_ @lavalava 

#_ this python script will clone an already similar directory. 
#_ the script was designed for substantially large directories.
#_ the script uses a depth first algorithm. if the local is
#_ significantly deeper expect a long copy process.

from __future__ import generators

#_ might need these
import os
import subprocess
import filecmp

#_ the local and remote paths being replicated.
local = "/home/andrew/"
remote = "/media/whales/"

#_ this function walks both the remote and local directory.
def dive(remote_dir,local_dir): 
 
   #_common contains the directories which are common between the remote
   #_and the local
   for common in filecmp.dircmp(local_dir,remote_dir).common_dirs:

     #_ paths used for the walk function call.
     l_common = os.path.join(local_dir,common)
     r_common = os.path.join(remote_dir,common)
    
     print "Checking ---" + r_common + "--- "
    
     #_ walk to the child directory
     dive(r_common,l_common)

   #_the dir_kill contains the directories or files solely in the remote_dir.
   #_that will be killed/erased
   for dir_kill in filecmp.dircmp(local_dir,remote_dir).right_only:
     
     #_get the full path
     path_kill  = os.path.join(remote_dir,dir_kill) 
  
     print "Deleting " + path_kill + " --" 
  
     #_make the child process do the removal, and wait
     subprocess.Popen(["rm","-rf",path_kill]).wait() 
  
   #_the dir_copy contains the directories or files solely in the local_dir.
   #_that will be copied over to the remote directory.
   for dir_copy in filecmp.dircmp(local_dir,remote_dir).left_only:

     #_get the full path for remote and local
     l_copy  = os.path.join(local_dir,dir_copy)
     r_copy = os.path.join(remote_dir,dir_copy) 

     print "Copying " + l_copy + " to " + r_copy + " --"  
    
     #_make the child process to do the copying
     subprocess.Popen(["cp","-rf",l_copy,r_copy]).wait() 

   #_the dir_diff contains the files or directories that differ but have the 
   #_same filename.
   for dir_diff in filecmp.dircmp(local_dir,remote_dir).diff_files:

     #_get the full path for remote and local
     l_diff  = os.path.join(local_dir,dir_diff)
     r_diff = os.path.join(remote_dir,dir_diff)
      
     print "Updating " + r_diff + " --"  

     #_make the child processes to do the erasing and copying.
     subprocess.Popen(["rm","-rf",r_diff]).wait()
     subprocess.Popen(["cp","-rf",l_diff,r_diff]).wait()   

#walah
print "\n ---Sync starting--- \n"

dive(remote,local)

print "\n ---Done."


