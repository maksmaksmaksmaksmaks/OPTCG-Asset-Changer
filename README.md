# OPTCG Asset Changer

A tool for modifying textures in the OPTCG sim
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
buttonLong_beige: buttonLong_beige_new
Background: Background.png
YouWin: YouWin_GOD_SLAIN.png
```

### 4. Run the Tool
You can just run the .exe or install UnityPy and run the script yourself.

### 5. Link to latest release
- [Release](https://github.com/maksmaksmaksmaksmaks/OPTCG-Asset-Changer/releases)


#### Important Notes

- The tool will save your original assets file in the backup folder



---

**make it look pretty :3**  