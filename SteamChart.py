#!/usr/bin/env python
# coding: utf-8

# ## **OCTARIO FACHRI IRIAWAN (1301190416)**
# ## **MAULANA NUR (1301190402)**

# In[1]:


# Import the required libraries
import numpy as np
import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, Slider, Select, CheckboxGroup, Div, NumeralTickFormatter
from bokeh.layouts import column, row


# In[2]:


# Load the datas into dataframes
df1 = pd.read_csv('Data/steam_games_preprocessed_small.csv')
df2 = pd.read_csv('Data/steam_games.csv', delimiter=';')

# Replace spaces with underscores
df.columns = df.columns.str.replace(' ', '_')
df2.columns = df2.columns.str.replace(' ', '_')

# Assign a list of columns consisting of 'App_ID', 'Developer', 'Publisher', 'Genre', 'Tags', 'Categories', 'Languages', and 'Platforms' to a variable named 'cols'
cols=['App_ID', 'Developer', 'Publisher', 'Genre', 'Tags', 'Categories', 'Languages', 'Platforms']

# Merge the two dataframes on the 'App ID' column
df = pd.merge(df1,df2[cols],on='App ID', how='left')

# Show the dataframe
df.head()


# In[40]:


# Create an empty list to store the dictionaries
tags_list = []

# Iterate over the 'Tags_y' column
for tag in df['Tags_y']:
    # Convert the column value to dictionary using dict()
    tag_dict = dict(item.split(':') for item in tag.split(','))
    # Add the dictionary to the 'tags_list'
    tags_list.append(tag_dict)
# Add the tags list into the 'Tags_y' column
df['Tags_y'] = tags_list

# Split the'Genre_y', 'Categories_y', 'Languages_y', and 'Platforms_y' columns at commas
df['Genre_y'] = df['Genre_y'].str.split(', ')
df['Categories_y'] = df['Categories_y'].str.split(', ')
df['Languages_y'] = df['Languages_y'].str.split(', ')
df['Platforms_y'] = df['Platforms_y'].str.split(', ')


# In[41]:


# Extract the unique values from the 'Genre', 'Tags', 'Categories', 'Languages', and 'Platforms' columns. Then convert them to lists
g_genres = df['Genre_y'].explode().unique().tolist()
g_tags = df['Tags_y'].explode().unique().tolist()
g_categories = df['Categories_y'].explode().unique().tolist()
g_languages = df['Languages_y'].explode().unique().tolist()
g_platforms = df['Platforms_y'].explode().unique().tolist()

#Sort the columns values alphabetically
g_genres.sort()
g_tags.sort()
g_categories.sort()
g_languages.sort()
g_platforms.sort()


# In[ ]:


# Create a new column in the DataFrame called 'x' and 'y' and assign the values from the 'Ratings' and 'Estimated Revenue' column to it respectively
df['x'] = df['Ratings']
df['y'] = df['Estimated Revenue']


# In[26]:


# Create a ColumnDataSource object from the dataframe
source = ColumnDataSource(df)


# In[52]:


# Create a hover tool with tooltips
hover = HoverTool(tooltips = [('Name', '@Name'), ('Ratings', '@Ratings'), ('Price', '@Initial_Price'), ('Developer','@Developer_y'), ('Publisher','@Publisher_y'), ('Genre','@Genre_y')])

# Create a figure with the hover tool and crosshair
plot = figure(title='Steam Games Chart', x_axis_label='Ratings', y_axis_label='Estimated Revenue', width=800, height=600, tools=[hover,'crosshair'])

# Set the x-axis and y-axis tick formatter to make the values more readable
plot.xaxis.formatter = NumeralTickFormatter(format='0.0a')
plot.yaxis.formatter = NumeralTickFormatter(format='0.0a')

# Add a circle glyph to the plot
plot.circle(x = 'x', y = 'y', source = source, color = "blue", hover_color = "orange", fill_alpha = 0.2, line_width = 0)

# Set the minimum border size of the plot
plot.min_border = 75


# In[ ]:


# Create a CheckboxGroup for widget Genres
checkbox_group_1 = CheckboxGroup(labels=g_genres)

# Create a CheckboxGroup widget for Tags
checkbox_group_2 = CheckboxGroup(labels=g_tags)

# Create a CheckboxGroup widget for Categories
checkbox_group_3 = CheckboxGroup(labels=g_categories)

# Create a CheckboxGroup widget for Languages
checkbox_group_4 = CheckboxGroup(labels=g_languages)

# Create a CheckboxGroup widget for Platforms
checkbox_group_5 = CheckboxGroup(labels=g_platforms)

# Get the minimum and maximum values of the Initial_Price, Ratings, and Owners_average columns
price_min, price_max = df['Initial_Price'].min(), df['Initial_Price'].max()
ratings_min, ratings_max = df['Ratings'].min(), df['Ratings'].max()
owners_min, owners_max = df['Owners_average'].min(), 10000000

# Create a Slider widget for Initial_Price
price_slider = Slider(start=price_min, end=price_max, value=price_max, step=1, title="Max Price is")

# Create a Slider widget for Ratings
ratings_slider = Slider(start=ratings_min, end=ratings_max, value=ratings_min, step=5, title="Min Ratings is")

# Create a Slider widget for Owners_average 
owners_slider = Slider(start=owners_min, end=owners_max, value=owners_min, step=10000, title="Min Estimated Owners is")

# Create a Select widget for x-axis
x_axis_data = Select(
    # Set the options to the column names
    options = ['Ratings', 'Initial_Price', 'Owners_average', 'Estimated Revenue'],
    # Set the initial value to 'Ratings'
    value = 'Ratings',
    # Set the title to 'X-axis'
    title = 'X-axis'
)

# Create a Select widget for y-axis
y_axis_data = Select(
    # Set the options to the column names
    options = ['Ratings', 'Initial_Price', 'Owners_average', 'Estimated Revenue'],
    # Set the initial value to 'Estimated Revenue'
    value = 'Estimated_Revenue',
    # Set the title to 'Y-axis'
    title = 'Y-axis'
)


# In[ ]:


# Define a callback function to update the data shown in the plot based on the checked boxes
def update(attr, old, new):
    
    # Get the selected checkboxes
    selected_1 = checkbox_group_1.active
    selected_2 = checkbox_group_2.active
    selected_3 = checkbox_group_3.active
    selected_4 = checkbox_group_4.active
    selected_5 = checkbox_group_5.active
    
    # Get the current values of the sliders
    price = price_slider.value
    ratings = ratings_slider.value
    owners = owners_slider.value
    
    # Get the selected x-axis and y-axis value
    x = x_axis_data.value
    y = y_axis_data.value
    
    # Set the x-axis and y-axis labels to the selected data based on the value
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    
    # Update the 'x' and 'y' column using the selected data
    df['x'] = df[x]
    df['y'] = df[y]
    
    # Update the boxes variable from containing integers into the column names
    selected_1 = [g_genres[i] for i in selected_1]
    selected_2 = [g_tags[i] for i in selected_2]
    selected_3 = [g_categories[i] for i in selected_3]
    selected_4 = [g_languages[i] for i in selected_4]
    selected_5 = [g_platforms[i] for i in selected_5]
    
    # Filter the data based on the selected options
    filtered_data = df[
        df[selected_1].all(axis=1) & 
        df[selected_2].all(axis=1) &
        df[selected_3].all(axis=1) &
        df[selected_4].all(axis=1) &
        df[selected_5].all(axis=1) &
        (df['Initial_Price'] <= price) &
        (df['Ratings'] >= ratings) &
        (df['Owners_average'] >= owners)
    ]
    
    # Update the data in the ColumnDataSource
    source.data = ColumnDataSource.from_df(filtered_data)


# In[ ]:


# Add a listener to the checkbox group widget to call the update function when the active boxes change
checkbox_group_1.on_change('active', update)
checkbox_group_2.on_change('active', update)
checkbox_group_3.on_change('active', update)
checkbox_group_4.on_change('active', update)
checkbox_group_5.on_change('active', update)

# Add a listener to the sliders widget to call the update function when the sliders value change
price_slider.on_change('value', update)
ratings_slider.on_change('value', update)
owners_slider.on_change('value', update)

# Add a listener to the selection widget to call the update function when the selected data change
x_axis_data.on_change('value', update)
y_axis_data.on_change('value', update)


# In[ ]:


# Create a Div widget with the label "Genres"
genre_label = Div(text="<b>Genres</b>")

# Create a Div widget with the label "Tags"
tags_label = Div(text="<b>Tags</b>")

# Create a Div widget with the label "Categories"
categories_label = Div(text="<b>Categories</b>")

# Create a Div widget with the label "Languages"
languages_label = Div(text="<b>Languages</b>")

# Create a Div widget with the label "Platforms"
platforms_label = Div(text="<b>Platforms</b>")

# Create a Div widget with the label "Price"
price_label = Div(text="<b>Price</b>")

# Create a Div widget with the label "Ratings"
ratings_label = Div(text="<b>Ratings</b>")

# Create a Div widget with the label "Estimated Number of Owners"
owners_label = Div(text="<b>Estimated Number of Owners</b>")

# Create a Div widget with the label "X-axis Data"
x_label = Div(text="<b>X-axis Data</b>")

# Create a Div widget with the label "Y-axis Data"
y_label = Div(text="<b>Y-axis Data</b>")


# Add the labels and widgets to the layout
layout = row(
    column(genre_label, checkbox_group_1),
    column(tags_label, checkbox_group_2),
    column(categories_label, checkbox_group_3),
    column(languages_label, checkbox_group_4),
    column(platforms_label, checkbox_group_5),
    column(price_label, price_slider, ratings_label, ratings_slider, owners_label, owners_slider, x_label, x_axis_data, y_label, y_axis_data),
    plot
)

# Add the layout to the document
curdoc().add_root(layout)


# References: </br>
# https://bobbyhadz.com/blog/python-convert-comma-separated-string-to-dictionary </br>
# https://stackoverflow.com/questions/58528989/pandas-get-unique-values-from-column-of-lists </br>
# https://stackoverflow.com/questions/25657448/python-bokeh-plot-how-to-format-axis-display </br>
# https://www.kaggle.com/code/kanncaa1/visualization-bokeh-tutorial-part-1?scriptVersionId=3778211 </br>
# https://ln5.sync.com/dl/a88a4ddf0/2hv7gewd-yeuw8x6i-jzj6sb6m-fuji7crg/view/default/6346379870009 </br>
# https://towardsdatascience.com/data-visualization-with-bokeh-in-python-part-ii-interactions-a4cf994e2512 </br>

# In[ ]:




