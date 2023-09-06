import streamlit as st
import pandas as pd
import numpy as np
import gurobipy as gp


########### Layouts for dashboard
st.title('Food Composition Estimator')

# Load the ingredients database
ingredients_df = pd.read_csv("ingredients.csv")


# Widget for selecting number of ingredients
st.header("Step 1: Use slider to choose total number of ingredients")
num_ingredients = st.slider("Select number of ingredients", 1, 10, 7)
# Widget for selecting ingredients
st.header("Step 2: Please enter the top {} ingredients found in the product".format(num_ingredients))
selected_ingredients = []
for i in range(num_ingredients):
    ingredient = st.selectbox("Ingredient {}".format(i+1), ingredients_df["Descrip"].unique())
    selected_ingredients.append(ingredient)
    
    
# Widget for entering Big 7 values
st.header("Step 3: Please enter the Big 7 values of the product")
carbs = st.number_input("Carbohydrates (g)", value=0.0)
energy = st.number_input("Energy (Calories)", value=0.0)
sat_fat = st.number_input("Saturated fats (g)", value=0.0)
protein = st.number_input("Protein (g)", value=0.0)
sodium = st.number_input("Sodium (mg)", value=0.0)
sugar = st.number_input("Sugar (g)", value=0.0)
fat = st.number_input("Fat (g)", value=0.0)


# Create an array of the selected ingredients in the order they were selected
selected_ingredients_array = []
ingredient_indices = []
for ingredient in selected_ingredients:
    # selected_ingredients_array.append(ingredient)
    ingredient_indices.append(ingredients_df[ingredients_df['Descrip'] == ingredient].index.values[0])
ingredient_value = ingredients_df.iloc[ingredient_indices][['Carb_g','Energy_kcal','Saturated_fats_g','Protein_g','Sodium_mg','Sugar_g','Fat_g']].values.tolist()

# st.write("")

# time = st.number_input("Maximum optimization time(in minutes)", value = 10)

st.write("")
if st.button('Start optimize process'):
    product_value = np.array([carbs, energy, sat_fat, protein,sodium, sugar, fat])
    
    
    ########### The optimization function, could be replace with any other optimization algorithms
    ########### with the output as [x1, x2, ..., xn] with n elements represents percentages for n ingredients(in order)
    
    from scipy.optimize import minimize

    def minimize_func(A, b):
        A = A.T
        ###### Set objective function
        ###### dot score of y has been divided by 10000 due to the convergence requirements of scipy.minimize
        def fmin(x):
            y = (np.dot(A, x) - b)/0.2
            return np.dot(y, y)/10000

        #=================================================


        m = np.shape(A)[0]
        n = np.shape(A)[1]


        ### Different start point:

        # Choice 1: increasing for ith item:
        # x0 = []
        # for i in range(n):
        #     x0.append(2*(n-i)/((n+1)*n))

        # Choice 2: start from 1/n
        # x0 = np.ones(n)/n
        
        # Choice 3: start from zeros:
        x0 = np.zeros(n)

        #=================================================

        bnds = (( (1*10e-100, 1), )*n) #all x_i must be between 0 and 1
        cons = [{'type': 'eq', 'fun': lambda x: 1.0-np.sum(x)}] #sum(x_i) = 1 and Ax <= b
        cons = cons + [{'type': 'ineq', 'fun': lambda x,i=i: x[i] - x[i+1]} for i in range(n-1)] #consider order of vectors as constraints
        res = minimize(fmin, x0, method='SLSQP',bounds=bnds,constraints=cons)
        
        return res.x

    with st.spinner("Training ongoing"):
        
        ####### Once the optimization algorithm changed, the function name here should be changed too
        results = minimize_func(np.array(ingredient_value), np.array(product_value))
    
        st.subheader("The results are:")
        for i in range(len(selected_ingredients)):
            st.write('Estimated percentage for', '**' + selected_ingredients[i] + '**', 'is:', round(results[i]*100, 2), '%')