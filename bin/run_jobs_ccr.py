#---------------------------------------------------------------------------------------------------
# run_jobs_ccr.py
# Component of:
#     https://github.com/GhubGateway/CCRDemo and
#     https://theghub.org/tools/ghubex1
# Called from: ccrghubdemo.ipynb
# Also see Ghub, https://theghub.org/about
# Purpose: Run a workflow on CCR
# Author: Renette Jones-Ivey
# Date: July 2024
#---------------------------------------------------------------------------------------------------

import ast
import numpy as np
import os
import subprocess
import sys

class RunJobs():
    

    def __init__(self, username, ice_sheet_description, ice_sheet_folder, modeling_groups):

        self.username = username
        self.ice_sheet_description = ice_sheet_description
        self.ice_sheet_folder = ice_sheet_folder
        self.ice_sheet = ice_sheet_folder.split('/')[-1]
        self.modeling_groups = modeling_groups
        self.waittime = 15 #minutes - includes pending and execution times

        #'''
        print('self.username: %s' %self.username)
        print('self.ice_sheet_description: %s' %self.ice_sheet_description)
        print('self.ice_sheet_folder: %s' %self.ice_sheet_folder)
        print('self.ice_sheet: %s' %self.ice_sheet)
        print('self.modeling_groups: %s' %str(self.modeling_groups))
        #'''
        
    def run_jobs(self):

        try:

            #########################################################
            # Run the workflow jobs
            #########################################################
    
            tooldir = os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
            print ('tooldir: ', tooldir)
            
            modeling_groups_list = list(self.modeling_groups.split(','))
            modeling_groups_list_len = len(modeling_groups_list)
            #print ('type(self.modeling_groups_list): ', type(modeling_groups_list))
            print ('modeling_groups_list_len: ', modeling_groups_list_len)
            print ('modeling_groups_list: ', modeling_groups_list)

            launch_script = os.path.join(tooldir, 'bin', 'pythonLaunch.sh')
            sbatch_script = os.path.join(tooldir, 'bin', 'sbatch_slurm.sh')
            slurm_script = os.path.join(tooldir, 'bin', 'get_netcdf_info_slurm.sh')
            job_script = os.path.join(tooldir, 'bin', 'get_netcdf_info.py')
            wait_script = os.path.join(tooldir, 'bin', 'wait.sh')

            # Implements minimal method to submit batch slurm jobs and wait for the slurm jobs to complete.
            # More sophisticated methods exist.
            exitCodes = np.zeros(modeling_groups_list_len)
            for i in range(modeling_groups_list_len):
            
                modeling_group  = modeling_groups_list[i]
                print ('modeling_group: ', modeling_group)
                modeling_group_path = os.path.join(self.ice_sheet_folder, modeling_group)
                print ('modeling_group_path: ', modeling_group_path)
                exitCodes[i] = subprocess.call([sbatch_script, slurm_script, launch_script, job_script, modeling_group_path])
            #print('exitCodes: %s' %str(exitCodes))

            # process_netcdf_info_job depends on all the get_netcdf_info_jobs completing
            
            exitCode = subprocess.call([wait_script, self.username, str(self.waittime)])
            #print ('exitCode: %s' %str(exitCode))

            if np.sum(exitCodes) == 0:
                sbatch_script = os.path.join(tooldir, 'bin', 'sbatch_slurm.sh')
                slurm_script = os.path.join(tooldir, 'bin', 'process_netcdf_info_slurm.sh')
                job_script = os.path.join(tooldir, 'bin', 'process_netcdf_info.py')
                exitCodes[0] = subprocess.call([sbatch_script, slurm_script, launch_script, job_script, self.ice_sheet_folder, self.ice_sheet_description, self.modeling_groups])
                #print('exitCodes: %s' %str(exitCodes))
                exitCode = subprocess.call([wait_script, self.username, str(self.waittime)])
                #print ('exitCode: %s' %str(exitCode))
            else:
                print ('A nonzero exitCode was returned.')
                print ('exitCodes: %s' %str(exitCodes))
            
        except Exception as e:
            
            print ('run_jobs_ccr.py Exception: %s\n' %str(e))
            
        return
