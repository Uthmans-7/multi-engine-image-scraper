import os
from PIL import Image
from imagededup.methods import PHash

TARGET_FOLDER = os.path.join( ".")

MIN_FILE_SIZE_KB = 10  # Trashes files smaller than 10KB
SIMILARITY_THRESHOLD = 15 # The magic PHash number for visual clones

def clean_dataset():
    phasher = PHash()
    
    if not os.path.exists(TARGET_FOLDER):
        print(f" ERROR: Cannot find the folder '{TARGET_FOLDER}'")
        print("Check your configuration path at the top of the script!")
        return

    total_corrupted_removed = 0
    total_duplicates_removed = 0

    print(f"\n INITIATING MASTER CLEANUP FOR: {TARGET_FOLDER}")

    for folder in os.listdir(TARGET_FOLDER):
        folder_path = os.path.join(TARGET_FOLDER, folder)
        
        if not os.path.isdir(folder_path):
            continue

        print(f"\n{'='*40}")
        print(f" CLEANING: {folder}")
        print(f"{'='*40}")

        # --- TASK 1: REMOVE CORRUPTED & TINY FILES ---
        print("Checking for corrupted/small files...")
        corrupted_count = 0
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            # Check file size
            if os.path.getsize(file_path) < MIN_FILE_SIZE_KB * 1024:
                os.remove(file_path)
                corrupted_count += 1
                continue

            # Check if file is visually readable
            try:
                with Image.open(file_path) as img:
                    img.verify() 
            except Exception:
                os.remove(file_path)
                corrupted_count += 1
                
        print(f"Trashed {corrupted_count} tiny or corrupted files.")
        total_corrupted_removed += corrupted_count

        # --- TASK 2: REMOVE VISUAL DUPLICATES ---
        print("Finding visual clones...")
        try:
            duplicates = phasher.find_duplicates_to_remove(
                image_dir=folder_path, 
                max_distance_threshold=SIMILARITY_THRESHOLD
            )
            
            for dup_file in duplicates:
                dup_path = os.path.join(folder_path, dup_file)
                if os.path.exists(dup_path):
                    os.remove(dup_path)
            
            print(f"Deleted {len(duplicates)} identical clones.")
            total_duplicates_removed += len(duplicates)
            
        except Exception as e:
            print(f"Skipping similarity check for {folder} due to error: {e}")

    print("\n" + "="*40)
    print(" MASTER CLEANUP COMPLETE!")
    print(f" Target Cleaned: {TARGET_FOLDER}")
    print(f" Total Tiny/Corrupt Removed: {total_corrupted_removed}")
    print(f" Total Duplicates Destroyed: {total_duplicates_removed}")
    print("="*40)

if __name__ == "__main__":
    clean_dataset()