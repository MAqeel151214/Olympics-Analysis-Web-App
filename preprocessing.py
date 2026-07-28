import pandas as pd


def preprocess(df: pd.DataFrame, region_df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess raw Olympics data for analysis.

    Steps:
        1. Merge with NOC region mapping to add country/region names.
        2. Remove duplicate rows.
        3. One-hot encode the Medal column into integer Gold, Silver, Bronze columns.

    Note:
        Both Summer and Winter Olympics are retained. Season filtering
        is handled at the UI layer via sidebar controls.

    Args:
        df: Raw athlete_events DataFrame.
        region_df: NOC-to-region mapping DataFrame.

    Returns:
        Cleaned and enriched DataFrame ready for analysis.
    """
    # Merge with region/NOC mapping
    df = df.merge(region_df, on='NOC', how='left')

    # Drop duplicates
    df = df.drop_duplicates()

    # One-hot encode medals as integers (not booleans)
    df = pd.concat([df, pd.get_dummies(df['Medal']).astype(int)], axis=1)

    return df
