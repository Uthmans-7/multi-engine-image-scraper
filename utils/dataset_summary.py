import os

# Configuration
TARGET_FOLDER = os.path.join(".")

def generate_executive_summary():
    if not os.path.exists(TARGET_FOLDER):
        print(f"ERROR: Cannot find folder '{TARGET_FOLDER}'. Check your path.")
        return

    total_images = 0
    class_counts = {}

    # Threshold Bins
    excellent = []   # 200+
    good = []        # 100 - 199
    borderline = []  # 70 - 99
    critical = [] 
    critical01 = []    # Under 70

    # Scan the directory alphabetically
    for folder_name in sorted(os.listdir(TARGET_FOLDER)):
        folder_path = os.path.join(TARGET_FOLDER, folder_name)
        
        if os.path.isdir(folder_path):
            images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            count = len(images)
            
            class_counts[folder_name] = count
            total_images += count

            # Sort into bins
            class_info = f"{folder_name.ljust(40)} : {count} images"
            if count >= 200:
                excellent.append(class_info)
            elif count >= 100:
                good.append(class_info)
            elif count >= 70:
                borderline.append(class_info)
            elif count >= 40:
                critical.append(class_info)
            else:
                critical01.append(class_info)

    total_classes = len(class_counts)

    # Print the Executive Report
    print("\n" + "=" * 60)
    print("DATASET EXECUTIVE SUMMARY: " + TARGET_FOLDER.upper())
    print("=" * 60)
    print(f"TOTAL IMAGES : {total_images}")
    print(f"TOTAL CLASSES: {total_classes}")
    print("-" * 60)
    
    print("\n[ MACRO HEALTH METRICS ]")
    print(f"Excellent (200+ images)  : {len(excellent)} classes")
    print(f"Good (100-199 images)    : {len(good)} classes")
    print(f"Borderline (70-99 images): {len(borderline)} classes")
    print(f"Critical (Under 70)      : {len(critical)} classes")
    print(f"Critical01 (Under 40)      : {len(critical01)} classes")
    print("-" * 60)

    # Print Detailed Breakdown
    if excellent:
        print("\n[ EXCELLENT TIER (200+) ]")
        for item in excellent: print(item)

    if good:
        print("\n[ GOOD TIER (100 - 199) ]")
        for item in good: print(item)

    if borderline:
        print("\n[ BORDERLINE TIER (70 - 99) ]")
        for item in borderline: print(item)

    if critical:
        print("\n[ CRITICAL TIER (Under 70) ]")
        for item in critical: print(item)

    if critical01:
        print("\n[ CRITICAL TIER (Under 40) ]")
        for item in critical01: print(item)
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    generate_executive_summary()