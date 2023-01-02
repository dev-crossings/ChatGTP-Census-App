import streamlit as st
import requests
import pandas as pd
import seaborn as sns

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

    # Sort the counties alphabetically
    df = df.sort_values("County")



    st.markdown("<style>h1 {font-size: 16pt;}</style><h1>% of CA county for Japanese or Filipino or Chinese demos</h1>", unsafe_allow_html=True)
    st.markdown("<style>h2 {font-style: italic; font-size: 12pt;}</style><h2>data derived from 2020 US Census ACS data</h2>", unsafe_allow_html=True)


    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(df)



    # Add a multiselect to select one or more counties
    county_names = st.multiselect("Select one or more counties: (Sacramento & San Francisco are pre-selected as an example)", df["County"].tolist(), ["Sacramento", "San Francisco"])

    # Filter the data for the selected counties
    county_df = df[df["County"].isin(county_names)]

    # Add a dropdown menu to select Japanese or Filipino data
    population_type = st.selectbox("Select population type:", ["Japanese", "Filipino", "Chinese"])

    if population_type == "Japanese":
        # Create a plot using Seaborn
        sns.set_style("darkgrid")
        plot = sns.barplot(x="County", y="Japanese_pct", data=county_df)
        plot.set_title("Japanese Population in California Counties")
        plot.set_xlabel("County")
        plot.set_ylabel("Percentage of total population")
    
    elif population_type == "Filipino":
        # Create a plot using Seaborn
        sns.set_style("darkgrid")
        plot = sns.barplot(x="County", y="Filipino_pct", data=county_df)
        plot.set_title("Filipino Population in California Counties")
        plot.set_xlabel("County")
        plot.set_ylabel("Percentage of total population")

    else:
        # Create a plot using Seaborn
        sns.set_style("darkgrid")
        plot = sns.barplot(x="County", y="Chinese_pct", data=county_df)
        plot.set_title("Chinese Population in California Counties")
        plot.set_xlabel("County")
        plot.set_ylabel("Percentage of total population")

    # Get the underlying figure from the plot
    figure = plot.get_figure()

    # Display the plot in the app using st.pyplot
    st.pyplot(figure)


if __name__ == "__main__":
    main()
