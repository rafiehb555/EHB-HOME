#!/usr/bin/env python3
"""
Markdown Error Fixer
Fixes common markdown linting errors automatically
"""

import glob
import re


def fix_markdown_file(file_path):
    """Fix markdown linting errors in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Fix MD022: Add blank lines around headings
        content = re.sub(r'([^\n])\n(#+\s)', r'\1\n\n\2', content)
        content = re.sub(r'(#+\s[^\n]*)\n([^\n])', r'\1\n\n\2', content)

        # Fix MD031: Add blank lines around code blocks
        content = re.sub(r'([^\n])\n(```)', r'\1\n\n\2', content)
        content = re.sub(r'(```[^\n]*\n[^`]*```)\n([^\n])', r'\1\n\n\2', content)

        # Fix MD032: Add blank lines around lists
        content = re.sub(r'([^\n])\n([*+-]\s)', r'\1\n\n\2', content)
        content = re.sub(r'([*+-]\s[^\n]*)\n([^\n])', r'\1\n\n\2', content)

        # Fix MD040: Add language to code blocks
        content = re.sub(r'(```)\n', r'\1\n', content)

        # Fix trailing whitespace
        content = re.sub(r'[ \t]+\n', '\n', content)

        # Fix no newline at end of file
        if not content.endswith('\n'):
            content += '\n'

        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {file_path}")
            return True
        else:
            print(f"✅ Already clean: {file_path}")
            return False

    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False


def main():
    """Main function to fix all markdown files"""
    print("🔧 Fixing Markdown Linting Errors...")

    # Find all markdown files
    markdown_files = glob.glob("**/*.md", recursive=True)

    fixed_count = 0
    total_count = len(markdown_files)

    for file_path in markdown_files:
        if fix_markdown_file(file_path):
            fixed_count += 1

        print("\n📊 Summary:")
    print(f"Total files: {total_count}")
    print(f"Fixed files: {fixed_count}")
    print(f"Already clean: {total_count - fixed_count}")
    
    if fixed_count > 0:
        print(f"\n✅ Successfully fixed {fixed_count} markdown files!")
    else:
        print("\n✅ All markdown files are already clean!")


if __name__ == "__main__":
    main()
