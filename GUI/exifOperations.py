# NOTE all exif tags https://exiv2.org/tags.html
# also view xmp and iptc as meta standards for images

# NOTE  This is a PILLOW implementation for exif data usage
from PIL import Image  # https://pillow.readthedocs.io/en/stable/reference/Image.html
from PIL.ExifTags import TAGS


def get_key_from_value(d, val):
    # NOTE get the key for a value in a dictionary (reverse look up)
    # necessary because the exif tags are numerical so for ease of access we can use the clear text and translate into numerical value
    # NOTE: could be skipped, if one always looks up the numerical value by hand and inputs them.
    keys = [k for k, v in d.items() if v == val]
    if len(keys) > 1:
        print('error in: get_key_from_value() for exif data. More than one key. Not Unique')
        return None
    if keys:
        return keys[0]
    return None


def pil_write_single_exif(data=None, key_Clear=None, value=None):
    if data is None:
        print('need exif data handle to write')
        return -1
    data[get_key_from_value(TAGS, key_Clear)] = value
    return 0


def pil_write_dict_exif(data=None, dictionary=None):
    if data is None:
        print('need exif data handle to write')
        return -1
    for k, v in dictionary.items():
        data[get_key_from_value(TAGS, k)] = v
    return 0


def pil_sort_exif(data=None):
    # BUG doesn't seem to be working. Even tho it is displayed during debugging as changed and the order is fine, as soon as you print it,
    # it reverts back to some other order, after saving the order has changed again. Seems to be an issue with handling of the dictionary.
    # NOTE is not important for our usage
    if data is None:
        print('need exif data handle to write')
        return -1
    exif_sorted = dict(sorted(data.items()))
    # needs to be convoluted so the exif data remains, is the easiest way to sort the dictionary part of it tho
    for k, v in exif_sorted.items():
        del data[k]
        data[k] = v
    return data


def pil_print_pretty_exif(data=None):
    if data is None:
        print('need exif data handle to write')
        return -1
    # sort for visibility
    exif_sorted = dict(sorted(data.items()))
    # iterating over all EXIF data fields
    print(f"Tag_ID", f"Field Name       Value")
    for tag_id in exif_sorted:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        date = data.get(tag_id)
        # decode bytes
        if isinstance(date, bytes):
            date = date.decode()
        print(f"{tag_id:6}", f"{tag:15}: {date}")
    print('')
    return 0
