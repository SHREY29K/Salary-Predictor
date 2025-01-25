import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map={}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experience(x):
    if x=="More than 50 years":
        return 50
    if x=="Less than 1 year":
        return 0.5
    return float(x)

def clean_education(x):
    x = x.lower().strip()  
    x = x.replace("’", "'")

    if "bachelor" in x:
        return "Bachelor's degree"
    elif "master" in x or "m.a." in x or "m.s." in x or "m.eng." in x or "mba" in x:
        return "Master's degree"
    elif "professional" in x or "jd" in x or "md" in x or "ph.d" in x or "ed.d" in x:
        return "Post Grad"
    
    return "Less than Bachelor's degree"


@st.cache
def load_data():
  dataset = pd.read_csv("survey_results_public.csv")
  dataset = dataset[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
  dataset = dataset.rename({"ConvertedCompYearly": "Salary"}, axis=1)
  dataset = dataset[dataset["Salary"].notnull()]
  dataset = dataset.dropna()
  dataset = dataset[dataset["Employment"] == "Employed, full-time"]
  dataset = dataset.drop("Employment", axis=1)

  country_map = shorten_categories(dataset.Country.value_counts(), 400)
  dataset['Country'] = dataset['Country'].map(country_map)
  dataset = dataset[(dataset["Salary"] <= 25000) & (dataset["Salary"] >= 10000)]
  dataset = dataset[dataset['Country'] != 'Other']

  dataset['YearsCodePro'] = dataset['YearsCodePro'].apply(clean_experience)
  dataset['EdLevel'] = dataset['EdLevel'].apply(clean_education)

  return dataset

dataset = load_data()

def show_explore_page():
  st.title("Explore Software Developer Salaries")

  st.write(
    """
    ### Stack Overflow Developer Survey of 2023
    """
  )

  data = dataset['Country'].value_counts()

  fig1, ax1 = plt.subplots()

  # Calculate percentages
  percentages = (data / data.sum()) * 100
  labels_with_percentages = [f"{country} ({percent:.1f}%)" for country, percent in zip(data.index, percentages)]

  # Plot the pie chart without labels or percentages
  ax1.pie(
      data,
      shadow=True,
      startangle=140
  )

  # Add a legend with country names and percentages
  ax1.legend(
      labels_with_percentages,  # Labels with percentages
      title="Countries",  # Legend title
      loc="center left",  # Position of the legend
      bbox_to_anchor=(1, 0.5),  # Adjust position to the side
      fontsize=10  # Font size
  )

  ax1.axis('equal')  # Equal aspect ratio for the pie chart

  plt.tight_layout()  # Prevent overlapping of legend and chart
  plt.show()

  st.write("""### Number of Data from Different Countries""")

  st.pyplot(fig1)


  st.write("""### Mean Salary Based on Country""")

  data = dataset.groupby("Country")["Salary"].mean().sort_values(ascending=False)
  st.bar_chart(data)

  st.write("""### Mean Salary Based on Experience""")

  data = dataset.groupby("YearsCodePro")["Salary"].mean().sort_values(ascending=False)
  st.line_chart(data)