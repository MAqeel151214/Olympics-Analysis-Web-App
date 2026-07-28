import numpy as np
import pandas as pd


# ── NOC → ISO-3 mapping for Plotly choropleth ────────────────────────────────────
# Olympic NOC codes differ from ISO-3166 alpha-3 in ~20 cases.
_NOC_TO_ISO3 = {
    'GER': 'DEU', 'SUI': 'CHE', 'GRE': 'GRC', 'NED': 'NLD',
    'DEN': 'DNK', 'CRO': 'HRV', 'POR': 'PRT', 'BUL': 'BGR',
    'GBR': 'GBR', 'RSA': 'ZAF', 'CHI': 'CHL', 'IRI': 'IRN',
    'MAS': 'MYS', 'PHI': 'PHL', 'NGR': 'NGA', 'TPE': 'TWN',
    'KSA': 'SAU', 'UAE': 'ARE', 'BAH': 'BHS', 'PUR': 'PRI',
    'TTO': 'TTO', 'ISV': 'VIR', 'IVB': 'VGB', 'BER': 'BMU',
    'CAY': 'CYM', 'ANT': 'ATG', 'VIN': 'VCT', 'BAR': 'BRB',
    'SKN': 'KNA', 'LCA': 'LCA', 'GRN': 'GRD', 'DMA': 'DMA',
    'HAI': 'HTI', 'GUA': 'GTM', 'HON': 'HND', 'ESA': 'SLV',
    'NCA': 'NIC', 'CRC': 'CRI', 'PAN': 'PAN', 'PAR': 'PRY',
    'URU': 'URY', 'BOL': 'BOL', 'SRI': 'LKA', 'BAN': 'BGD',
    'MYA': 'MMR', 'CAM': 'KHM', 'LAO': 'LAO', 'VIE': 'VNM',
    'INA': 'IDN', 'SIN': 'SGP', 'BRU': 'BRN', 'TLS': 'TLS',
    'ALG': 'DZA', 'MAR': 'MAR', 'TUN': 'TUN', 'LBA': 'LBY',
    'SUD': 'SDN', 'ETH': 'ETH', 'KEN': 'KEN', 'TAN': 'TZA',
    'UGA': 'UGA', 'RWA': 'RWA', 'BDI': 'BDI', 'MOZ': 'MOZ',
    'MAW': 'MWI', 'ZAM': 'ZMB', 'ZIM': 'ZWE', 'BOT': 'BWA',
    'NAM': 'NAM', 'ANG': 'AGO', 'CGO': 'COG', 'COD': 'COD',
    'GAB': 'GAB', 'CMR': 'CMR', 'CIV': 'CIV', 'GHA': 'GHA',
    'NIG': 'NER', 'BEN': 'BEN', 'TOG': 'TGO', 'BUR': 'BFA',
    'MLI': 'MLI', 'SEN': 'SEN', 'GAM': 'GMB', 'GUI': 'GIN',
    'SLE': 'SLE', 'LBR': 'LBR', 'MTN': 'MRT', 'MAD': 'MDG',
    'SEY': 'SYC', 'MRI': 'MUS', 'COM': 'COM', 'LES': 'LSO',
    'SWZ': 'SWZ', 'ERI': 'ERI', 'DJI': 'DJI', 'SOM': 'SOM',
    'CAF': 'CAF', 'CHA': 'TCD', 'GEQ': 'GNQ', 'STP': 'STP',
    'CPV': 'CPV', 'GBS': 'GNB', 'SOL': 'SLB', 'VAN': 'VUT',
    'SAM': 'WSM', 'FIJ': 'FJI', 'TGA': 'TON', 'PNG': 'PNG',
    'MGL': 'MNG', 'NEP': 'NPL', 'BHU': 'BTN', 'MDV': 'MDV',
    'OMA': 'OMN', 'QAT': 'QAT', 'KUW': 'KWT', 'BRN': 'BHR',
    'LIB': 'LBN', 'SYR': 'SYR', 'YEM': 'YEM', 'JOR': 'JOR',
    'PLE': 'PSE', 'AFG': 'AFG', 'TKM': 'TKM', 'UZB': 'UZB',
    'KGZ': 'KGZ', 'TJK': 'TJK', 'KAZ': 'KAZ',
    'PRK': 'PRK', 'KOR': 'KOR', 'JPN': 'JPN', 'CHN': 'CHN',
    'IND': 'IND', 'PAK': 'PAK', 'THA': 'THA',
    'LIE': 'LIE', 'MON': 'MCO', 'SMR': 'SMR', 'AND': 'AND',
    'MLT': 'MLT', 'CYP': 'CYP', 'ISL': 'ISL',
    'LUX': 'LUX', 'BLR': 'BLR', 'MDA': 'MDA',
    'MKD': 'MKD', 'MNE': 'MNE', 'SRB': 'SRB', 'BIH': 'BIH',
    'SLO': 'SVN', 'SVK': 'SVK', 'CZE': 'CZE',
    'LAT': 'LVA', 'LTU': 'LTU', 'EST': 'EST',
    'GEO': 'GEO', 'ARM': 'ARM', 'AZE': 'AZE',
    'UKR': 'UKR', 'RUS': 'RUS', 'USA': 'USA',
    'CAN': 'CAN', 'MEX': 'MEX', 'BRA': 'BRA',
    'ARG': 'ARG', 'COL': 'COL', 'VEN': 'VEN',
    'PER': 'PER', 'ECU': 'ECU', 'CUB': 'CUB',
    'DOM': 'DOM', 'JAM': 'JAM', 'IRL': 'IRL',
    'IRQ': 'IRQ', 'ISR': 'ISR', 'TUR': 'TUR',
    'POL': 'POL', 'ROU': 'ROU', 'HUN': 'HUN',
    'AUT': 'AUT', 'SWE': 'SWE', 'NOR': 'NOR',
    'FIN': 'FIN', 'ESP': 'ESP', 'ITA': 'ITA',
    'FRA': 'FRA', 'BEL': 'BEL', 'AUS': 'AUS',
    'NZL': 'NZL', 'EGY': 'EGY',
    # Historic / combined teams — map to modern successor
    'URS': 'RUS', 'EUN': 'RUS', 'FRG': 'DEU', 'GDR': 'DEU',
    'TCH': 'CZE', 'YUG': 'SRB', 'SCG': 'SRB',
    'RHO': 'ZWE', 'BOH': 'CZE', 'SAA': 'DEU',
    'ANZ': 'AUS', 'NFL': 'CAN', 'NBO': 'MYS',
    'WIF': 'TTO', 'UAR': 'SYR', 'YAR': 'YEM', 'YMD': 'YEM',
    'CRT': 'GRC', 'HKG': 'HKG', 'MAC': 'MAC',
    'VNM': 'VNM', 'SSD': 'SSD', 'KOS': 'XKX',
    'BIZ': 'BLZ', 'ARU': 'ABW', 'AHO': 'CUW',
}


def _noc_to_iso3(noc: str) -> str:
    """Convert an Olympic NOC code to ISO-3166 alpha-3."""
    return _NOC_TO_ISO3.get(noc, noc)


# ═════════════════════════════════════════════════════════════════════════════════
# EXISTING FUNCTIONS (preserved from previous iteration)
# ═════════════════════════════════════════════════════════════════════════════════


def fetch_medal_tally(df: pd.DataFrame, year: str, country: str) -> pd.DataFrame:
    """Fetch medal tally filtered by year and/or country.

    Args:
        df: Preprocessed Olympics DataFrame.
        year: Selected year or 'Overall' for all years.
        country: Selected country/region or 'Overall' for all countries.

    Returns:
        DataFrame with Gold, Silver, Bronze, and total columns.
    """
    medal_df = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )

    flag = 0

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[
            (medal_df['Year'] == int(year)) & (medal_df['region'] == country)
        ]

    if flag == 1:
        x = (
            temp_df.groupby('Year')
            .sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']]
            .sort_values('Gold')
            .reset_index()
        )
    else:
        x = (
            temp_df.groupby('region')
            .sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']]
            .sort_values('Gold', ascending=False)
            .reset_index()
        )

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype(int)
    x['Silver'] = x['Silver'].astype(int)
    x['Bronze'] = x['Bronze'].astype(int)
    x['total'] = x['total'].astype(int)

    return x


def country_year_list(df: pd.DataFrame) -> tuple[list, list]:
    """Get sorted lists of unique countries and years for dropdown selectors.

    Args:
        df: Preprocessed Olympics DataFrame.

    Returns:
        Tuple of (country_list, year_list), each with 'Overall' prepended.
    """
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return country, years


# Mapping from raw column names to human-readable labels
_COLUMN_LABELS = {
    'region': 'Nations',
    'Event': 'Events',
    'Name': 'Athletes',
}


def data_over_time(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Count unique values of a column per Olympic edition over time.

    Args:
        df: Preprocessed Olympics DataFrame.
        col: Column name to count unique values of (e.g. 'region', 'Event', 'Name').

    Returns:
        DataFrame with 'Edition' and a human-readable count column.
    """
    data = (
        df.drop_duplicates(['Year', col])['Year']
        .value_counts()
        .reset_index()
        .sort_values('Year')
    )

    label = _COLUMN_LABELS.get(col, col)
    data.rename(
        columns={'Year': 'Edition', 'count': f'Number of {label}'},
        inplace=True,
    )

    return data


def most_successful(
    df: pd.DataFrame, sport: str, country: str | None = None, top_n: int = 15
) -> pd.DataFrame:
    """Find the most successful athletes by medal count.

    Args:
        df: Preprocessed Olympics DataFrame.
        sport: Sport to filter by, or 'Overall' for all sports.
        country: Optional country/region to filter by.
        top_n: Number of top athletes to return.

    Returns:
        DataFrame with Name, Medals, Sport, and region columns.
    """
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    if country is not None:
        temp_df = temp_df[temp_df['region'] == country]

    x = (
        temp_df['Name']
        .value_counts()
        .reset_index()
        .head(top_n)
        .merge(df, left_on='Name', right_on='Name', how='left')[
            ['Name', 'count', 'Sport', 'region']
        ]
        .drop_duplicates('Name')
    )

    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x


def yearwise_medal_tally(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """Get year-by-year medal count for a specific country.

    Args:
        df: Preprocessed Olympics DataFrame.
        country: Country/region to analyse.

    Returns:
        DataFrame with Year and Medal count columns.
    """
    temp_df = df.dropna(subset=['Medal']).copy()
    temp_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],
        inplace=True,
    )

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_event_heatmap(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """Build a pivot table of medal counts by sport and year for a country.

    Args:
        df: Preprocessed Olympics DataFrame.
        country: Country/region to analyse.

    Returns:
        Pivot table DataFrame (Sport × Year) with medal counts.
    """
    temp_df = df.dropna(subset=['Medal']).copy()
    temp_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],
        inplace=True,
    )

    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(
        index='Sport', columns='Year', values='Medal', aggfunc='count'
    ).fillna(0)

    return pt


# ═════════════════════════════════════════════════════════════════════════════════
# NEW FUNCTIONS — Feature Expansion
# ═════════════════════════════════════════════════════════════════════════════════


def get_choropleth_data(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate medal counts per country for the world choropleth map.

    Deduplicates team events, maps NOC → ISO-3 codes, and returns
    Gold, Silver, Bronze, Total per country.

    Args:
        df: Preprocessed Olympics DataFrame (already season-filtered).

    Returns:
        DataFrame with columns: NOC, ISO3, region, Gold, Silver, Bronze, Total.
    """
    medal_df = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )

    agg = (
        medal_df.groupby(['NOC', 'region'])
        .sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']]
        .reset_index()
    )

    agg['Total'] = agg['Gold'] + agg['Silver'] + agg['Bronze']
    for col in ['Gold', 'Silver', 'Bronze', 'Total']:
        agg[col] = agg[col].astype(int)

    # Map NOC → ISO-3 for Plotly choropleth
    agg['ISO3'] = agg['NOC'].apply(_noc_to_iso3)

    # Some historic NOCs map to the same modern country — aggregate them
    agg = (
        agg.groupby(['ISO3', 'region'])
        .sum(numeric_only=True)[['Gold', 'Silver', 'Bronze', 'Total']]
        .reset_index()
    )

    return agg.sort_values('Total', ascending=False)


def compare_countries(
    df: pd.DataFrame, country1: str, country2: str
) -> dict[str, dict]:
    """Build comparison metrics for two countries.

    Args:
        df: Preprocessed Olympics DataFrame.
        country1: First country/region name.
        country2: Second country/region name.

    Returns:
        Dict with keys country1, country2, each containing:
        total_medals, gold, silver, bronze, total_athletes, total_sports, editions.
    """
    medal_df = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )

    result = {}
    for country in [country1, country2]:
        cdf = df[df['region'] == country]
        mdf = medal_df[(medal_df['region'] == country) & medal_df['Medal'].notna()]

        result[country] = {
            'Gold': int(mdf['Gold'].sum()),
            'Silver': int(mdf['Silver'].sum()),
            'Bronze': int(mdf['Bronze'].sum()),
            'Total Medals': int(mdf['Gold'].sum() + mdf['Silver'].sum() + mdf['Bronze'].sum()),
            'Athletes': cdf['Name'].nunique(),
            'Sports': cdf['Sport'].nunique(),
            'Editions': cdf['Year'].nunique(),
        }

    return result


def get_sport_overlap(
    df: pd.DataFrame, country1: str, country2: str
) -> tuple[set, set, set]:
    """Find shared and exclusive medal-winning sports between two countries.

    Args:
        df: Preprocessed Olympics DataFrame.
        country1: First country/region name.
        country2: Second country/region name.

    Returns:
        Tuple of (shared_sports, exclusive_to_c1, exclusive_to_c2).
    """
    medal_df = df.dropna(subset=['Medal'])

    sports1 = set(medal_df[medal_df['region'] == country1]['Sport'].unique())
    sports2 = set(medal_df[medal_df['region'] == country2]['Sport'].unique())

    shared = sports1 & sports2
    only_c1 = sports1 - sports2
    only_c2 = sports2 - sports1

    return shared, only_c1, only_c2


def get_season_comparison(df_all: pd.DataFrame) -> dict[str, dict]:
    """Compute side-by-side statistics for Summer vs Winter Olympics.

    Args:
        df_all: Full preprocessed DataFrame with BOTH seasons.

    Returns:
        Dict with keys 'Summer' and 'Winter', each containing:
        editions, cities, sports, events, athletes, nations.
    """
    result = {}
    for season in ['Summer', 'Winter']:
        sdf = df_all[df_all['Season'] == season]
        result[season] = {
            'Editions': sdf['Year'].nunique(),
            'Host Cities': sdf['City'].nunique(),
            'Sports': sdf['Sport'].nunique(),
            'Events': sdf['Event'].nunique(),
            'Athletes': sdf['Name'].nunique(),
            'Nations': sdf['region'].nunique(),
        }

    return result


def get_crossover_athletes(df_all: pd.DataFrame) -> pd.DataFrame:
    """Find athletes who competed in both Summer and Winter Olympics.

    Args:
        df_all: Full preprocessed DataFrame with BOTH seasons.

    Returns:
        DataFrame with Name, Sex, region, Summer_Sports, Winter_Sports,
        Summer_Years, Winter_Years, and Medals.
    """
    athlete_seasons = df_all.groupby('Name')['Season'].apply(set).reset_index()
    crossover_names = athlete_seasons[
        athlete_seasons['Season'].apply(lambda s: len(s) == 2)
    ]['Name']

    if crossover_names.empty:
        return pd.DataFrame(columns=[
            'Name', 'Sex', 'region', 'Summer Sports', 'Winter Sports',
            'Summer Years', 'Winter Years', 'Medals'
        ])

    cross_df = df_all[df_all['Name'].isin(crossover_names)]

    records = []
    for name, group in cross_df.groupby('Name'):
        summer = group[group['Season'] == 'Summer']
        winter = group[group['Season'] == 'Winter']
        medals = group['Medal'].notna().sum()

        records.append({
            'Name': name,
            'Sex': group['Sex'].iloc[0],
            'region': group['region'].iloc[0],
            'Summer Sports': ', '.join(sorted(summer['Sport'].unique())),
            'Winter Sports': ', '.join(sorted(winter['Sport'].unique())),
            'Summer Years': ', '.join(map(str, sorted(summer['Year'].unique()))),
            'Winter Years': ', '.join(map(str, sorted(winter['Year'].unique()))),
            'Medals': int(medals),
        })

    return (
        pd.DataFrame(records)
        .sort_values('Medals', ascending=False)
        .reset_index(drop=True)
    )


def get_season_medal_dominance(df_all: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """Get top countries and their medal counts split by season.

    Args:
        df_all: Full preprocessed DataFrame with BOTH seasons.
        top_n: Number of top countries to include.

    Returns:
        DataFrame with region, Summer_Medals, Winter_Medals columns.
    """
    medal_df = df_all.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )
    medal_df = medal_df.dropna(subset=['Medal'])

    # Total medals per country per season
    season_medals = (
        medal_df.groupby(['region', 'Season'])
        .size()
        .reset_index(name='Medals')
    )

    pivot = season_medals.pivot_table(
        index='region', columns='Season', values='Medals', fill_value=0
    ).reset_index()

    # Ensure both columns exist
    for col in ['Summer', 'Winter']:
        if col not in pivot.columns:
            pivot[col] = 0

    pivot['Total'] = pivot['Summer'] + pivot['Winter']
    pivot = pivot.sort_values('Total', ascending=False).head(top_n)

    return pivot


def compute_bmi_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Compute BMI statistics grouped by sport.

    BMI = Weight (kg) / Height (m)^2

    Args:
        df: Preprocessed Olympics DataFrame.

    Returns:
        DataFrame with Sport, avg_bmi, min_bmi, max_bmi, count columns.
    """
    bmi_df = df.dropna(subset=['Height', 'Weight']).copy()
    bmi_df['BMI'] = bmi_df['Weight'] / ((bmi_df['Height'] / 100) ** 2)

    stats = (
        bmi_df.groupby('Sport')['BMI']
        .agg(['mean', 'min', 'max', 'count'])
        .reset_index()
    )
    stats.columns = ['Sport', 'Avg BMI', 'Min BMI', 'Max BMI', 'Athletes']
    stats = stats[stats['Athletes'] >= 10]  # Only sports with enough data
    stats = stats.sort_values('Avg BMI', ascending=False).reset_index(drop=True)

    for col in ['Avg BMI', 'Min BMI', 'Max BMI']:
        stats[col] = stats[col].round(1)

    return stats


def get_bmi_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Get individual BMI values for distribution plotting.

    Args:
        df: Preprocessed Olympics DataFrame.

    Returns:
        DataFrame with Name, Sport, BMI, Medal columns.
    """
    bmi_df = df.dropna(subset=['Height', 'Weight']).copy()
    bmi_df['BMI'] = (bmi_df['Weight'] / ((bmi_df['Height'] / 100) ** 2)).round(1)
    return bmi_df[['Name', 'Sport', 'BMI', 'Medal', 'Sex']].drop_duplicates()


def get_repeat_medalists(df: pd.DataFrame, min_editions: int = 3) -> pd.DataFrame:
    """Find athletes who won medals across multiple Olympic editions.

    Args:
        df: Preprocessed Olympics DataFrame.
        min_editions: Minimum number of different editions with medals.

    Returns:
        DataFrame with Name, region, Sport, Medals, Editions, Years.
    """
    medal_df = df.dropna(subset=['Medal'])

    athlete_editions = (
        medal_df.groupby('Name')
        .agg(
            Editions=('Year', 'nunique'),
            Medals=('Medal', 'count'),
            Years=('Year', lambda x: ', '.join(map(str, sorted(x.unique())))),
            region=('region', 'first'),
            Sport=('Sport', lambda x: ', '.join(sorted(x.unique())[:3])),
        )
        .reset_index()
    )

    result = (
        athlete_editions[athlete_editions['Editions'] >= min_editions]
        .sort_values(['Editions', 'Medals'], ascending=[False, False])
        .head(50)
        .reset_index(drop=True)
    )

    return result


def search_athlete(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Search for athletes by name (case-insensitive substring match).

    Args:
        df: Preprocessed Olympics DataFrame.
        query: Search string.

    Returns:
        DataFrame with the athlete's Olympic history: Year, City, Sport,
        Event, Medal, Age for each appearance.
    """
    if not query or len(query.strip()) < 2:
        return pd.DataFrame()

    query_lower = query.strip().lower()
    matches = df[df['Name'].str.lower().str.contains(query_lower, na=False)]

    if matches.empty:
        return pd.DataFrame()

    result = (
        matches[['Name', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal', 'Age', 'region']]
        .drop_duplicates()
        .sort_values(['Name', 'Year'])
        .reset_index(drop=True)
    )

    return result