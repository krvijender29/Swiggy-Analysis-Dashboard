from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Swiggy_Raw_Data_Excel.xlsx"

PAGE_TITLE = "Swiggy Analytics Dashboard"
PAGE_ICON = "🧡"
LAYOUT = "wide"

COLOR_SEQ = ["#FF6B35", "#FF9142", "#FFC371", "#4ecdc4", "#556fb5", "#a685e2", "#f7b267"]
PLOTLY_TEMPLATE = "plotly_dark"

PRICE_BINS = [0,100,200,300,500,1000, float("inf")]
PRICE_LABELS = ["<100","100-200","200-300","300-500","500-1000","1000+"]

WEEKDAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]