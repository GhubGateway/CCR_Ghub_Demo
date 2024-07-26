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
#import numpy as np
import os
import subprocess
import sys

class RunJobs():
    

    def __init__(self, ice_sheet_folder, ice_sheet_description, modeling_groups):

        self.ice_sheet_folder = ice_sheet_folder
        self.ice_sheet = ice_sheet_folder.split('/')[-1]
        self.ice_sheet_description = ice_sheet_description
        self.modeling_groups = modeling_groups


        #'''
        print('self.ice_sheet_folder: ', self.ice_sheet_folder)
        print('self.ice_sheet: ', self.ice_sheet)
        print('self.ice_sheet_description: ', self.ice_sheet_description)
        print('self.modeling_groups: ', self.modeling_groups)
        #'''
        
    def run_jobs(self):

        try:

            #########################################################
            # Create the Pegasus WMS workflow
            #########################################################
    
            tooldir = os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
            print ('tooldir: ', tooldir)
            
            # Run the jobs

            modeling_groups_list = list(self.modeling_groups.split(','))
            modeling_groups_list_len = len(modeling_groups_list)
            #print ('type(self.modeling_groups_list): ', type(modeling_groups_list))
            print ('modeling_groups_list_len: ', modeling_groups_list_len)
            print ('modeling_groups_list: ', modeling_groups_list)

            file_basename_list = []
            get_netcdf_info_job_list = []

            launch_script = os.path.join(tooldir, 'bin', 'pythonLaunch.sh')
            sbatch_script = os.path.join(tooldir, 'bin', 'get_netcdf_info_sbatch_slurm.sh')
            slurm_script = os.path.join(tooldir, 'bin', 'get_netcdf_info_slurm.sh')
            job_script = os.path.join(tooldir, 'bin', 'get_netcdf_info.py')

            exitCode = subprocess.call([sbatch_script, slurm_script, launch_script, job_script, self.ice_sheet_folder+'/', self.modeling_groups])
                
            # process_netcdf_info_job depends on all the get_netcdf_info_jobs completing
            
            if exitCode == 0:
                sbatch_script = os.path.join(tooldir, 'bin', 'process_netcdf_info_sbatch_slurm.sh')
                slurm_script = os.path.join(tooldir, 'bin', 'process_netcdf_info_slurm.sh')
                job_script = os.path.join(tooldir, 'bin', 'process_netcdf_info.py')
                exitCode = subprocess.call([sbatch_script, slurm_script, launch_script, job_script, self.ice_sheet_folder, self.ice_sheet_description, self.modeling_groups])
                print('exitCode: ', exitCode)
            else:
                print ('A nonzero exitCode was returned.')
                print ('exitCode: ', exitCode)
                
            sys.stdout.flush()
            
        except Exception as e:
            
            print ('run_jobs_ccr.py Exception: %s\n' %str(e))
            
        return
