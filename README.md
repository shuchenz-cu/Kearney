# Kearney
Instruction:
1.	Go to the terminal and type in ‘pip install -r requirements.txt’ in the command line
2.	Type in ‘streamlit run Kearney_Dash_(your choice of optimization algorithm).py’
3.	To stop the algorithm, type in ‘control-c’ in the MacOSterminal(the command details may  depends on the OS system)

Note:
1.	The usage of Gurobi might need license. If the installation of gurobipy has failed, please refer to https://pypi.org/project/gurobipy/ for more information
2.	Extra two optimization functions CVXPY and scipy.optimize.minimize are stored in the Additional_Optimizations.ipynb
3.	All files should be stored and run within the same folder, especially the ‘Kearney_Dash.py’ and ‘ingredients.csv’.  If the stored location for csv file is different from the dash file, please change the csv file location inside the pd.read_csv(‘…’)
