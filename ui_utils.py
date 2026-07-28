"""Utility functions for rich UI rendering: flags, emojis, and styling."""

import base64

# Mapping from ISO-3 to ISO-2 for flagcdn
ISO3_TO_ISO2 = {
    'DEU': 'de', 'CHE': 'ch', 'GRC': 'gr', 'NLD': 'nl', 'DNK': 'dk',
    'HRV': 'hr', 'PRT': 'pt', 'BGR': 'bg', 'GBR': 'gb', 'ZAF': 'za',
    'CHL': 'cl', 'IRN': 'ir', 'MYS': 'my', 'PHL': 'ph', 'NGA': 'ng',
    'TWN': 'tw', 'SAU': 'sa', 'ARE': 'ae', 'BHS': 'bs', 'PRI': 'pr',
    'TTO': 'tt', 'VIR': 'vi', 'VGB': 'vg', 'BMU': 'bm', 'CYM': 'ky',
    'ATG': 'ag', 'VCT': 'vc', 'BRB': 'bb', 'KNA': 'kn', 'LCA': 'lc',
    'GRD': 'gd', 'DMA': 'dm', 'HTI': 'ht', 'GTM': 'gt', 'HND': 'hn',
    'SLV': 'sv', 'NIC': 'ni', 'CRI': 'cr', 'PAN': 'pa', 'PRY': 'py',
    'URY': 'uy', 'BOL': 'bo', 'LKA': 'lk', 'BGD': 'bd', 'MMR': 'mm',
    'KHM': 'kh', 'LAO': 'la', 'VNM': 'vn', 'IDN': 'id', 'SGP': 'sg',
    'BRN': 'bn', 'TLS': 'tl', 'DZA': 'dz', 'MAR': 'ma', 'TUN': 'tn',
    'LBY': 'ly', 'SDN': 'sd', 'ETH': 'et', 'KEN': 'ke', 'TZA': 'tz',
    'UGA': 'ug', 'RWA': 'rw', 'BDI': 'bi', 'MOZ': 'mz', 'MWI': 'mw',
    'ZMB': 'zm', 'ZWE': 'zw', 'BWA': 'bw', 'NAM': 'na', 'AGO': 'ao',
    'COG': 'cg', 'COD': 'cd', 'GAB': 'ga', 'CMR': 'cm', 'CIV': 'ci',
    'GHA': 'gh', 'NER': 'ne', 'BEN': 'bj', 'TGO': 'tg', 'BFA': 'bf',
    'MLI': 'ml', 'SEN': 'sn', 'GMB': 'gm', 'GIN': 'gn', 'SLE': 'sl',
    'LBR': 'lr', 'MRT': 'mr', 'MDG': 'mg', 'SYC': 'sc', 'MUS': 'mu',
    'COM': 'km', 'LSO': 'ls', 'SWZ': 'sz', 'ERI': 'er', 'DJI': 'dj',
    'SOM': 'so', 'CAF': 'cf', 'TCD': 'td', 'GNQ': 'gq', 'STP': 'st',
    'CPV': 'cv', 'GNB': 'gw', 'SLB': 'sb', 'VUT': 'vu', 'WSM': 'ws',
    'FJI': 'fj', 'TON': 'to', 'PNG': 'pg', 'MNG': 'mn', 'NPL': 'np',
    'BTN': 'bt', 'MDV': 'mv', 'OMN': 'om', 'QAT': 'qa', 'KWT': 'kw',
    'BHR': 'bh', 'LBN': 'lb', 'SYR': 'sy', 'YEM': 'ye', 'JOR': 'jo',
    'PSE': 'ps', 'AFG': 'af', 'TKM': 'tm', 'UZB': 'uz', 'KGZ': 'kg',
    'TJK': 'tj', 'KAZ': 'kz', 'PRK': 'kp', 'KOR': 'kr', 'JPN': 'jp',
    'CHN': 'cn', 'IND': 'in', 'PAK': 'pk', 'THA': 'th', 'LIE': 'li',
    'MCO': 'mc', 'SMR': 'sm', 'AND': 'ad', 'MLT': 'mt', 'CYP': 'cy',
    'ISL': 'is', 'LUX': 'lu', 'BLR': 'by', 'MDA': 'md', 'MKD': 'mk',
    'MNE': 'me', 'SRB': 'rs', 'BIH': 'ba', 'SVN': 'si', 'SVK': 'sk',
    'CZE': 'cz', 'LVA': 'lv', 'LTU': 'lt', 'EST': 'ee', 'GEO': 'ge',
    'ARM': 'am', 'AZE': 'az', 'UKR': 'ua', 'RUS': 'ru', 'USA': 'us',
    'CAN': 'ca', 'MEX': 'mx', 'BRA': 'br', 'ARG': 'ar', 'COL': 'co',
    'VEN': 've', 'PER': 'pe', 'ECU': 'ec', 'CUB': 'cu', 'DOM': 'do',
    'JAM': 'jm', 'IRL': 'ie', 'IRQ': 'iq', 'ISR': 'il', 'TUR': 'tr',
    'POL': 'pl', 'ROU': 'ro', 'HUN': 'hu', 'AUT': 'at', 'SWE': 'se',
    'NOR': 'no', 'FIN': 'fi', 'ESP': 'es', 'ITA': 'it', 'FRA': 'fr',
    'BEL': 'be', 'AUS': 'au', 'NZL': 'nz', 'EGY': 'eg', 'MAC': 'mo',
    'SSD': 'ss', 'XKX': 'xk', 'BLZ': 'bz', 'ABW': 'aw', 'CUW': 'cw',
    'FR': 'fr', 'IT': 'it'
}

SPORT_EMOJIS = {
    'Swimming': '🏊', 'Athletics': '🏃', 'Gymnastics': '🤸', 'Cycling': '🚴',
    'Football': '⚽', 'Basketball': '🏀', 'Tennis': '🎾', 'Volleyball': '🏐',
    'Boxing': '🥊', 'Weightlifting': '🏋️', 'Wrestling': '🤼', 'Judo': '🥋',
    'Taekwondo': '🥋', 'Table Tennis': '🏓', 'Badminton': '🏸', 'Golf': '⛳',
    'Hockey': '🏑', 'Ice Hockey': '🏒', 'Figure Skating': '⛸️', 'Skiing': '⛷️',
    'Snowboarding': '🏂', 'Rowing': '🚣', 'Sailing': '⛵', 'Equestrianism': '🐎',
    'Shooting': '🎯', 'Archery': '🏹', 'Fencing': '🤺', 'Water Polo': '🤽',
    'Diving': '🏊‍♂️', 'Synchronized Swimming': '🧜‍♀️', 'Speed Skating': '⛸️',
    'Short Track Speed Skating': '⛸️', 'Cross Country Skiing': '🎿',
    'Alpine Skiing': '⛷️', 'Freestyle Skiing': '⛷️', 'Ski Jumping': '🎿',
    'Nordic Combined': '🎿', 'Biathlon': '🎿', 'Bobsleigh': '🛷', 'Skeleton': '🛷',
    'Luge': '🛷', 'Curling': '🥌', 'Rugby': '🏉', 'Rugby Sevens': '🏉',
    'Baseball': '⚾', 'Softball': '🥎', 'Canoeing': '🛶', 'Triathlon': '🏃‍♂️',
    'Modern Pentathlon': '🤺', 'Trampolining': '🤸', 'Rhythmic Gymnastics': '🎗️',
    'Beach Volleyball': '🏖️', 'Handball': '🤾', 'Wrestling': '🤼', 'Karate': '🥋',
    'Skateboarding': '🛹', 'Sport Climbing': '🧗', 'Surfing': '🏄', 'BMX': '🚴',
    'Overall': '🏅'
}

def get_flag_url(iso3: str) -> str:
    """Get the flagcdn URL for a given ISO-3 code."""
    iso2 = ISO3_TO_ISO2.get(iso3.upper())
    if iso2:
        return f"https://flagcdn.com/w40/{iso2}.png"
    return "https://upload.wikimedia.org/wikipedia/commons/2/2f/Missing_flag.png"

def get_sport_icon(sport_name: str) -> str:
    """Return an emoji icon for the given sport."""
    return SPORT_EMOJIS.get(sport_name, '🏅')

def get_image_base64(filepath: str) -> str:
    """Convert a local image to base64 for embedding in CSS."""
    with open(filepath, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_country_emoji(iso3: str) -> str:
    """Convert an ISO-3 code to a Flag Emoji."""
    iso2 = ISO3_TO_ISO2.get(iso3.upper())
    if not iso2:
        return '🏳️'
    return chr(ord(iso2[0].upper()) + 127397) + chr(ord(iso2[1].upper()) + 127397)
