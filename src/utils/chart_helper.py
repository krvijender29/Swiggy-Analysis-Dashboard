from src.config import PLOTLY_TEMPLATE

def style_fig(fig, height: int = 420):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color = "#d6d9e3"),
        height= height,
        margin=dict(l=10, r= 10, t= 50, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    return fig
