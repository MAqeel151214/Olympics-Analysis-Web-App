import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import preprocessing, helper
import ui_utils
from chart_utils import (
    style_chart, styled_line, styled_heatmap,
    ACCENT, TEAL, YELLOW, PURPLE, PINK,
    MEDAL_COLORS, SEASON_COLORS, GENDER_COLORS, COLOR_SEQUENCE,
)

# ── Page config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Olympics Analysis Dashboard",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Asset Setup ──────────────────────────────────────────────────────────────────
try:
    BG_BASE64 = ui_utils.get_image_base64("assets/olympic_bg.png")
except Exception:
    BG_BASE64 = ""

# ── Custom CSS ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Background Image Injection */
    .stApp {{
        background-image: url("data:image/png;base64,{BG_BASE64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    html, body, [class*="st-"] {{ font-family: 'Inter', sans-serif; }}

    /* Glassmorphism Metric Cards */
    div[data-testid="stMetric"] {{
        background: rgba(26, 31, 46, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 107, 53, 0.3);
        border-radius: 12px; padding: 16px 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 32px 0 rgba(255, 107, 53, 0.25);
    }}
    div[data-testid="stMetric"] label {{
        color: #FF6B35 !important; font-weight: 600;
        font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;
    }}
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
        font-size: 2rem; font-weight: 700; color: #FAFAFA;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background: rgba(14, 17, 23, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 107, 53, 0.2);
    }}
    
    /* Dataframes and Charts Backgrounds */
    .stPlotlyChart {{ border-radius: 12px; overflow: hidden; }}
    .stDataFrame, .stTable {{ 
        border-radius: 8px; 
        overflow: hidden;
    }}
    
    hr {{ border-color: rgba(255, 255, 255, 0.1); }}
    
    .footer {{
        text-align: center; color: #aaa; font-size: 0.8rem;
        padding: 20px 0; border-top: 1px solid rgba(255, 255, 255, 0.1); margin-top: 40px;
        background: rgba(0,0,0,0.3); border-radius: 8px;
    }}
    .footer a {{ color: #FF6B35; text-decoration: none; font-weight: 600; }}
    
    .season-badge {{
        display: inline-block; padding: 4px 12px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 600; margin-right: 6px;
    }}
    .summer-badge {{ background: rgba(255,107,53,0.15); color: #FF6B35; border: 1px solid #FF6B35; }}
    .winter-badge {{ background: rgba(96,165,250,0.15); color: #60A5FA; border: 1px solid #60A5FA; }}
</style>
""", unsafe_allow_html=True)


# ── Data loading ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load and preprocess Olympics data with caching."""
    try:
        df = pd.read_csv('athlete_events.csv')
        region_df = pd.read_csv('noc_regions.csv')
        df = preprocessing.preprocess(df, region_df)
        return df
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e.filename}")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()


with st.spinner("Loading Olympics data..."):
    df_all = load_data()


# ── Utility for Flags in Dataframes ──────────────────────────────────────────────
def _get_iso3_from_region(df_ref, region_name):
    # Lookup NOC from region name using the original dataframe
    subset = df_ref[df_ref['region'] == region_name]
    if not subset.empty:
        noc = subset.iloc[0]['NOC']
        from helper import _noc_to_iso3
        return _noc_to_iso3(noc)
    return "UNKNOWN"

def inject_flags(target_df, region_col='region'):
    """Adds a 'Flag' column with image URLs to a dataframe based on its region."""
    if region_col in target_df.columns:
        # Create a mapping for performance
        unique_regions = target_df[region_col].unique()
        flag_map = {}
        for r in unique_regions:
            iso = _get_iso3_from_region(df_all, r)
            flag_map[r] = ui_utils.get_flag_url(iso)
        
        # Insert Flag as the first column visually
        cols = target_df.columns.tolist()
        target_df['Flag'] = target_df[region_col].map(flag_map)
        new_cols = ['Flag'] + [c for c in cols if c != 'Flag']
        return target_df[new_cols]
    return target_df


# ── Sidebar Setup ───────────────────────────────────────────────────────────────
try:
    st.sidebar.image("assets/sidebar_logo.png", use_container_width=True)
except Exception:
    pass

st.sidebar.title('🏅 Olympics Analysis')

season_option = st.sidebar.selectbox(
    'Season Filter',
    ['☀️ Summer', '❄️ Winter', '🏅 Both'],
    index=0,
    help="Filter all data across the dashboard by Olympic season."
)

SEASON_MAP = {'☀️ Summer': 'Summer', '❄️ Winter': 'Winter', '🏅 Both': 'Both'}
selected_season = SEASON_MAP[season_option]

if selected_season == 'Both':
    df = df_all.copy()
else:
    df = df_all[df_all['Season'] == selected_season].copy()

st.sidebar.divider()

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis',
     'Athlete wise Analysis', '🌍 Medal Map', '⚔️ Country Comparison',
     '☀️❄️ Summer vs Winter'),
    help="Navigate between different analytical views."
)


# ═════════════════════════════════════════════════════════════════════════════════
# TAB: Medal Tally
# ═════════════════════════════════════════════════════════════════════════════════
if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    country, years = helper.country_year_list(df)
    
    # Custom formatters for dropdowns
    def format_country(c):
        if c == 'Overall': return '🌍 Overall'
        iso = _get_iso3_from_region(df_all, c)
        return f"{ui_utils.get_country_emoji(iso)} {c}"

    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country, format_func=format_country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('🌍 Medal Tally of All Time')
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f'🗓️ Medal Tally in {selected_year}')
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f'{format_country(selected_country)} Medal Tally — All Years')
    else:
        st.title(f'{format_country(selected_country)} Medal Tally in {selected_year}')

    # Inject flags and format dataframe
    tally_display = inject_flags(medal_tally)
    tally_display = tally_display.rename(columns={'Gold': '🥇 Gold', 'Silver': '🥈 Silver', 'Bronze': '🥉 Bronze'})
    
    st.dataframe(
        tally_display, 
        use_container_width=True,
        column_config={
            "Flag": st.column_config.ImageColumn("Flag", width="small"),
            "🥇 Gold": st.column_config.NumberColumn(format="%d 🥇"),
            "🥈 Silver": st.column_config.NumberColumn(format="%d 🥈"),
            "🥉 Bronze": st.column_config.NumberColumn(format="%d 🥉"),
        }
    )

    csv = medal_tally.to_csv(index=False)
    st.download_button("📥 Download as CSV", data=csv, file_name="medal_tally.csv", mime="text/csv", help="Download the current medal tally view as a CSV file for offline analysis.")

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.subheader('Top 15 Countries — Medal Breakdown')
        top15 = medal_tally.head(15)
        fig = go.Figure()
        for medal, color in [('Gold', MEDAL_COLORS['Gold']),
                             ('Silver', MEDAL_COLORS['Silver']),
                             ('Bronze', MEDAL_COLORS['Bronze'])]:
            fig.add_trace(go.Bar(
                y=top15['region'], x=top15[medal],
                name=medal, orientation='h', marker_color=color,
            ))
        fig.update_layout(barmode='stack', yaxis=dict(autorange='reversed'))
        style_chart(fig, height=500)
        st.plotly_chart(fig, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════════
# TAB: Overall Analysis
# ═════════════════════════════════════════════════════════════════════════════════
if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].dropna().unique().shape[0]

    st.title('📈 Top Statistics')
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Editions 🗓️", f"{editions:,}")
    with col2: st.metric("Host Cities 🏙️", f"{cities:,}")
    with col3: st.metric("Sports 🏅", f"{sports:,}")

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Events 🏁", f"{events:,}")
    with col2: st.metric("Athletes 🏃", f"{athletes:,}")
    with col3: st.metric("Nations 🌍", f"{nations:,}")

    st.divider()

    all_years = sorted(df['Year'].unique())
    if len(all_years) >= 2:
        yr_min, yr_max = st.slider('Filter Year Range', min_value=int(all_years[0]), max_value=int(all_years[-1]), value=(int(all_years[0]), int(all_years[-1])))
        df_filtered = df[(df['Year'] >= yr_min) & (df['Year'] <= yr_max)]
    else:
        df_filtered = df

    nations_ot = helper.data_over_time(df_filtered, 'region')
    fig = px.line(nations_ot, x='Edition', y='Number of Nations', title='🌍 Participating Nations Over Time')
    st.plotly_chart(styled_line(fig, ACCENT), use_container_width=True)

    events_ot = helper.data_over_time(df_filtered, 'Event')
    fig = px.line(events_ot, x='Edition', y='Number of Events', title='🏁 Events Over Time')
    st.plotly_chart(styled_line(fig, TEAL), use_container_width=True)

    athletes_ot = helper.data_over_time(df_filtered, 'Name')
    fig = px.line(athletes_ot, x='Edition', y='Number of Athletes', title='🏃 Athletes Over Time')
    st.plotly_chart(styled_line(fig, YELLOW), use_container_width=True)

    st.title("🔥 Number of Events Over Time (Every Sport)")
    with st.spinner("Rendering heatmap..."):
        x = df_filtered.drop_duplicates(['Year', 'Sport', 'Event'])
        heatmap_data = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
        fig = px.imshow(heatmap_data, text_auto=True, aspect='auto', color_continuous_scale='OrRd')
        fig.update_layout(xaxis_title='Year', yaxis_title='Sport')
        st.plotly_chart(styled_heatmap(fig, len(heatmap_data)), use_container_width=True)

    st.title("🌟 Most Successful Athletes")
    sport_list = sorted(df['Sport'].unique().tolist())
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list, format_func=lambda s: f"{ui_utils.get_sport_icon(s)} {s}")
    
    top_athletes = helper.most_successful(df, selected_sport)
    top_display = inject_flags(top_athletes)
    
    st.dataframe(
        top_display, 
        use_container_width=True,
        column_config={
            "Flag": st.column_config.ImageColumn("Flag", width="small")
        }
    )


# ═════════════════════════════════════════════════════════════════════════════════
# TAB: Country-wise Analysis
# ═════════════════════════════════════════════════════════════════════════════════
if user_menu == 'Country-wise Analysis':
    country, years = helper.country_year_list(df)
    country_filtered = [c for c in country if c != 'Overall']
    
    def format_country(c):
        iso = _get_iso3_from_region(df_all, c)
        return f"{ui_utils.get_country_emoji(iso)} {c}"

    selected_country = st.sidebar.selectbox('Select Country', country_filtered, format_func=format_country)
    yearwise_medal = helper.yearwise_medal_tally(df, selected_country)

    st.title(f'{format_country(selected_country)} Medal Tally Trend')
    fig = px.line(yearwise_medal, x='Year', y='Medal')
    st.plotly_chart(styled_line(fig, ACCENT), use_container_width=True)

    st.title(f"{format_country(selected_country)} excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    if pt.empty:
        st.info(f"No medal data available for {selected_country}")
    else:
        with st.spinner("Rendering heatmap..."):
            pt = pt.astype(int)
            fig = px.imshow(pt, text_auto=True, aspect='auto', color_continuous_scale='OrRd')
            fig.update_layout(xaxis_title='Year', yaxis_title='Sport')
            st.plotly_chart(styled_heatmap(fig, len(pt), row_height=28), use_container_width=True)

    st.title(f'🌟 Top 10 Athletes of {format_country(selected_country)}')
    top10 = helper.most_successful(df, 'Overall', country=selected_country, top_n=10)
    st.dataframe(top10, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════════
# TAB: Athlete-wise Analysis
# ═════════════════════════════════════════════════════════════════════════════════
if user_menu == 'Athlete wise Analysis':
    st.title('🏃 Athlete-wise Analysis')

    st.subheader('🔍 Athlete Search')
    search_query = st.text_input('Search by athlete name', placeholder='e.g. Usain, Nadia, Phelps...', help="Type part or full name of an athlete to view their Olympic history.")
    if search_query:
        results = helper.search_athlete(df, search_query)
        if results.empty:
            st.warning(f'No athletes found matching "{search_query}". Try using a partial name or checking the spelling.')
        else:
            n_athletes = results['Name'].nunique()
            st.success(f'Found {n_athletes} athlete(s) with {len(results)} records')
            st.dataframe(inject_flags(results), use_container_width=True, height=400,
                         column_config={"Flag": st.column_config.ImageColumn("Flag")})

    st.divider()
    
    st.subheader('🎂 Age Distribution of Athletes')
    age_df = df.dropna(subset=['Age'])
    fig = px.histogram(age_df, x='Age', nbins=50, color_discrete_sequence=[ACCENT])
    st.plotly_chart(style_chart(fig), use_container_width=True)

    st.subheader('🥇 Age Distribution by Medal Type')
    medal_age_df = df.dropna(subset=['Age', 'Medal'])
    fig = px.box(medal_age_df, x='Medal', y='Age', color='Medal', color_discrete_map=MEDAL_COLORS)
    st.plotly_chart(style_chart(fig), use_container_width=True)

    st.subheader('🏋️ BMI Analysis by Sport')
    bmi_stats = helper.compute_bmi_stats(df)
    if not bmi_stats.empty:
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = px.bar(bmi_stats.head(20), x='Avg BMI', y='Sport', orientation='h', color='Avg BMI', color_continuous_scale='OrRd')
            fig.update_layout(yaxis=dict(autorange='reversed'))
            st.plotly_chart(style_chart(fig, height=600), use_container_width=True)
        with col2:
            st.dataframe(bmi_stats, use_container_width=True, height=600)

        bmi_dist = helper.get_bmi_distribution(df)
        sport_for_bmi = st.selectbox('Select Sport for BMI distribution',
                                     ['All'] + sorted(bmi_dist['Sport'].unique().tolist()),
                                     format_func=lambda s: f"{ui_utils.get_sport_icon(s)} {s}")
        if sport_for_bmi != 'All':
            bmi_dist = bmi_dist[bmi_dist['Sport'] == sport_for_bmi]

        fig = px.histogram(bmi_dist, x='BMI', nbins=60, color='Sex', color_discrete_map=GENDER_COLORS, barmode='overlay', opacity=0.7)
        st.plotly_chart(style_chart(fig), use_container_width=True)

    st.divider()
    st.subheader('🏆 Repeat Medalists')
    min_ed = st.slider('Minimum Olympic editions with medals', 2, 6, 3)
    repeat_df = helper.get_repeat_medalists(df, min_editions=min_ed)
    if repeat_df.empty:
        st.info('No athletes found with that many editions.')
    else:
        st.success(f'{len(repeat_df)} athletes medaled across {min_ed}+ editions')
        st.dataframe(inject_flags(repeat_df), use_container_width=True, height=500,
                     column_config={"Flag": st.column_config.ImageColumn("Flag")})


# ═════════════════════════════════════════════════════════════════════════════════
# TAB: Medal Map
# ═════════════════════════════════════════════════════════════════════════════════
if user_menu == '🌍 Medal Map':
    st.title('🌍 World Medal Map')
    medal_type = st.selectbox('Color by', ['Total', 'Gold', 'Silver', 'Bronze'])
    choro_data = helper.get_choropleth_data(df)
    
    fig = px.choropleth(
        choro_data, locations='ISO3', color=medal_type, hover_name='region',
        hover_data={'Gold': True, 'Silver': True, 'Bronze': True, 'Total': True, 'ISO3': False},
        color_continuous_scale='OrRd', title=f'{medal_type} Medals by Country',
    )
    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=True, coastlinecolor='#333', landcolor='rgba(26,31,46,0.5)', bgcolor='rgba(0,0,0,0)', lakecolor='rgba(14,17,23,0.5)'),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family='Inter', color='#FAFAFA'), height=600,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader('📊 Medal Standings')
    display_map_df = inject_flags(choro_data[['region', 'Gold', 'Silver', 'Bronze', 'Total']].head(30))
    display_map_df = display_map_df.rename(columns={'Gold': '🥇 Gold', 'Silver': '🥈 Silver', 'Bronze': '🥉 Bronze'})
    st.dataframe(display_map_df, use_container_width=True,
                 column_config={"Flag": st.column_config.ImageColumn("Flag", width="small")})


# ═════════════════════════════════════════════════════════════════════════════════
# TAB: Country Comparison
# ═════════════════════════════════════════════════════════════════════════════════
if user_menu == '⚔️ Country Comparison':
    st.title('⚔️ Head-to-Head Country Comparison')
    countries_list = sorted([c for c in df['region'].dropna().unique()])

    def format_country(c):
        iso = _get_iso3_from_region(df_all, c)
        return f"{ui_utils.get_country_emoji(iso)} {c}"

    col1, col2 = st.columns(2)
    with col1:
        c1 = st.selectbox('Country 1', countries_list, index=countries_list.index('USA') if 'USA' in countries_list else 0, format_func=format_country)
    with col2:
        c2 = st.selectbox('Country 2', countries_list, index=countries_list.index('China') if 'China' in countries_list else 1, format_func=format_country)

    if c1 == c2:
        st.warning('Please select two different countries to compare their head-to-head metrics.')
    else:
        comp = helper.compare_countries(df, c1, c2)
        st.subheader('📊 Summary')
        metrics = ['Total Medals', 'Gold', 'Silver', 'Bronze', 'Athletes', 'Sports', 'Editions']
        cols = st.columns(len(metrics))
        for i, m in enumerate(metrics):
            with cols[i]:
                v1, v2 = comp[c1][m], comp[c2][m]
                delta = v1 - v2
                st.metric(m, f"{v1:,}", delta=f"{delta:+,} vs {c2}" if delta != 0 else "Tied")

        st.divider()
        st.subheader('📈 Medal Trends Over Time')
        ym1 = helper.yearwise_medal_tally(df, c1).rename(columns={'Medal': c1})
        ym2 = helper.yearwise_medal_tally(df, c2).rename(columns={'Medal': c2})
        merged = pd.merge(ym1, ym2, on='Year', how='outer').fillna(0).sort_values('Year')

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=merged['Year'], y=merged[c1], name=c1, line=dict(color=ACCENT, width=2.5)))
        fig.add_trace(go.Scatter(x=merged['Year'], y=merged[c2], name=c2, line=dict(color=TEAL, width=2.5)))
        fig.update_layout(yaxis_title='Medals')
        st.plotly_chart(style_chart(fig, height=400), use_container_width=True)

        st.subheader('🏅 Sport Overlap')
        shared, only1, only2 = helper.get_sport_overlap(df, c1, c2)
        col1_, col2_, col3_ = st.columns(3)
        with col1_:
            st.markdown(f'**🤝 Shared ({len(shared)})**')
            st.write('  '.join(f"{ui_utils.get_sport_icon(s)} {s}" for s in sorted(shared)) if shared else 'None')
        with col2_:
            st.markdown(f'**🔶 Only {format_country(c1)} ({len(only1)})**')
            st.write('  '.join(f"{ui_utils.get_sport_icon(s)} {s}" for s in sorted(only1)) if only1 else 'None')
        with col3_:
            st.markdown(f'**🔷 Only {format_country(c2)} ({len(only2)})**')
            st.write('  '.join(f"{ui_utils.get_sport_icon(s)} {s}" for s in sorted(only2)) if only2 else 'None')


# ═════════════════════════════════════════════════════════════════════════════════
# TAB: Summer vs Winter
# ═════════════════════════════════════════════════════════════════════════════════
if user_menu == '☀️❄️ Summer vs Winter':
    st.title('☀️ Summer vs ❄️ Winter Olympics')
    sc = helper.get_season_comparison(df_all)

    st.subheader('📊 Overview Comparison')
    metrics_list = ['Editions', 'Host Cities', 'Sports', 'Events', 'Athletes', 'Nations']
    col_summer, col_winter = st.columns(2)
    with col_summer:
        st.markdown('<span class="season-badge summer-badge">☀️ SUMMER</span>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, m in enumerate(metrics_list):
            with cols[i % 3]: st.metric(m, f"{sc['Summer'][m]:,}")
    with col_winter:
        st.markdown('<span class="season-badge winter-badge">❄️ WINTER</span>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, m in enumerate(metrics_list):
            with cols[i % 3]: st.metric(m, f"{sc['Winter'][m]:,}")

    st.divider()
    st.subheader('🥇 Medal Dominance — Top 15 Countries')
    dom = helper.get_season_medal_dominance(df_all, top_n=15)
    fig = go.Figure()
    fig.add_trace(go.Bar(y=dom['region'], x=dom['Summer'], name='☀️ Summer', orientation='h', marker_color=SEASON_COLORS['Summer']))
    fig.add_trace(go.Bar(y=dom['region'], x=dom['Winter'], name='❄️ Winter', orientation='h', marker_color=SEASON_COLORS['Winter']))
    fig.update_layout(barmode='stack', yaxis=dict(autorange='reversed'), xaxis_title='Total Medals')
    st.plotly_chart(style_chart(fig, height=500), use_container_width=True)

    st.divider()
    st.subheader('🌟 Crossover Athletes (Competed in Both Seasons)')
    with st.spinner("Finding crossover athletes..."):
        cross = helper.get_crossover_athletes(df_all)
    if cross.empty:
        st.info('No crossover athletes found.')
    else:
        st.success(f'{len(cross)} athletes competed in both Summer & Winter Olympics!')
        st.dataframe(inject_flags(cross), use_container_width=True, height=500,
                     column_config={"Flag": st.column_config.ImageColumn("Flag", width="small")})


# ── Footer ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    📊 Data source: <a href="https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results" target="_blank">120 Years of Olympic History</a> (Kaggle) &nbsp;|&nbsp;
    Built with <a href="https://streamlit.io" target="_blank">Streamlit</a> & <a href="https://plotly.com" target="_blank">Plotly</a>
</div>
""", unsafe_allow_html=True)
