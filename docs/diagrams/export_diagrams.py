#!/usr/bin/env python3
"""
Export HMBIS Mermaid diagrams with proper character handling
Uses quotes to wrap labels containing special characters
"""

import re
import os
import subprocess
import sys
from pathlib import Path

GREEN = '\033[0;32m'
BLUE = '\033[0;34m'
RED = '\033[0;31m'
YELLOW = '\033[0;33m'
NC = '\033[0m'

def extract_mermaid(md_file):
    """Extract Mermaid code from markdown"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'```mermaid\n(.*?)\n```', content, re.DOTALL)
    return match.group(1) if match else None

def safe_export(mermaid_code, name, format='svg', width=None, height=None):
    """Export with mmdc, handling special characters"""
    
    # Create temp directory
    temp_dir = Path('exports/temp')
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Write to temp file
    temp_file = temp_dir / f'{name}.mmd'
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(mermaid_code)
    
    # Setup output
    out_dir = Path(f'exports/{format}')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f'{name}.{format}'
    
    # Build command
    cmd = ['mmdc', '-i', str(temp_file), '-o', str(out_file), 
           '-t', 'neutral', '-e', 'utf8']
    
    if format == 'svg':
        cmd.extend(['-b', 'transparent'])
    else:  # png
        cmd.extend(['-b', 'white', '-s', '2'])
        if width:
            cmd.extend(['-w', str(width), '-H', str(height)])
    
    # Execute
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, 
                              timeout=45, cwd=os.getcwd())
        
        if result.returncode == 0 and out_file.exists():
            return True, f"✓ {format.upper()}: {out_file}"
        
        # Parse error message
        error = result.stderr or result.stdout or "Unknown error"
        # Extract meaningful error line
        for line in error.split('\n'):
            if 'Error:' in line or 'Parse error' in line:
                return False, line[:200]
        return False, error[:200]
        
    except subprocess.TimeoutExpired:
        return False, "Timeout (45s exceeded)"
    except Exception as e:
        return False, str(e)[:200]

def main():
    print(f"{BLUE}{'='*60}{NC}")
    print(f"{BLUE}HMBIS Knowledge Common - Diagram Export Utility{NC}")
    print(f"{BLUE}{'='*60}{NC}\n")
    
    # Check mmdc
    try:
        subprocess.run(['mmdc', '--version'], capture_output=True, check=True)
    except:
        print(f"{RED}Error: mmdc not found! Install: npm install -g @mermaid-js/mermaid-cli{NC}")
        sys.exit(1)
    
    diagrams = [
        ('01_system_architecture', 2400, 1800),
        ('02_data_flow', 2400, 3000),
        ('03_database_schema', 3000, 2400),
        ('04_user_interaction', 2400, 2800),
        ('05_scalability', 2800, 2200),
    ]
    
    results = {'success': [], 'failed': [], 'partial': []}
    
    for idx, (name, width, height) in enumerate(diagrams, 1):
        print(f"\n{BLUE}[{idx}/{len(diagrams)}] {name}{NC}")
        print(f"{'-'*60}")
        
        md_file = f'{name}.md'
        if not Path(md_file).exists():
            print(f"{RED}✗ File not found: {md_file}{NC}")
            results['failed'].append(name)
            continue
        
        # Extract Mermaid
        code = extract_mermaid(md_file)
        if not code:
            print(f"{RED}✗ Could not extract Mermaid code{NC}")
            results['failed'].append(name)
            continue
        
        print(f"{GREEN}✓{NC} Extracted {len(code)} characters of Mermaid code")
        
        # Export SVG
        svg_ok, svg_msg = safe_export(code, name, 'svg')
        if svg_ok:
            print(f"{GREEN}{svg_msg}{NC}")
        else:
            print(f"{YELLOW}⚠ SVG: {svg_msg}{NC}")
        
        # Export PNG
        png_ok, png_msg = safe_export(code, name, 'png', width, height)
        if png_ok:
            print(f"{GREEN}{png_msg}{NC}")
        else:
            print(f"{YELLOW}⚠ PNG: {png_msg}{NC}")
        
        # Classify result
        if svg_ok and png_ok:
            results['success'].append(name)
            print(f"{GREEN}✓ COMPLETE{NC}")
        elif svg_ok or png_ok:
            results['partial'].append(name)
            print(f"{YELLOW}⚠ PARTIAL{NC}")
        else:
            results['failed'].append(name)
            print(f"{RED}✗ FAILED{NC}")
    
    # Cleanup
    print(f"\n{BLUE}Cleaning temporary files...{NC}")
    import shutil
    shutil.rmtree('exports/temp', ignore_errors=True)
    
    # Final summary
    print(f"\n{BLUE}{'='*60}{NC}")
    print(f"{BLUE}EXPORT SUMMARY{NC}")
    print(f"{BLUE}{'='*60}{NC}\n")
    
    print(f"{GREEN}✓ Successful: {len(results['success'])}{NC}")
    for name in results['success']:
        print(f"  • {name}")
    
    if results['partial']:
        print(f"\n{YELLOW}⚠ Partial: {len(results['partial'])}{NC}")
        for name in results['partial']:
            print(f"  • {name}")
    
    if results['failed']:
        print(f"\n{RED}✗ Failed: {len(results['failed'])}{NC}")
        for name in results['failed']:
            print(f"  • {name}")
    
    # Count actual files
    svg_files = list(Path('exports/svg').glob('*.svg'))
    png_files = list(Path('exports/png').glob('*.png'))
    
    print(f"\n{BLUE}Output Files:{NC}")
    print(f"  SVG: {len(svg_files)} files → exports/svg/")
    print(f"  PNG: {len(png_files)} files → exports/png/")
    
    # Show file sizes
    try:
        result = subprocess.run(['du', '-sh', 'exports/'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            size = result.stdout.split()[0]
            print(f"  Total: {size}")
    except:
        pass
    
    print(f"\n{GREEN}✓ Export process complete!{NC}\n")
    
    # Return exit code
    if results['failed'] and not results['success']:
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()
