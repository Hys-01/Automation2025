import os
from pathlib import Path

def select_directory():
    """Let user select a directory"""
    while True:
        dir_path = input("Enter the directory path (or 'c' for current directory): ").strip()
        
        if dir_path.lower() == 'c':
            return Path.cwd()
        
        path = Path(dir_path)
        if path.exists() and path.is_dir():
            return path
        else:
            print("Invalid directory! Please try again.")

def preview_rename(files, pattern, start_number):
    """Preview the renaming operation"""
    print("\nPreview of changes:")
    print("-" * 50)
    
    for i, file_path in enumerate(files, start=start_number):
        new_name = pattern.replace("{n}", str(i)).replace("{name}", file_path.stem)
        new_name += file_path.suffix
        print(f"  {file_path.name}")
        print(f"  → {new_name}")
        print()
    
    return input("Proceed with renaming? (y/n): ").lower() == 'y'

def batch_renamer():
    """Main batch renaming function"""
    print("=== BATCH FILE RENAMER ===")
    
    # Select directory
    directory = select_directory()
    
    # Get all files in directory
    files = [f for f in directory.iterdir() if f.is_file()]
    
    if not files:
        print("No files found in the selected directory!")
        input("Press Enter to continue...")
        return
    
    print(f"\nFound {len(files)} files in {directory}")
    
    # Show current files
    print("\nCurrent files:")
    for i, file_path in enumerate(files, 1):
        print(f"  {i}. {file_path.name}")
    
    # Get renaming pattern
    print("\nRenaming patterns:")
    print("  Use {n} for numbers (e.g., 1, 2, 3)")
    print("  Use {name} for original filename (without extension)")
    print("  Examples: 'vacation_{n}', 'document_{n}', '{name}_backup'")
    
    pattern = input("\nEnter renaming pattern: ").strip()
    start_number = int(input("Start numbering from (default 1): ") or "1")
    
    # Filter files by extension if requested
    filter_ext = input("Filter by extension (e.g., '.jpg', '.pdf' - leave empty for all files): ").strip()
    if filter_ext:
        if not filter_ext.startswith('.'):
            filter_ext = '.' + filter_ext
        files = [f for f in files if f.suffix.lower() == filter_ext.lower()]
        
        if not files:
            print(f"No files with extension {filter_ext} found!")
            input("Press Enter to continue...")
            return
        
        print(f"Filtered to {len(files)} files with extension {filter_ext}")
    
    # Preview and confirm
    if not preview_rename(files, pattern, start_number):
        print("Renaming cancelled.")
        input("Press Enter to continue...")
        return
    
    # Perform renaming
    success_count = 0
    for i, file_path in enumerate(files, start=start_number):
        try:
            new_name = pattern.replace("{n}", str(i)).replace("{name}", file_path.stem)
            new_name += file_path.suffix
            new_path = file_path.parent / new_name
            
            # Handle name conflicts
            counter = 1
            temp_new_path = new_path
            while temp_new_path.exists():
                stem = new_path.stem
                temp_new_path = new_path.parent / f"{stem}_{counter}{new_path.suffix}"
                counter += 1
            
            file_path.rename(temp_new_path)
            success_count += 1
            print(f"✓ Renamed: {file_path.name} → {temp_new_path.name}")
            
        except Exception as e:
            print(f"✗ Error renaming {file_path.name}: {e}")
    
    print(f"\nRenaming complete! {success_count}/{len(files)} files renamed successfully.")
    input("Press Enter to continue...")

if __name__ == "__main__":
    batch_renamer()