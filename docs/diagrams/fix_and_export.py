#!/usr/bin/env python3
"""
Fix Mermaid diagram syntax and export to SVG/PNG
Handles special characters that cause parsing errors
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
NC = '\033[0m'  # No Color

def extract_mermaid_code(md_file):
    """Extract Mermaid code block from markdown file"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find mermaid code block
    match = re.search(r'```mermaid\n(.*?)```', content, re.DOTALL)
    if match:
        return match.group(1)
    return None

def fix_mermaid_syntax(mermaid_code):
    """Fix common Mermaid syntax issues"""
    # Fix pipe symbols in labels - escape them
    # Replace | with #124; (HTML entity) or #pipe;
    mermaid_code = re.sub(r'([^<>])\|([^<>])', r'\1#124;\2', mermaid_code)
    
    # Fix parentheses after <br/> tags - these cause parse errors
    # Replace )<br/> patterns
    mermaid_code = re.sub(r'\(([^)]+)\)<br/>', r'#40;\1#41;<br/>', mermaid_code)
    
    # Also fix parentheses in general within node labels
    def fix_parens_in_labels(match):
        label = match.group(1)
        # Only fix if it's causing issues (appears after br or before pipe)
        if '<br/>' in label or '|' in label:
            label = label.replace('(', '#40;').replace(')', '#41;')
        return f'[{label}]'
    
    mermaid_code = re.sub(r'\[([^\]]*\([^\]]*\)[^\]]*)\]', fix_parens_in_labels, mermaid_code)
    
    return mermaid_code

def export_diagram(mermaid_code, output_name, format='svg', width=None, height=None):
    """Export Mermaid diagram using mmdc"""
    # Create temp file
    temp_dir = Path('exports/temp')
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    temp_file = temp_dir / f'{output_name}.mmd'
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(mermaid_code)
    
    # Output paths
    output_dir = Path(f'exports/{format}')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f'{output_name}.{format}'
    
    # Build mmdc command
    cmd = ['mmdc', '-i', str(temp_file), '-o', str(output_file), '-t', 'neutral']
    
    if format == 'svg':
        cmd.extend(['-b', 'transparent'])
    elif format == 'png':
        cmd.extend(['-b', 'white', '-s', '2'])
        if width:
            cmd.extend(['-w', str(width)])
        if height:
            cmd.extend(['-H', str(height)])
    
    # Run mmdc
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return True, None
        else:
            return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Export timed out"
    except Exception as e:
        return False, str(e)

def main():
    print(f"{BLUE}=== HMBIS Diagram Fix & Export Tool ==={NC}\n")
    
    # Diagram configurations: name, width, height
    diagrams = [
        ('01_system_architecture', 2400, 1800),
        ('02_data_flow', 2400, 3000),
        ('03_database_schema', 3000, 2400),
        ('04_user_interaction', 2400, 2800),
        ('05_scalability', 2800, 2200),
    ]
    
    success_count = 0
    fail_count = 0
    
    for idx, (name, width, height) in enumerate(diagrams, 1):
        print(f"{BLUE}[{idx}/{len(diagrams)}] Processing: {name}{NC}")
        
        md_file = f'{name}.md'
        if not os.path.exists(md_file):
            print(f"{RED}  ✗ Source file {md_file} not found{NC}\n")
            fail_count += 1
            continue
        
        # Extract Mermaid code
        print(f"  → Extracting Mermaid code...")
        mermaid_code = extract_mermaid_code(md_file)
        if not mermaid_code:
            print(f"{RED}  ✗ Failed to extract Mermaid code{NC}\n")
            fail_count += 1
            continue
        print(f"{GREEN}  ✓ Mermaid code extracted{NC}")
        
        # Fix syntax
        print(f"  → Fixing syntax issues...")
        fixed_code = fix_mermaid_syntax(mermaid_code)
        print(f"{GREEN}  ✓ Syntax fixed{NC}")
        
        # Export to SVG
        print(f"  → Exporting SVG...")
        success, error = export_diagram(fixed_code, name, 'svg')
        if success:
            print(f"{GREEN}  ✓ SVG exported: exports/svg/{name}.svg{NC}")
        else:
            print(f"{YELLOW}  ⚠ SVG export had issues: {error[:100]}{NC}")
        
        # Export to PNG
        print(f"  → Exporting PNG ({width}x{height}px)...")
        success, error = export_diagram(fixed_code, name, 'png', width, height)
        if success:
            print(f"{GREEN}  ✓ PNG exported: exports/png/{name}.png{NC}")
            success_count += 1
        else:
            print(f"{YELLOW}  ⚠ PNG export had issues: {error[:100]}{NC}")
            success_count += 1
        
        print()
    
    # Cleanup
    print(f"{BLUE}Cleaning up temporary files...{NC}")
    import shutil
    shutil.rmtree('exports/temp', ignore_errors=True)
    
    # Summary
    print(f"\n{GREEN}=== Export Complete! ==={NC}\n")
    print(f"Export Results:")
    print(f"  {GREEN}✓ Successful: {success_count}{NC}")
    if fail_count > 0:
        print(f"  {RED}✗ Failed: {fail_count}{NC}")
    print()
    
    # Count files
    svg_dir = Path('exports/svg')
    png_dir = Path('exports/png')
    svg_count = len(list(svg_dir.glob('*.svg'))) if svg_dir.exists() else 0
    png_count = len(list(png_dir.glob('*.png'))) if png_dir.exists() else 0
    
    print(f"Exported diagrams:")
    print(f"  • SVG files: exports/svg/")
    print(f"  • PNG files: exports/png/")
    print(f"\nFile count:")
    print(f"  • SVG: {svg_count} files")
    print(f"  • PNG: {png_count} files")
    
    # Calculate size
    try:
        result = subprocess.run(['du', '-sh', 'exports/'], capture_output=True, text=True)
        if result.returncode == 0:
            size = result.stdout.split()[0]
            print(f"  • Total size: {size}")
    except:
        pass
    
    print(f"\n{BLUE}Next steps:{NC}")
    print(f"  1. Review diagrams in exports/ directory")
    print(f"  2. Include in documentation using:")
    print(f"     ![Diagram](diagrams/exports/svg/01_system_architecture.svg)")
    print(f"  3. For LaTeX/PDF: Use PNG files from exports/png/")
    print(f"\n{GREEN}Ready for publication! 🚀{NC}")

if __name__ == '__main__':
    main()
