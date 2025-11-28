
import os
import hashlib
from pathlib import Path

def calculate_file_hash(file_path, chunk_size=8192):
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def find_duplicates(directory):
    """Find duplicate files in a directory"""
    files_by_size = {}
    duplicates = []
    
    print("Scanning files...")
    
    # First group by file size (quick check)
    for file_path in directory.rglob('*'):
        if file_path.is_file():
            try:
                file_size = file_path.stat().st_size
                if file_size not in files_by_size:
                    files_by_size[file_size] = []
                files_by_size[file_size].append(file_path)
            except Exception as e:
                print(f"Error accessing {file_path}: {e}")
    
    # Then check files with same size by hash
    total_files = sum(len(files) for files in files_by_size.values())
    processed = 0
    
    for file_size, file_list in files_by_size.items():
        if len(file_list) > 1:  # Potential duplicates
            hashes = {}
            
            for file_path in file_list:
                file_hash = calculate_file_hash(file_path)
                if file_hash:
                    if file_hash not in hashes:
                        hashes[file_hash] = []
                    hashes[file_hash].append(file_path)
                
                processed += 1
                if total_files > 100:  # Only show progress for large scans
                    print(f"Progress: {processed}/{total_files} files scanned", end='\r')
            
            # Add files with same hash to duplicates
            for file_list in hashes.values():
                if len(file_list) > 1:
                    duplicates.append(file_list)
    
    if total_files > 100:
        print("\nScanning complete!")
    return duplicates

def format_file_size(size_bytes):
    """Convert file size to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def display_duplicates(duplicates):
    """Display duplicate files in a formatted way"""
    if not duplicates:
        print("No duplicate files found!")
        return
    
    total_space = 0
    total_duplicates = 0
    
    print(f"\nFound {len(duplicates)} sets of duplicate files:")
    print("=" * 70)
    
    for i, duplicate_set in enumerate(duplicates, 1):
        file_size = duplicate_set[0].stat().st_size
        space_wasted = file_size * (len(duplicate_set) - 1)
        total_space += space_wasted
        total_duplicates += len(duplicate_set) - 1
        
        print(f"\n🎯 Set {i} - {format_file_size(file_size)} each")
        print(f"   📊 Wasted space: {format_file_size(space_wasted)}")
        print(f"   📁 Files ({len(duplicate_set)} copies):")
        
        for j, file_path in enumerate(duplicate_set, 1):
            # Show relative path if it's long
            try:
                relative_path = file_path.relative_to(Path.cwd())
                if len(str(relative_path)) > 50:
                    print(f"      {j}. .../{str(relative_path)[-45:]}")
                else:
                    print(f"      {j}. {relative_path}")
            except:
                if len(str(file_path)) > 50:
                    print(f"      {j}. .../{str(file_path)[-45:]}")
                else:
                    print(f"      {j}. {file_path}")
        
        print("   " + "-" * 50)
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"   • Total duplicate sets: {len(duplicates)}")
    print(f"   • Total duplicate files: {total_duplicates}")
    print(f"   • Potential space savings: {format_file_size(total_space)}")
    print(f"   • Average files per set: {total_duplicates/len(duplicates):.1f}")

def export_duplicates(duplicates, export_path):
    """Export duplicate list to a text file"""
    try:
        with open(export_path, 'w', encoding='utf-8') as f:
            f.write("DUPLICATE FILES REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            total_space = 0
            total_duplicates = 0
            
            for i, duplicate_set in enumerate(duplicates, 1):
                file_size = duplicate_set[0].stat().st_size
                space_wasted = file_size * (len(duplicate_set) - 1)
                total_space += space_wasted
                total_duplicates += len(duplicate_set) - 1
                
                f.write(f"Set {i} - {format_file_size(file_size)} each\n")
                f.write(f"Wasted space: {format_file_size(space_wasted)}\n")
                f.write("Files:\n")
                
                for file_path in duplicate_set:
                    f.write(f"  • {file_path}\n")
                
                f.write("\n" + "-" * 40 + "\n\n")
            
            f.write(f"SUMMARY:\n")
            f.write(f"Total duplicate sets: {len(duplicates)}\n")
            f.write(f"Total duplicate files: {total_duplicates}\n")
            f.write(f"Potential space savings: {format_file_size(total_space)}\n")
        
        print(f"✓ Report exported to: {export_path}")
        return True
    except Exception as e:
        print(f"✗ Error exporting report: {e}")
        return False

def duplicate_finder():
    """Main duplicate finding function"""
    print("=== DUPLICATE FILE FINDER ===")
    print("This tool will find duplicate files without deleting them.\n")
    
    # Select directory
    while True:
        dir_path = input("Enter the directory to scan (or 'c' for current directory): ").strip()
        
        if dir_path.lower() == 'c':
            directory = Path.cwd()
            break
        
        directory = Path(dir_path)
        if directory.exists() and directory.is_dir():
            break
        else:
            print("Invalid directory! Please try again.")
    
    print(f"\nScanning {directory} for duplicates...")
    print("This may take a while for large directories...")
    
    # Find duplicates
    duplicates = find_duplicates(directory)
    
    # Display results
    display_duplicates(duplicates)
    
    # Export option
    if duplicates:
        export_choice = input("\nWould you like to export this report to a text file? (y/n): ").lower()
        if export_choice == 'y':
            export_name = input("Enter filename (default: duplicates_report.txt): ").strip()
            if not export_name:
                export_name = "duplicates_report.txt"
            elif not export_name.endswith('.txt'):
                export_name += '.txt'
            
            export_duplicates(duplicates, export_name)
    
    input("\nPress Enter to continue...")

# Additional utility function for quick scanning
def quick_scan():
    """Quick scan of current directory"""
    print("Quick scanning current directory...")
    duplicates = find_duplicates(Path.cwd())
    display_duplicates(duplicates)
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    duplicate_finder()