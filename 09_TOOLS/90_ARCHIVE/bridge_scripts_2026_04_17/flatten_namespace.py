import os

UPLINK_DIR = "/Users/yves/Documents/☀️ Emergentism_org/02_ORGANISM/03_UPLINK"
renamed = 0

for d in os.listdir(UPLINK_DIR):
    d_path = os.path.join(UPLINK_DIR, d)
    if os.path.isdir(d_path) and not d.startswith(".") and not d == "NOTEBOOK_LM_PACKAGES":
        # Extract base name. Example: "01_OFN" -> "OFN"
        folder_prefix = d.split("_", 1)[1] if "_" in d else d
        
        for f in os.listdir(d_path):
            if f.endswith(".md"):
                f_path = os.path.join(d_path, f)
                
                # Check if it's already properly prefixed so we don't accidentally rename twice if rerun
                if not f.startswith(f"{folder_prefix}_"):
                    new_name = f"{folder_prefix}_{f}"
                    new_path = os.path.join(d_path, new_name)
                    os.rename(f_path, new_path)
                    print(f"Renamed: {d}/{f} -> {new_name}")
                    renamed += 1

print(f"\nNamespace Flattening Complete. Total files formally renamed: {renamed}")
