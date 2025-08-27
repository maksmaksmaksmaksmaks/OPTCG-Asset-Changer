from pathlib import Path
# pyinstaller --onefile --collect-all UnityPy --collect-all archspec TESTING_FOLDER/AssetChanger/AssetChanger.py
import UnityPy
from PIL import Image


def primary_check():
    if Path('../OPTCGSim_Data/sharedassets1.assets').exists():
        print("Asset folder found")
    else:
        print("CANT FIND ASSETS")
        exit(1)
def backup_check():
    if Path('BACKUP_ASSETS/sharedassets1.assets').exists():
        print("Backup already made")
    else:
        print("making backup")
        backup_make()

def backup_make():
    original=Path('../OPTCGSim_Data/sharedassets1.assets')
    copied=Path('BACKUP_ASSETS/sharedassets1.assets')
    copied.parent.mkdir(parents=True, exist_ok=True)
    copied.write_bytes(original.read_bytes())

def changes_check():
    if Path('changes.txt').exists():
        print("Changes found")
    else:
        print("Missing changes")
        exit(1)


def read_dict(filename):
    texture_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line:
                key, value = line.split(':', 1)
                texture_dict[key.strip()] = value.strip()
            else:
                print(f'*** changes.txt not in proper format:\n{line}')
    return texture_dict


TEXTURE_MAPPINGS=read_dict("changes.txt")
IMAGES_FOLDER = "images"
ASSETS_FOLDER = "BACKUP_ASSETS"
OUTPUT_FOLDER = "../OPTCGSim_Data"
ASSETS_FILE = "sharedassets1.assets"


def validate_files():
    """Validate that all required files exist"""
    missing_files = []

    # Check assets file
    assets_path = Path(ASSETS_FOLDER) / ASSETS_FILE
    if not assets_path.exists():
        missing_files.append(f"Assets file: {assets_path}")

    # Check image files
    for image_file in TEXTURE_MAPPINGS.values():
        image_path = Path(IMAGES_FOLDER) / image_file
        if not image_path.exists():
            missing_files.append(f"Image file: {image_path}")

    if missing_files:
        print("*** Missing files:")
        for file in missing_files:
            print(f"  - {file}")
        return False

    return True


def load_replacement_images():
    """Load all replacement images into memory"""
    images = {}

    for asset_name,image_file in TEXTURE_MAPPINGS.items():
        image_path = Path(IMAGES_FOLDER) / image_file
        try:
            img = Image.open(image_path)
            images[asset_name] = img
            print(f"Loaded {image_file} ({img.size}) for asset '{asset_name}'")
        except Exception as e:
            print(f"*** Failed to load {image_file}: {e}")
            return None

    return images


def modify_multiple_textures(input_path, output_path, replacement_images):
    """Modify multiple textures in Unity assets file"""
    print(f"\nLoading Unity assets from: {input_path}")
    try:
        env = UnityPy.load(str(input_path))
    except Exception as e:
        raise Exception(f"Failed to load Unity assets: {e}")

    # Track found and modified textures
    found_textures = {}
    modified_count = 0

    # Search through all objects
    print("\nSearching for textures...")
    for obj in env.objects:
        if obj.type.name == "Texture2D":
            data = obj.read()
            texture_name = data.m_Name

            # Check if this texture is in our replacement list
            if texture_name in replacement_images:
                found_textures[texture_name] = data
                print(f"Found target texture: {texture_name} ({data.m_Width}x{data.m_Height})")

    # Perform replacements
    print(f"\nPerforming replacements...")
    for asset_name, replacement_img in replacement_images.items():
        if asset_name in found_textures:
            data = found_textures[asset_name]

            # Check dimensions
            if replacement_img.size != (data.m_Width, data.m_Height):
                print(f"***  Warning: {asset_name} size mismatch!")
                print(f"   Original: {data.m_Width}x{data.m_Height}, New: {replacement_img.size}")
                print(f"*** Skipping {asset_name} due to size mismatch")
                continue

            try:
                # Replace the texture
                data.image = replacement_img
                data.save()
                modified_count += 1
                print(f"Replaced {asset_name}")

            except Exception as e:
                print(f"*** Failed to replace {asset_name}: {e}")
        else:
            print(f"*** Asset '{asset_name}' not found in Unity file")

    # Save the modified assets file
    if modified_count > 0:
        try:
            with open(output_path, "wb") as f:
                f.write(env.file.save())
            print(f"\nModified assets file saved: {output_path}")
            print(f"Successfully modified {modified_count} textures")
            return True

        except Exception as e:
            raise Exception(f"Failed to save modified assets: {e}")
    else:
        print("\n***  No textures were modified")
        return False


def main():
    print("Unity Multi-Texture Replacement Tool")
    print("=" * 40)
    primary_check()
    changes_check()
    backup_check()
    # Show current configuration
    print(f"\nConfiguration:")
    print(f"Images folder: {IMAGES_FOLDER}")
    print(f"Assets folder: {ASSETS_FOLDER}")
    print(f"Output folder: {OUTPUT_FOLDER}")
    print(f"Target file: {ASSETS_FILE}")
    print(f"\nTexture mappings:")
    for asset_name,img_file in TEXTURE_MAPPINGS.items():
        print(f"  {img_file} → {asset_name}")


    print(f"\nOutput folder ready: {OUTPUT_FOLDER}")

    # Validate files exist
    print(f"\nValidating files...")
    if not validate_files():
        return

    # Load replacement images
    print(f"\nLoading replacement images...")
    replacement_images = load_replacement_images()
    if replacement_images is None:
        print("*** Failed to load images. Exiting.")
        return

    # Setup file paths
    input_file = Path(ASSETS_FOLDER) / ASSETS_FILE

    # Generate output filename
    output_file = Path(OUTPUT_FOLDER) / ASSETS_FILE

    try:
        # Perform the modifications
        success = modify_multiple_textures(input_file, output_file, replacement_images)

        if success:
            print(f"\n" + "=" * 50)
            print(f"SUCCESS: Modified assets file created!")
            print(f"Output file: {output_file}")
            print(f"Original file unchanged: {input_file}")
        else:
            print(f"\n***  No modifications were made.")

    except Exception as e:
        print(f"\n*** Error: {e}")
        print(f"Original file unchanged")


if __name__ == "__main__":
    main()
    input()

