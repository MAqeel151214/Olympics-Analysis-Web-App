"""Shared chart styling utilities for consistent Plotly visualizations."""

import plotly.graph_objects as go

# ── Color palette ────────────────────────────────────────────────────────────────
ACCENT = '#FF6B35'
TEAL = '#4ECDC4'
YELLOW = '#FFD93D'
PURPLE = '#A78BFA'
PINK = '#F472B6'
GOLD = '#FFD700'
SILVER = '#C0C0C0'
BRONZE = '#CD7F32'

MEDAL_COLORS = {'Gold': GOLD, 'Silver': SILVER, 'Bronze': BRONZE}
SEASON_COLORS = {'Summer': '#FF6B35', 'Winter': '#60A5FA'}
GENDER_COLORS = {'M': TEAL, 'F': ACCENT}

# Accent sequence for multi-series charts
COLOR_SEQUENCE = [ACCENT, TEAL, YELLOW, PURPLE, PINK, '#34D399', '#F87171', '#818CF8']


def style_chart(fig: go.Figure, height: int | None = None) -> go.Figure:
    """Apply consistent dark theme styling to a Plotly figure.

    Args:
        fig: Plotly figure to style.
        height: Optional explicit height in pixels.

    Returns:
        The same figure with styling applied (mutated in place).
    """
    layout_kwargs = dict(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter'),
    )
    if height is not None:
        layout_kwargs['height'] = height

    fig.update_layout(**layout_kwargs)
    return fig


def styled_line(fig: go.Figure, color: str = ACCENT, width: float = 2.5) -> go.Figure:
    """Apply line styling + dark theme to a Plotly line chart.

    Args:
        fig: Plotly figure with line traces.
        color: Line color (hex).
        width: Line width.

    Returns:
        Styled figure.
    """
    fig.update_traces(line=dict(color=color, width=width))
    return style_chart(fig)


def styled_heatmap(fig: go.Figure, n_rows: int, row_height: int = 24) -> go.Figure:
    """Apply heatmap styling with dynamic height.

    Args:
        fig: Plotly imshow figure.
        n_rows: Number of rows in the heatmap (for height calculation).
        row_height: Pixels per row.

    Returns:
        Styled figure.
    """
    return style_chart(fig, height=max(450, n_rows * row_height))
