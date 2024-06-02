# Import the pandas and numpy packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium

# Load the data
dinosaurs = pd.read_csv('data/dinosaurs.csv')

# Check for missing values
#print(dinosaurs.isnull().sum())

# To handle missing values, I fill the missing numerical values with the median and categorical values with the mode
numeric_cols = dinosaurs.select_dtypes(include=['float64', 'int64']).columns
categorical_cols = dinosaurs.select_dtypes(include=['object']).columns
for col in numeric_cols:
    dinosaurs[col].fillna(dinosaurs[col].median(), inplace=True)

for col in categorical_cols:
    dinosaurs[col].fillna(dinosaurs[col].mode()[0], inplace=True)

# Ensure there are no more missing values
#print(dinosaurs.isnull().sum())  

# The number of different dinosaur names from the name column
dinosaur_names = dinosaurs['name'].nunique()
print(f"The total number of different dinosaur names are {dinosaur_names}.")

# Checking for the largest dinosaur from the length column
# Fill missing values in the column with the mean value
dinosaurs['length_m'].fillna(dinosaurs['length_m'].mean(), inplace=True)

# Find largest dinosaur based
largest_dinosaur = dinosaurs.loc[dinosaurs['length_m'].idxmax()]
print(f"The largest dinosaur is {largest_dinosaur['name']} with a maximum head to tail length of {largest_dinosaur['length_m']} meters.")

# The most occuring dinosaur type
# Check for the distribution from the type column
dinosaur_types = dinosaurs['type'].value_counts()

# Plotting the distribution with enhanced visualization
plt.figure(figsize=(10, 6))
sns.barplot(x=dinosaur_types.index, y=dinosaur_types.values, palette='viridis')
plt.title('Distribution of Dinosaur Types')
plt.xlabel('Dinosaur Type')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

# Finding out if dinosaurs got bigger over time
# Calculate the average age (mid-point) for each dinosaur
dinosaurs['average_ma'] = (dinosaurs['max_ma'] + dinosaurs['min_ma']) / 2

# Scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(dinosaurs['average_ma'], dinosaurs['length_m'], color='skyblue')

# Trend line
z = np.polyfit(dinosaurs['average_ma'], dinosaurs['length_m'], 1)
p = np.poly1d(z)
plt.plot(dinosaurs['average_ma'], p(dinosaurs['average_ma']), "r--")

# Add labels and title
plt.xlabel('Average Age (million years)')
plt.ylabel('Dinosaur Length (meters)')
plt.title('Relationship between Dinosaur Length and Age')

# Invert x-axis to show the timeline from past to present and show plot
plt.gca().invert_xaxis()  
plt.show()

# Print the trend line equation
#print(f'Trend line equation: size = {z[0]} * age + {z[1]}')

# Create an interactive map showing each record
# Initialize the map centered around the mean latitude and longitude
map_center = [dinosaurs['lat'].mean(), dinosaurs['lng'].mean()]
dino_map = folium.Map(location=map_center, zoom_start=2)

# Add points to the map
for idx, row in dinosaurs.iterrows():
    folium.Marker(
        location=[row['lat'], row['lng']],
        popup=f"Name: {row['name']}<br>Type: {row['type']}<br>Length: {row['length_m']} meters",
    ).add_to(dino_map)

# Save the map to an HTML file
dino_map.save('dinosaur_map.html')
