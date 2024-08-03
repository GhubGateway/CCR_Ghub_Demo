# CCR/Ghub Jupyter Notebook Demo

This Jupyter Notebook provides a demonstration and scripts for executing jobs in parallel on the University at Buffalo (UB)'s Center For Computational Research (CCR)'s high performance compute cluster, UB-HPC. 

On CCR, sbatch and Slurm commands are used to execute the parallel jobs.

On Ghub, the Pegasus Workflow Management System (WMS) is used to execute the parallel jobs.

## How to use this notebook:

To clone this GitHub repository, in a terminal window enter:<br />

git clone https://github.com/GhubGateway/CCR_Ghub_Demo

### CCR

- Login to CCR OnDemand.
- Launch a Quick Launch General-Compute Desktop Interactive App.
- Open a terminal window (Click the **>_** button).
- In the terminal window, clone this GitHub repository.
- In the terminal window, change directory (cd) to the CCR_Ghub_Demo directory and install the ccrghubdemo_kernel Jupyter kernel:
    - Enter: source install_ccrghubdemo.2023.01_kernel.sh
- Launch the Quick Launch JupyterLab/Notebook Interactive App, check the JupyterLab check box and Connect to Jupyter.
- Open the ccrghubdemo.ipynb notebook.
- Select Kernel / Change Kernel and select the ccrghubdemo_kernel Kernel, the Python 3 (ipykernel) Kernel is set by default.
- Select Kernel, Restart Kernel and Run All Cells. 

### Ghub

- Login to Ghub.
- Launch the Workspace 10 Tool.
- In the terminal window, clone this GitHub repository. 
- Launch the Jupyter Notebooks (202210) Tool.
- Open the ccrghubdemo.ipynb notebook.
- The Python 3 (ipykernel) Kernel is set by defaiult.
- Select Kernel, Restart & Run All.



