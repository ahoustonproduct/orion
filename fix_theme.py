import re

with open("frontend/app/learn/[lessonId]/page.tsx", "r") as f:
    content = f.read()

replacements = {
    # Backgrounds
    r'bg-white\b': 'glass-card border-white/5',
    r'bg-\[\#ffffff\]': 'glass-card border-white/5',
    r'bg-\[\#f5f0ea\]': 'bg-black/20',
    r'bg-\[\#1e1a16\]': 'bg-black/40',
    
    # Text colors
    r'text-\[\#1c1410\]': 'text-white',
    r'text-\[\#5c4f45\]': 'text-gray-300',
    r'text-\[\#9a8c80\]': 'text-gray-400',
    r'text-\[\#f0ece6\]': 'text-gray-200',
    
    # Border colors
    r'border-\[\#e5ddd4\]': 'border-white/10 border-transparent',
    r'border-\[\#2c2520\]': 'border-white/5',
    
    # Accents (WUSTL red to premium rose/accent)
    r'bg-\[\#a01c2c\]': 'bg-[var(--color-accent)] shadow-lg shadow-[var(--color-accent)]/20',
    r'hover:bg-\[\#821624\]': 'hover:bg-[var(--color-accent-hover)]',
    r'text-\[\#a01c2c\]': 'text-[var(--color-accent-light)]',
    r'hover:border-\[\#a01c2c\]': 'hover:border-[var(--color-accent)] hover:shadow-[var(--color-accent)]/20 shadow-md',
    
    # Success/Error states in dark mode
    r'bg-green-50': 'bg-green-500/10',
    r'border-green-200': 'border-green-500/30',
    r'text-green-700': 'text-green-400',
    r'text-green-600': 'text-green-500',
    r'bg-red-50': 'bg-red-500/10',
    r'border-red-200': 'border-red-500/30',
    r'text-red-700': 'text-red-400',
    r'text-red-600': 'text-red-500',
    
    # Specific elements
    r'text-black': 'text-white',
    r'border overflow-x-auto': 'border-white/10 overflow-x-auto',
}

for pattern, replacement in replacements.items():
    content = re.sub(pattern, replacement, content)

# Fix the inner raw html Markdown renderer since it uses hardcoded #1c1410 and #1e1a16 too
content = content.replace("bg-[#1e1a16]", "bg-black/30")
content = content.replace("border-[#2c2520]", "border-white/10")
content = content.replace("text-[#1c1410]", "text-white")

with open("frontend/app/learn/[lessonId]/page.tsx", "w") as f:
    f.write(content)
