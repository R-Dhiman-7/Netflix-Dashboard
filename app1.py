import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Netflix Data Dashboard",layout="wide")
st.title("Netflix Data Analysis Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    return df

df = load_data()
st.sidebar.header("Dashboard Filters")

type_filter = st.sidebar.multiselect(
    "Select Content Type",
    options=df['type'].dropna().unique(),
    default=df['type'].dropna().unique()
)

country_filter = st.sidebar.multiselect(
    "Select Country",
    options=df['country'].dropna().unique()
)

rating_filter = st.sidebar.multiselect(
    "Select Rating",
    options=df['rating'].dropna().unique()
)

year_filter = st.sidebar.slider(
    "Select Release Year",
    int(df.release_year.min()),
    int(df.release_year.max()),
    (2000,2020)
)

filtered_df = df[df['type'].isin(type_filter)]

if country_filter:
    filtered_df = filtered_df[filtered_df['country'].isin(country_filter)]

if rating_filter:
    filtered_df = filtered_df[filtered_df['rating'].isin(rating_filter)]

filtered_df = filtered_df[
    (filtered_df['release_year'] >= year_filter[0]) &
    (filtered_df['release_year'] <= year_filter[1])
]


st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
total_titles = len(filtered_df)
movies = len(filtered_df[filtered_df['type']=="Movie"])
tv_shows = len(filtered_df[filtered_df['type']=="TV Show"])
countries = filtered_df['country'].nunique()

col1.metric("Total Titles", total_titles)
col2.metric("Movies", movies)
col3.metric("TV Shows", tv_shows)
col4.metric("Countries", countries)

st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("Movies vs TV Shows")
    type_count = filtered_df['type'].value_counts()
    fig = px.pie(
        values=type_count.values,
        names=type_count.index,
        color_discrete_sequence=px.colors.sequential.Reds
    )

    st.plotly_chart(fig, width="stretch")


with col2:
    st.subheader("Content Added Over Time")
    yearly = filtered_df['year_added'].value_counts().sort_index()
    fig = px.line(
        x=yearly.index,
        y=yearly.values,
        markers=True
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Titles Added"
    )

    st.plotly_chart(fig, width="stretch")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Countries Producing Content")
    top_countries = (
        filtered_df['country']
        .value_counts()
        .head(10)
    )
    fig = px.bar(
        x=top_countries.values,
        y=top_countries.index,
        orientation="h",
        color=top_countries.values,
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        xaxis_title="Number of Titles",
        yaxis_title="Country"
    )

    st.plotly_chart(fig, width="stretch")


with col2:
    st.subheader("Ratings Distribution")
    rating_counts = filtered_df['rating'].value_counts()

    fig = px.bar(
        x=rating_counts.index,
        y=rating_counts.values,
        color=rating_counts.values,
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        xaxis_title="Rating",
        yaxis_title="Count"
    )

    st.plotly_chart(fig,width="stretch")

st.divider()
st.subheader("Top Genres")
genres = filtered_df['listed_in'].str.split(',').explode()

genre_counts = genres.value_counts().head(10)

fig = px.bar(
    x=genre_counts.index,
    y=genre_counts.values,
    color=genre_counts.values,
    color_continuous_scale="Reds"
)

fig.update_layout(
    xaxis_title="Genre",
    yaxis_title="Number of Titles"
)

st.plotly_chart(fig, width="stretch")

st.divider()
st.subheader("Global Distribution of Netflix Content")
country_counts = filtered_df['country'].value_counts().reset_index()
country_counts.columns = ['country','count']
fig = px.choropleth(
    country_counts,
    locations="country",
    locationmode="country names",
    color="count",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig,width="stretch")

st.divider()
st.subheader("Dataset Preview")
search = st.text_input("Search Title")
if search:
    filtered_df = filtered_df[
        filtered_df['title'].str.contains(search, case=False)
    ]
st.dataframe(filtered_df.head(100))


st.markdown("---")
st.markdown(
    "Netflix Data Dashboard"
)