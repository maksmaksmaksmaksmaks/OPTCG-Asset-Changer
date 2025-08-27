# OPTCG Asset Changer

A tool for modifying textures in the OPTCG sim.

## Instructions

### 1. Setup
Place the `AssetChanger` folder next to your `OPTCGSim.exe` file:
```
Your Game Folder/
├── OPTCGSim.exe
└── AssetChanger/
    ├── images/
    ├── output/
    ├── AssetChanger.exe
    └── AssetChanger.py
```

### 2. Add Your Images
- Put your custom images in the `images` folder
- **Important**: Make sure they are the proper size
- Check the required sizes in the reference text file

### 3. Configure Changes
Edit the `changes.txt` file using this format:
```
# Comments start with #
UnityAssetName: NewImage.png
```

**Example:**
```
# UI Elements
buttonLong_beige: my_custom_button.png
Background: new_background.png
YouWin: victory_screen.png

# You can reuse the same image for multiple assets
Arrow: my_arrow.png
AttackArrow: my_arrow.png
```

### 4. Run the Tool
You can just run the .exe or install UnityPy and run the script yourself.
## Important Notes

- The tool will save your original assets file in the backup folder

---

**make it look pretty :3**  