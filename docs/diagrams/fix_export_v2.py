#!/usr/bin/env python3
"""
Fix Mermaid diagram syntax for successful export
Strategy: Replace problematic characters with safe alternatives
"""

import re
import os
import subprocess
from pathlib import Path

# ANSI color codes
GREEN = '\033[0;32m'
BLUE = '\033[0;34m'
RED = '\033[0;31m'
YELLOW = '\033[0;33m'
NC = '\033[0m'

def extract_mermaid_code(md_file):
    """Extract Mermaid code block from markdown file"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'```mermaid\n(.*?)```', content, re.DOTALL)
    if match:
        return match.group(1)
    return None

def fix_mermaid_syntax(mermaid_code):
    """Fix Mermaid syntax issues by replacing problematic characters"""
    
    # Replace pipe symbols with unicode alternatives or remove
    mermaid_code = mermaid_code.replace(' | ', ' / ')
    mermaid_code = mermaid_code.replace('|', '/')
    
    # Fix curly braces in paths that might confuse parser
    # Replace {z}/{x}/{y} type patterns
    mermaid_code = re.sub(r'\{([a-z])\}', r'[\1]', mermaid_code)
    
    # Replace special unicode characters that might cause issues
    mermaid_code = mermaid_code.replace('━', '-')
    mermaid_code = mermaid_code.replace('•', '*')
    
    # Fix parentheses in labels - escape them or replace
    # Strategy: Replace (text) with [text] in node labels
    def fix_node_label(match):
        full_match = match.group(0)
        node_id = match.group(1)
        label_content = match.group(2)
        
        # Replace parentheses with square brackets in labels
        label_content = label_content.replace('(', '[').replace(')', ']')
        
        return f'{node_id}[{label_content}]'
    
    # Match patterns like: NODEID[label content with (parens)]
    mermaid_code = re.sub(r'(\w+)\[([^\]]*\([^\]]*\)[^\]]*)\]', fix_node_label, mermaid_code)
    
    return mermaid_code

def export_diagram(mermaid_code, output_name, format='svg', width=None, height=None):
    """Export Mermaid diagram using mmdc"""
    temp_dir = Path('exports/temp')
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    temp_file = temp_dir / f'{output_name}.mmd'
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(mermaid_code)
    
    output_dir = Path(f'exports/{format}')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f'{output_name}.{format}'
    
    cmd = ['mmdc', '-i', str(temp_file), '-o', str(output_file), '-t', 'neutral']
    
    if format == 'svg':
        cmd.extend(['-b', 'transparent'])
    elif format == 'png':
        cmd.extend(['-b', 'white', '-s', '2'])
        if width:
            cmd.extend(['-w', str(width)])
        if height:
            cmd.extend(['-H', str(height)])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return True, "Success"
        else:
            # Extract first line of error
            error_line = result.stderr.split('\n')[0] if result.stderr else "Unknown error"
            return False, error_line[:150]
    except subprocess.TimeoutExpired:
        return False, "Export timed out (30s)"
    except Exception as e:
        return False, str(e)[:150]

def main():
    print(f"{BLUE}=== HMBIS Diagram Fix & Export Tool (v2) ==={NC}\n")
    
    diagrams = [
        ('01_system_architecture', 2400, 1800),
        ('02_data_flow', 2400, 3000),
        ('03_database_schema', 3000, 2400),
        ('04_user_interaction', 2400, 2800),
        ('05_scalability', 2800, 2200),
    ]
    
    success_count = 0
    fail_count = 0
    warnings = []
    
    for idx, (name, width, height) in enumerate(diagrams, 1):
        print(f"{BLUE}[{idx}/{len(diagrams)}] Processing: {name}{NC}")
        
        md_file = f'{name}.md'
        if not os.path.exists(md_file):
            print(f"{RED}  ✗ Source file not found{NC}\n")
            fail_count += 1
            continue
        
        # Extract
        print(f"  → Extracting Mermaid code...")
        mermaid_code = extract_mermaid_code(md_file)
        if not mermaid_code:
            print(f"{RED}  ✗ Extraction failed{NC}\n")
            fail_count += 1
            continue
        
        # Fix syntax
        print(f"  → Fixing syntax (replacing pipes, braces, special chars)...")
        fixed_code = fix_mermaid_syntax(mermaid_code)
        
        # Export SVG
        print(f"  → Exporting SVG...")
        success, msg = export_diagram(fixed_code, name, 'svg')
        if success:
            print(f"{GREEN}  ✓ SVG: exports/svg/{name}.svg{NC}")
        else:
            print(f"{RED}  ✗ SVG failed: {msg}{NC}")
            warnings.append(f"{name} SVG: {msg}")
        
        # Export PNG
        print(f"  → Exporting PNG ({width}x{height}px)...")
        success_png, msg_png = export_diagram(fixed_code, name, 'png', width, height)
        if success_png:
            print(f"{GREEN}  ✓ PNG: exports/png/{name}.png{NC}")
            if success:  # Both succeeded
                success_count += 1
        else:
            print(f"{RED}  ✗ PNG failed: {msg_png}{NC}")
            warnings.append(f"{name} PNG: {msg_png}")
        
        if not success and not success_png:
            fail_count += 1
        
        print()
    
    # Cleanup
    print(f"{BLUE}Cleaning up...{NC}")
    import shutil
    shutil.rmtree('exports/temp', ignore_errors=True)
    
    # Summary
    print(f"\n{GREEN}===Export Complete! ==={NC}\n")
    print(f"Results: {GREEN}{success_count} successful{NC}, {RED}{fail_count} failed{NC}")
    
    if warnings:
        print(f"\n{YELLOW}Warnings:{NC}")
        for w in warnings[:5]:  # Show first 5
            print(f"  • {w}")
    
    svg_dir = Path('exports/svg')
    png_dir = Path('exports/png')
    svg_files = list(svg_dir.glob('*.svg')) if svg_dir.exists() else []
    png_files = list(png_dir.glob('*.png')) if png_dir.exists() else []
    
    print(f"\nExported files:")
    print(f"  • SVG: {len(svg_files)} files in exports/svg/")
    print(f"  • PNG: {len(png_files)} files in exports/png/")
    
    if svg_files:
        print(f"\n{GREEN}Successfully exported:{NC}")
        for f in svg_files:
            print(f"  ✓ {f.name}")
    
    print(f"\n{BLUE}Usage:{NC}")
    print(f"  View SVG: open exports/svg/*.svg")
    print(f"  View PNG: open exports/png/*.png")
    print(f"\n{GREEN}🚀 Done!{NC}")

if __name__ == '__main__':
    main()
