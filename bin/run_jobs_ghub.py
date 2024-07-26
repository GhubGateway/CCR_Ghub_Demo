#---------------------------------------------------------------------------------------------------
# run_jobs_ghub.py
# Component of:
#     https://github.com/GhubGateway/CCRDemo and
#     https://theghub.org/tools/ghubex1
# Called from: ccrghubdemo.ipynb
# Also see Ghub, https://theghub.org/about
# Purpose: Plan and submit a Pegasus WMS workflow to run on CCR
# Author: Renette Jones-Ivey
# Date: July 2024
# Reference: https://pegasus.isi.edu/documentation
#---------------------------------------------------------------------------------------------------

import ast
import os
import sys

#import Rappture
#from Rappture.tools import executeCommand as RapptureExec
# Modified for Python 2 to 3
import hublib.cmd
#help (hublib.cmd.command.executeCommand)

# API for generating Pegasus YML files
from Pegasus.api import *

class RunJobs():
    

    def __init__(self, ice_sheet_folder, ice_sheet_description, modeling_groups):

        self.ice_sheet_folder = ice_sheet_folder
        self.ice_sheet = ice_sheet_folder.split('/')[-1]
        self.ice_sheet_description = ice_sheet_description
        self.modeling_groups = modeling_groups
        self.maxwalltime = 30 #minutes

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
            
            # Pegasus requires three catalogs and the workflow's job definitions to plan and start a workflow:

            # The Site Catalog defines the site(s) where the workflow jobs are to be executed.
            # On Ghub, the site catalog is preconfigured for the UB-HPC cluster.
            
            # The Transformation Catalog defines the executable(s) invoked on the cluster to run the workflow jobs.
            # On Ghub, the specified executable is a bash launch script for the selected template which runs the workflow jobs,
            # passed in as arguments to the bash launch script.
            
            # The Replica Catalalog defines the locations of the input files required by the workflow jobs.

            wf = Workflow('ccrghubdemo-workflow')
            tc = TransformationCatalog()
            rc = ReplicaCatalog()

            # Add the python launch script to the transformation catalog. The launch script is run on CCR to run the python scripts.
                
            tooldir = os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
            print ('tooldir: ', tooldir)
            python_launch_exec_path =  os.path.join(tooldir, 'remotebin', 'pythonLaunch.sh')
            print ("python_launch_exec_path: %s" %python_launch_exec_path)
            
            pythonlaunch = Transformation(
                'pythonlaunch',
                site='local',
                pfn=python_launch_exec_path,
                is_stageable = True, #Stageable or installed
                arch=Arch.X86_64,
                os_type=OS.LINUX,
                os_release="rhel")

            tc.add_transformations(pythonlaunch)
            wf.add_transformation_catalog(tc)

            # All files in a Pegasus workflow are referred to in the DAX using their Logical File Name (LFN).
            # These LFNs are mapped to Physical File Names (PFNs) when Pegasus plans the workflow.
            # Add input files to the DAX-level replica catalog
            
            rc.add_replica('local', File('get_netcdf_info.py'), os.path.join(tooldir, 'bin', 'get_netcdf_info.py'))
            rc.add_replica('local', File('process_netcdf_info.py'), os.path.join(tooldir, 'bin', 'process_netcdf_info.py'))
            wf.add_replica_catalog(rc)

            # Add job(s) to the workflow

            modeling_groups_list = list(self.modeling_groups.split(','))
            #print ('type(self.modeling_groups_list): ', type(modeling_groups_list))
            #print('len(modeling_groups_list): ', len(modeling_groups_list))
            print ('modeling_groups_list: ', modeling_groups_list)

            file_basename_list = []
            get_netcdf_info_job_list = []

            for i in range(len(modeling_groups_list)):
            
                modeling_group  = modeling_groups_list[i]
                #print ('modeling_group: ', modeling_group)
                modeling_group_path = os.path.join(self.ice_sheet_folder, modeling_group)
                #print ('modeling_group_path: ', modeling_group_path)
                file_basename = '_'.join(modeling_group_path.split('/')[-2:])
                #print ('file_basename: ', file_basename)
                file_basename_list.append(file_basename)

                # Note: on Ghub, .add_outputs register_replica must be set to False (the default is True) to prevent
                # Pegasus from returning with a post script failure.
                
                get_netcdf_info_job = Job(pythonlaunch)\
                    .add_args("""get_netcdf_info.py %s""" %(modeling_group_path))\
                    .add_inputs(File('get_netcdf_info.py'))\
                    .add_outputs(File('%s_netcdf_info.txt' %file_basename), stage_out=True, register_replica=False)\
                    .add_outputs(File('%s_netcdf_info.json' %file_basename), stage_out=False, register_replica=False)\
                    .add_metadata(time='%d' %self.maxwalltime)
                    
                wf.add_jobs(get_netcdf_info_job)
                get_netcdf_info_job_list.append (get_netcdf_info_job)

            process_netcdf_info_job = Job(pythonlaunch)\
                .add_args('''process_netcdf_info.py %s %s %s''' %(self.ice_sheet_folder, self.ice_sheet_description, self.modeling_groups))\
                .add_inputs(File('process_netcdf_info.py'))\
                .add_outputs(File('%s_processed_netcdf_info.txt' %self.ice_sheet), stage_out=True, register_replica=False)\
                .add_metadata(time='%d' %self.maxwalltime)
                
            for i in range(len(modeling_groups_list)):
                process_netcdf_info_job.add_inputs(File('%s_netcdf_info.json' %file_basename_list[i]), bypass_staging=True)
                
            wf.add_jobs(process_netcdf_info_job)
            
            # process_netcdf_info_job depends on all the get_netcdf_info_jobs completing
            
            wf.add_dependency(process_netcdf_info_job, parents=get_netcdf_info_job_list)

            #########################################################
            # Create the Pegasus Workflow YML file
            #########################################################
    
            # Create the YML file
            try:
                wf.write()
            except PegasusClientError as e:
                print(e)

            # Verify contents
            #fp = open('workflow.yml', 'r')
            #file_contents = fp.read()
            #print (file_contents)
            #fp.close()
            
            sys.stdout.flush()
            
            #########################################################
            # Submit the Pegasus Workflow Plan
            #########################################################
    
            # *** Disabled pending resolution of an open Ghub ticket ***
            '''
            submitcmd = ['submit', '--venue', 'WF-vortex-ghub', 'pegasus-plan', '--dax', 'workflow.yml']
            #print ('submitcmd: ', submitcmd)

            # submit blocks.
            exitCode,pegasusStdout,pegasusStderr = hublib.cmd.command.executeCommand(submitcmd,streamOutput=True)

            if (exitCode == 0):

                return

            else:
            
                # In this case, look for .stderr and .stdout files in the work directory
                print ('Wrapper.py: hublib.cmd.command.executeCommand(%s) returned with a non zero exit code = %d\n' %(submitcmd, exitCode))
                files = os.listdir(tooldir)
                files.sort(key=lambda x: os.path.getmtime(x))
                for file in files:
                    # Get the numbered Pegasus work directory
                    #print ('type(file): ', type(file)) #<class 'str'>
                    if os.path.isfile(file) and file[0].isdigit() and file.endswith('.stderr'):
                        print ('stderr file: %s\n' %os.path.join(tooldir, file))
                        print ('For the ghubex1 tool, the following errors were returned while running a Pegasus workflow: ')
                        with open(file) as f:
                            lines = f.readlines()
                            for line in lines:
                                if 'WARNING' not in line:
                                    print (line)
                        # In case there is more than one stderr file in the working directory
                        break
                return
              '''
             
        except Exception as e:
            
            print ('launchWrapper.py Exception: %s\n' %str(e))
            
        return
