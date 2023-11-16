import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

#To determine if a person is overweight, 
#first calculate their BMI by dividing their weight in kilograms by the square of their height in meters. 
#If that value is > 25 then the person is overweight. 
#Use the value 0 for NOT overweight and the value 1 for overweight.

# Add 'overweight' column
df['overweight'] = df['weight']/((df['height']/100)**2)
df['overweight'] = np.where(df['overweight'] > 25, 1, 0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df[['cholesterol','gluc']] = df[['cholesterol','gluc']].applymap(lambda x: 1 if x > 1 else 0)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = df[['cholesterol','gluc','smoke','alco','active','overweight','cardio']]


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = pd.melt(df_cat, id_vars = ['cardio'], var_name = 'variable', value_name = 'value')
    

    # Draw the catplot with 'sns.catplot()'
    df_cat = df_cat.groupby(['cardio','variable','value']).size().reset_index(name='total')


    # Get the figure for the output
    fig = sns.catplot(x='variable', y='total', hue='value', data=df_cat, kind='bar', col='cardio', legend='True').fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


#Clean the data. Filter out the following patient segments that represent incorrect data:

#diastolic pressure is higher than systolic (Keep the correct data with (df['ap_lo'] <= df['ap_hi']))
#height is less than the 2.5th percentile (Keep the correct data with (df['height'] >= df['height'].quantile(0.025)))
#height is more than the 97.5th percentile
#weight is less than the 2.5th percentile
#weight is more than the 97.5th percentile

#Clean the data. Filter out the following patient segments that represent incorrect data:

# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi'])\
                    &(df['height'] >= df['height'].quantile(0.025))\
                    &(df['height'] <= df['height'].quantile(0.975))\
                    &(df['weight'] >= df['weight'].quantile(0.025))\
                    &(df['weight'] <= df['weight'].quantile(0.975))
                   ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)

    # Set up the matplotlib figure
    fig, ax = plt.subplots()
    heatmap = sns.heatmap(corr, annot=True, mask=mask, cmap='icefire', center = 0.1, \
                          cbar_kws={'shrink': 0.5}, \
                          xticklabels=True, yticklabels=True, linewidths=0.5, linecolor='white', fmt= '.1f', ax=ax)
    

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
