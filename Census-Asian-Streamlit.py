import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests

@st.cache
def load_data():
    # Make a request to the US Census API to get the data
    response = requests.get("https://api.census.gov/data/2020/acs/acs5?get=NAME,B01001_001E,B06009_002E,B06009_003E,B06009_004E&for=county:*&in=state:06")


    # Convert the response to JSON
    data = response.json()

    # Convert the JSON data to a DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])

    # Clean the data
    df = df[["NAME", "B01001_001E", "B06009_002E", "B06009_003E", "B06009_004E"]]
    df.rename(columns={"NAME": "County", "B01001_001E": "Total population", "B06009_002E": "Japanese", "B06009_003E": "Filipino", "B06009_004E": "Chinese"}, inplace=True)
    df["County"] = df["County"].str.replace(" County,", "")  # Remove " County" from the county names
    df["County"] = df["County"].str.replace(" California", "")  # Remove " California" from the county names
    
    df["Chinese"] = df["Chinese"].astype(int)
    df["Japanese"] = df["Japanese"].astype(int)
    df["Filipino"] = df["Filipino"].astype(int)
    df["Total population"] = df["Total population"].astype(int)
    df["Chinese_pct"] = df["Chinese"] / df["Total population"]
    df["Japanese_pct"] = df["Japanese"] / df["Total population"]
    df["Filipino_pct"] = df["Filipino"] / df["Total population"]

    return df



def main():
    # Load the data
    df = load_data()

    st.markdown("<style>h1 {font-size: 16pt;}</style><h1>% of CA county for Japanese or Filipino or Chinese demos</h1>", unsafe_allow_html=True)
    st.markdown("<style>h2 {font-style: italic; font-size: 12pt;}</style><h2>data derived from 2020 US Census ACS data</h2>", unsafe_allow_html=True)

    # Sort the counties alphabetically
    df = df.sort_values("County")

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(df)

    # Add a multiselect to select one or more counties
    county_names = st.multiselect("Select one or more counties: (Sacramento & San Francisco are pre-selected as an example)", df["County"].tolist(), ["Sacramento", "San Francisco"])

    # Filter the data for the selected counties
    county_df = df[df["County"].isin(county_names)]

    # Add a multiselect to select one or more ethnic groups
    ethnic_groups = st.multiselect("Select one or more ethnic groups: (Japanese & Filipino are pre-selected as an example)", ["Japanese", "Filipino", "Chinese"], ["Japanese", "Filipino"])

    # Create a new column that represents the sum of the selected ethnic groups as a percentage of the total population
    county_df["Selected ethnic groups"] = county_df[ethnic_groups].sum(axis=1) / county_df["Total population"]

    # Create a plot using Seaborn
    sns.set_style("darkgrid")
    figure, ax = plt.subplots()
    plot = sns.barplot(x="County", y="Selected ethnic groups", data=county_df)


    # Add labels to the bars
    for p in ax.patches:
        ax.text(p.get_x() + p.get_width()/2., p.get_height(), '{:.1%}'.format(p.get_height()), 
            ha="center", va="bottom", fontsize=11)

    plot.set_title(f"Selected Ethnic Groups as % of California Counties")
    plot.set_xlabel("County")
    plot.set_ylabel("Percentage of total population")

    # Get the underlying figure from the plot
    figure = plot.get_figure()

    # Display the plot in the app using st.pyplot
    st.pyplot(figure)

if __name__ == "__main__":
    main()
