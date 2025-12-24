import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_spotify_data

st.set_page_config(
    page_title="Spotify Analytics Dashboard",
    page_icon="🎵",
    layout="wide"
)

@st.cache_data
def get_data():
    high_pop_df, low_pop_df = load_spotify_data()
    high_pop_df['popularity_category'] = 'High'
    low_pop_df['popularity_category'] = 'Low'
    combined_df = pd.concat([high_pop_df, low_pop_df], ignore_index=True)
    return high_pop_df, low_pop_df, combined_df

high_pop, low_pop, combined = get_data()

st.title("🎵 Spotify Listening Patterns Analytics")
st.markdown("### Business Intelligence Dashboard for Music Strategy Decisions")
st.markdown("---")

st.sidebar.header("📊 Dashboard Controls")
st.sidebar.markdown("Use the filters below to explore the data")

selected_page = st.sidebar.selectbox(
    "Select Analysis Section:",
    ["Overview", "Popularity Analysis", "Genre Insights", "Audio Features", "Artist Analysis", "Recommendations"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Dataset Info**")
st.sidebar.metric("High Popularity Songs", f"{len(high_pop):,}")
st.sidebar.metric("Low Popularity Songs", f"{len(low_pop):,}")
st.sidebar.metric("Total Songs", f"{len(combined):,}")

# Main content area based on selected page
if selected_page == "Overview":
    st.header("📊 Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_popularity_high = high_pop['track_popularity'].mean()
        st.metric("Avg Popularity (High)", f"{avg_popularity_high:.1f}")
    
    with col2:
        avg_popularity_low = low_pop['track_popularity'].mean()
        st.metric("Avg Popularity (Low)", f"{avg_popularity_low:.1f}")
    
    with col3:
        total_genres = combined['playlist_genre'].nunique()
        st.metric("Total Genres", total_genres)
    
    with col4:
        total_artists = combined['track_artist'].nunique()
        st.metric("Unique Artists", f"{total_artists:,}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Genre Distribution")
        genre_counts = combined['playlist_genre'].value_counts()
        fig = px.pie(
            values=genre_counts.values,
            names=genre_counts.index,
            title="Songs by Genre",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Popularity Category Split")
        pop_counts = combined['popularity_category'].value_counts()
        fig = px.bar(
            x=pop_counts.index,
            y=pop_counts.values,
            labels={'x': 'Category', 'y': 'Number of Songs'},
            title="High vs Low Popularity",
            color=pop_counts.index,
            color_discrete_map={'High': '#1DB954', 'Low': '#FF6B6B'}
        )
        st.plotly_chart(fig, use_container_width=True)

elif selected_page == "Popularity Analysis":
    st.header("🎯 What Makes Songs Popular?")
    
    st.subheader("Audio Features: High vs Low Popularity")
    
    audio_features = ['danceability', 'energy', 'loudness', 'speechiness', 
                     'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    
    high_means = high_pop[audio_features].mean()
    low_means = low_pop[audio_features].mean()
    
    comparison_df = pd.DataFrame({
        'Feature': audio_features,
        'High Popularity': high_means.values,
        'Low Popularity': low_means.values
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='High Popularity',
        x=comparison_df['Feature'],
        y=comparison_df['High Popularity'],
        marker_color='#1DB954'
    ))
    fig.add_trace(go.Bar(
        name='Low Popularity',
        x=comparison_df['Feature'],
        y=comparison_df['Low Popularity'],
        marker_color='#FF6B6B'
    ))
    
    fig.update_layout(
        barmode='group',
        title='Average Audio Features Comparison',
        xaxis_title='Audio Feature',
        yaxis_title='Average Value',
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("💡 Key Insights")
    
    comparison_df['Difference'] = comparison_df['High Popularity'] - comparison_df['Low Popularity']
    comparison_df['Abs_Difference'] = comparison_df['Difference'].abs()
    top_differences = comparison_df.nlargest(3, 'Abs_Difference')
    
    col1, col2, col3 = st.columns(3)
    
    for idx, (col, row) in enumerate(zip([col1, col2, col3], top_differences.itertuples())):
        with col:
            direction = "higher" if row.Difference > 0 else "lower"
            st.metric(
                label=f"Top {idx+1}: {row.Feature.capitalize()}",
                value=f"{abs(row.Difference):.3f}",
                delta=f"{direction} in popular songs"
            )
elif selected_page == "Genre Insights":
    st.header("🎸 Genre Performance Analysis")
    
    # Genre popularity comparison
    st.subheader("Average Popularity by Genre")
    
    genre_popularity = combined.groupby(['playlist_genre', 'popularity_category'])['track_popularity'].mean().reset_index()
    
    fig = px.bar(
        genre_popularity,
        x='playlist_genre',
        y='track_popularity',
        color='popularity_category',
        barmode='group',
        title='Average Track Popularity Across Genres',
        labels={'track_popularity': 'Average Popularity', 'playlist_genre': 'Genre'},
        color_discrete_map={'High': '#1DB954', 'Low': '#FF6B6B'}
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Genre audio characteristics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Genre Energy & Danceability")
        genre_features = combined.groupby('playlist_genre')[['energy', 'danceability']].mean().reset_index()
        
        fig = px.scatter(
            genre_features,
            x='energy',
            y='danceability',
            text='playlist_genre',
            size=[20]*len(genre_features),
            title='Genre Positioning',
            labels={'energy': 'Energy Level', 'danceability': 'Danceability'}
        )
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top 5 Genres by Song Count")
        top_genres = combined['playlist_genre'].value_counts().head(5)
        
        fig = px.bar(
            x=top_genres.values,
            y=top_genres.index,
            orientation='h',
            title='Most Common Genres',
            labels={'x': 'Number of Songs', 'y': 'Genre'},
            color=top_genres.values,
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Business recommendations
    st.subheader("📊 Genre Strategy Insights")
    
    # Find best performing genre
    best_genre = combined.groupby('playlist_genre')['track_popularity'].mean().idxmax()
    best_genre_pop = combined.groupby('playlist_genre')['track_popularity'].mean().max()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Best Performing Genre", best_genre, f"{best_genre_pop:.1f} avg popularity")
    
    with col2:
        genre_count = combined['playlist_genre'].nunique()
        st.metric("Total Genres", genre_count)
    
    with col3:
        most_common = combined['playlist_genre'].value_counts().index[0]
        st.metric("Most Common Genre", most_common)

elif selected_page == "Audio Features":
    st.header("🎵 Deep Dive: Audio Features")
    
    # Feature selection
    st.subheader("Interactive Feature Explorer")
    
    audio_features = ['danceability', 'energy', 'loudness', 'speechiness', 
                     'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    
    selected_feature = st.selectbox("Select an audio feature to explore:", audio_features)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution comparison
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=high_pop[selected_feature],
            name='High Popularity',
            marker_color='#1DB954',
            opacity=0.7
        ))
        fig.add_trace(go.Histogram(
            x=low_pop[selected_feature],
            name='Low Popularity',
            marker_color='#FF6B6B',
            opacity=0.7
        ))
        fig.update_layout(
            title=f'{selected_feature.capitalize()} Distribution',
            xaxis_title=selected_feature.capitalize(),
            yaxis_title='Count',
            barmode='overlay',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Box plot comparison
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=high_pop[selected_feature],
            name='High Popularity',
            marker_color='#1DB954'
        ))
        fig.add_trace(go.Box(
            y=low_pop[selected_feature],
            name='Low Popularity',
            marker_color='#FF6B6B'
        ))
        fig.update_layout(
            title=f'{selected_feature.capitalize()} Box Plot',
            yaxis_title=selected_feature.capitalize(),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Correlation heatmap
    st.subheader("Feature Correlations with Popularity")
    
    correlation_data = combined[audio_features + ['track_popularity']].corr()['track_popularity'].drop('track_popularity').sort_values(ascending=False)
    
    fig = px.bar(
        x=correlation_data.values,
        y=correlation_data.index,
        orientation='h',
        title='Correlation with Track Popularity',
        labels={'x': 'Correlation Coefficient', 'y': 'Audio Feature'},
        color=correlation_data.values,
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected_page == "Artist Analysis":
    st.header("🎤 Artist Performance Insights")
    
    # Top artists by track count
    st.subheader("Most Prolific Artists")
    
    top_artists_count = combined['track_artist'].value_counts().head(10)
    
    fig = px.bar(
        x=top_artists_count.values,
        y=top_artists_count.index,
        orientation='h',
        title='Top 10 Artists by Number of Tracks',
        labels={'x': 'Number of Tracks', 'y': 'Artist'},
        color=top_artists_count.values,
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Top artists by average popularity
    st.subheader("Highest Average Popularity")
    
    # Filter artists with at least 3 songs
    artist_stats = combined.groupby('track_artist').agg({
        'track_popularity': ['mean', 'count']
    }).reset_index()
    artist_stats.columns = ['artist', 'avg_popularity', 'track_count']
    artist_stats_filtered = artist_stats[artist_stats['track_count'] >= 3].sort_values('avg_popularity', ascending=False).head(10)
    
    fig = px.bar(
        artist_stats_filtered,
        x='avg_popularity',
        y='artist',
        orientation='h',
        title='Top 10 Artists by Average Popularity (min 3 tracks)',
        labels={'avg_popularity': 'Average Popularity', 'artist': 'Artist'},
        color='avg_popularity',
        color_continuous_scale='Greens'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Artist genre distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Artist Success Rate")
        
        artist_success = combined.groupby('track_artist')['popularity_category'].apply(
            lambda x: (x == 'High').sum() / len(x) * 100
        ).sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=artist_success.values,
            y=artist_success.index,
            orientation='h',
            title='Top 10 Artists - % High Popularity Tracks',
            labels={'x': 'Success Rate (%)', 'y': 'Artist'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Key Artist Metrics")
        
        total_artists = combined['track_artist'].nunique()
        avg_tracks_per_artist = combined.groupby('track_artist').size().mean()
        top_artist = combined['track_artist'].value_counts().index[0]
        
        st.metric("Total Unique Artists", f"{total_artists:,}")
        st.metric("Avg Tracks per Artist", f"{avg_tracks_per_artist:.1f}")
        st.metric("Most Prolific Artist", top_artist)

elif selected_page == "Recommendations":
    st.header("💼 Business Recommendations")
    
    st.markdown("""
    Based on the analysis of 4,831 tracks across high and low popularity categories,
    here are key actionable insights for music strategy decisions:
    """)
    
    st.markdown("---")
    
    # Calculate key insights
    audio_features = ['danceability', 'energy', 'loudness', 'speechiness', 
                     'acousticness', 'instrumentalness', 'liveness', 'valence']
    
    high_means = high_pop[audio_features].mean()
    low_means = low_pop[audio_features].mean()
    differences = (high_means - low_means).abs().sort_values(ascending=False)
    
    best_genre = combined.groupby('playlist_genre')['track_popularity'].mean().idxmax()
    best_genre_pop = combined.groupby('playlist_genre')['track_popularity'].mean().max()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 1. Audio Feature Optimization")
        st.markdown(f"""
        **Top differentiating features:**
        - **{differences.index[0].capitalize()}**: Biggest difference between high/low popularity
        - **{differences.index[1].capitalize()}**: Second most important factor
        - **{differences.index[2].capitalize()}**: Third key differentiator
        
        **Recommendation:** Focus on optimizing these features when selecting or promoting tracks.
        Analyze successful tracks to understand the ideal range for each feature.
        """)
        
        st.subheader("🎸 2. Genre Strategy")
        st.markdown(f"""
        **Best performing genre:** {best_genre} (avg popularity: {best_genre_pop:.1f})
        
        **Recommendation:** 
        - Increase playlist representation of {best_genre}
        - Study what makes {best_genre} tracks successful
        - Consider cross-genre collaborations featuring {best_genre} elements
        """)
    
    with col2:
        st.subheader("👥 3. Artist Development")
        
        high_pop_artists = high_pop['track_artist'].nunique()
        low_pop_artists = low_pop['track_artist'].nunique()
        
        st.markdown(f"""
        **Artist distribution:**
        - High popularity: {high_pop_artists} unique artists
        - Low popularity: {low_pop_artists} unique artists
        
        **Recommendation:**
        - Identify emerging artists with high-performing features
        - Invest in artist development for those showing promise
        - Create mentorship programs pairing high/low popularity artists
        """)
        
        st.subheader("📊 4. Playlist Curation")
        st.markdown("""
        **Recommendation:**
        - Balance energy and danceability in playlists
        - Use data-driven feature matching for better user engagement
        - Test A/B variants with different feature combinations
        - Monitor engagement metrics for continuous optimization
        """)
    
    st.markdown("---")
    
    st.subheader("🚀 Next Steps")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Short-term (1-3 months)**
        - Audit current playlists
        - Rebalance genre distribution
        - A/B test feature optimization
        """)
    
    with col2:
        st.markdown("""
        **Mid-term (3-6 months)**
        - Develop artist partnerships
        - Launch data-driven campaigns
        - Build prediction models
        """)
    
    with col3:
        st.markdown("""
        **Long-term (6-12 months)**
        - Create automated curation
        - Expand to new genres
        - Build competitive advantage
        """)   