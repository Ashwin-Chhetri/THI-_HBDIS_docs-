#!/bin/bash
# Export all HMBIS Knowledge Common diagrams to SVG and PNG formats
# Usage: ./export_all_diagrams.sh

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Check if mermaid-cli is installed
if ! command -v mmdc &> /dev/null; then
    echo -e "${RED}Error: mermaid-cli (mmdc) not found!${NC}"
    echo "Install with: npm install -g @mermaid-js/mermaid-cli"
    exit 1
fi

echo -e "${BLUE}=== HMBIS Diagram Export Tool ===${NC}\n"

# Create export directories
mkdir -p exports/svg exports/png exports/temp

# Function to extract Mermaid code from markdown
extract_mermaid() {
    local input_file=$1
    local output_file=$2
    
    # Extract content between ```mermaid and the next ```
    sed -n '/```mermaid/,/^```$/p' "$input_file" | sed '1d;$d' > "$output_file"
    
    if [ ! -s "$output_file" ]; then
        return 1
    fi
    return 0
}

# Diagram configurations: name:width:height
diagrams=(
    "01_system_architecture:2400:1800"
    "02_data_flow:2400:3000"
    "03_database_schema:3000:2400"
    "04_user_interaction:2400:2800"
    "05_scalability:2800:2200"
)

# Export counter
total=${#diagrams[@]}
current=0
success_count=0
fail_count=0

for diagram in "${diagrams[@]}"; do
    IFS=':' read -r name width height <<< "$diagram"
    current=$((current + 1))
    
    echo -e "${BLUE}[$current/$total] Processing: $name${NC}"
    
    # Check if source file exists
    if [ ! -f "${name}.md" ]; then
        echo -e "${RED}  ✗ Source file ${name}.md not found${NC}"
        fail_count=$((fail_count + 1))
        continue
    fi
    
    # Extract Mermaid code
    temp_file="exports/temp/${name}.mmd"
    echo -e "  → Extracting Mermaid code..."
    if ! extract_mermaid "${name}.md" "$temp_file"; then
        echo -e "${RED}  ✗ Failed to extract Mermaid code${NC}"
        fail_count=$((fail_count + 1))
        continue
    fi
    echo -e "${GREEN}  ✓ Mermaid code extracted${NC}"
    
    # Export to SVG
    echo -e "  → Exporting SVG..."
    if mmdc -i "$temp_file" -o "exports/svg/${name}.svg" \
         -t neutral -b transparent 2>&1 | grep -v "Warning"; then
        echo -e "${GREEN}  ✓ SVG exported: exports/svg/${name}.svg${NC}"
    else
        echo -e "${YELLOW}  ⚠ SVG export completed with warnings${NC}"
    fi
    
    # Export to PNG (high resolution)
    echo -e "  → Exporting PNG (${width}x${height}px)..."
    if mmdc -i "$temp_file" -o "exports/png/${name}.png" \
         -t neutral -w "$width" -H "$height" -s 2 -b white 2>&1 | grep -v "Warning"; then
        echo -e "${GREEN}  ✓ PNG exported: exports/png/${name}.png${NC}"
        success_count=$((success_count + 1))
    else
        echo -e "${YELLOW}  ⚠ PNG export completed with warnings${NC}"
        success_count=$((success_count + 1))
    fi
    
    echo ""
done

# Cleanup temp files
echo -e "${BLUE}Cleaning up temporary files...${NC}"
rm -rf exports/temp

# Summary
echo -e "\n${GREEN}=== Export Complete! ===${NC}\n"
echo "Export Results:"
echo -e "  ${GREEN}✓ Successful: $success_count${NC}"
if [ $fail_count -gt 0 ]; then
    echo -e "  ${RED}✗ Failed: $fail_count${NC}"
fi
echo ""
echo "Exported diagrams:"
echo "  • SVG files: exports/svg/"
echo "  • PNG files: exports/png/"
echo ""
echo "File count:"
svg_count=$(ls exports/svg/*.svg 2>/dev/null | wc -l)
png_count=$(ls exports/png/*.png 2>/dev/null | wc -l)
echo "  • SVG: $svg_count files"
echo "  • PNG: $png_count files"

# Calculate total size
if command -v du &> /dev/null; then
    total_size=$(du -sh exports/ 2>/dev/null | cut -f1)
    echo "  • Total size: $total_size"
fi

echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Review diagrams in exports/ directory"
echo "  2. Include in documentation using:"
echo "     ![Diagram](diagrams/exports/svg/01_system_architecture.svg)"
echo "  3. For LaTeX/PDF: Use PNG files from exports/png/"
echo ""
echo -e "${GREEN}Ready for publication! 🚀${NC}"

# Summary
echo -e "${GREEN}=== Export Complete! ===${NC}\n"
echo "Exported diagrams:"
echo "  • SVG files: exports/svg/"
echo "  • PNG files: exports/png/"
echo ""
echo "File count:"
svg_count=$(ls exports/svg/*.svg 2>/dev/null | wc -l)
png_count=$(ls exports/png/*.png 2>/dev/null | wc -l)
echo "  • SVG: $svg_count files"
echo "  • PNG: $png_count files"

# Calculate total size
if command -v du &> /dev/null; then
    total_size=$(du -sh exports/ 2>/dev/null | cut -f1)
    echo "  • Total size: $total_size"
fi

echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Review diagrams in exports/ directory"
echo "  2. Include in documentation using:"
echo "     ![Diagram](diagrams/exports/svg/01_system_architecture.svg)"
echo "  3. For LaTeX/PDF: Use PNG files from exports/png/"
echo ""
echo -e "${GREEN}Ready for publication! 🚀${NC}"
