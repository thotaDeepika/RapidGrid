import sys

# 1. Update index.css to add custom dark scrollbar
css_file = "src/index.css"
with open(css_file, "r", encoding="utf-8") as f:
    css_content = f.read()

new_scrollbar_css = """::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: #0b1326;
}
::-webkit-scrollbar-thumb {
  background: #2d3449;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #ffb3ad;
}"""

css_content = css_content.replace("::-webkit-scrollbar { display: none; }", new_scrollbar_css)

with open(css_file, "w", encoding="utf-8") as f:
    f.write(css_content)


# 2. Update CitizenDashboard.jsx layout height & padding for smooth scrolling
cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    c_content = f.read()

# Adjust map height from 45vh to 32vh
c_content = c_content.replace(
    '<div className="relative w-full h-[45vh] overflow-hidden bg-surface-container-low flex-shrink-0">',
    '<div className="relative w-full h-[32vh] overflow-hidden bg-surface-container-low flex-shrink-0">'
)

# Add pb-16 to tracking view main container for smooth bottom scrolling
c_content = c_content.replace(
    '<main className="flex-1 flex flex-col w-full pt-16 bg-surface overflow-y-auto">',
    '<main className="flex-1 flex flex-col w-full pt-16 pb-16 bg-surface overflow-y-auto space-y-4">'
)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(c_content)

print("index.css scrollbar restored and CitizenDashboard layout scrolling optimized")
