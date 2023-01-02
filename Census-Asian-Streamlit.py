import streamlit as st
import requests
import pandas as pd
import seaborn as sns

@st.cache
def load_data():
    # Make a request to the US Census API to get the data
    response = requests.get("https://api.census.gov/data/2020/acs/acs5?get=NAME,B01001_001E,B06009_002E,B06009_003E&for=county:*&in=state:06")


    # Convert the response to JSON
    data = response.json()

    # Convert the JSON data to a DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])

    # Clean the data
    df = df[["NAME", "B01001_001E", "B06009_002E", "B06009_003E"]]
    df.rename(columns={"NAME": "County", "B01001_001E": "Total population", "B06009_002E": "Japanese", "B06009_003E": "Filipino"}, inplace=True)
    df["Japanese"] = df["Japanese"].astype(int)
    df["Filipino"] = df["Filipino"].astype(int)
    df["Total population"] = df["Total population"].astype(int)
    df["Japanese_pct"] = df["Japanese"] / df["Total population"]
    df["Filipino_pct"] = df["Filipino"] / df["Total population"]



    return df

def main():
    # Load the data
    df = load_data()

    # Sort the counties alphabetically
    df = df.sort_values("County")

    st.title("Percentage of CA county for either Japanese or Filipino populations")
    st.header("data derived from 2020 US Census ACS data")

    # Add a multiselect to select one or more counties
    county_names = st.multiselect("Select one or more counties:", df["County"].tolist(), ["Sacramento County, California", "San Francisco County, California"])

    # Filter the data for the selected counties
    county_df = df[df["County"].isin(county_names)]

    # Add a dropdown menu to select Japanese or Filipino data
    population_type = st.selectbox("Select population type:", ["Japanese", "Filipino"])

    if population_type == "Japanese":
        # Create a plot using Seaborn
        sns.set_style("darkgrid")
        plot = sns.barplot(x="County", y="Japanese_pct", data=county_df)
        plot.set_title("Japanese Population in California Counties")
        plot.set_xlabel("County")
        plot.set_ylabel("Percentage of total population")
    else:
        # Create a plot using Seaborn
        sns.set_style("darkgrid")
        plot = sns.barplot(x="County", y="Filipino_pct", data=county_df)
        plot.set_title("Filipino Population in California Counties")
        plot.set_xlabel("County")
        plot.set_ylabel("Percentage of total population")

    # Get the underlying figure from the plot
    figure = plot.get_figure()

    # Display the plot in the app using st.pyplot
    st.pyplot(figure)

    st.subheader('Raw data')
    st.write(df)


if __name__ == "__main__":
    main()
