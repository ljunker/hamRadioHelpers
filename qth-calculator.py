import geocoder
import argparse

def dms_to_decimal(degrees, minutes, seconds, direction):
    decimal = degrees + (minutes / 60) + (seconds / 3600)
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal


def lat_lon_to_maidenhead(latitude, longitude):
    longitude += 180
    latitude += 90

    field_lon = chr(int(longitude // 20) + ord('A'))
    field_lat = chr(int(latitude // 10) + ord('A'))

    square_lon = int((longitude % 20) // 2)
    square_lat = int(latitude % 10)

    subsquare_lon = chr(int((longitude % 2) * 12) + ord('a'))
    subsquare_lat = chr(int((latitude % 1) * 24) + ord('a'))

    maidenhead = f"{field_lon}{field_lat}{square_lon}{square_lat}{subsquare_lon}{subsquare_lat}"
    return maidenhead


def parse_coordinates_from_flags():
    parser = argparse.ArgumentParser(description="Calculate Maidenhead Locator from coordinates.")
    parser.add_argument("--lat", type=float, help="Latitude in decimal degrees")
    parser.add_argument("--lon", type=float, help="Longitude in decimal degrees")
    parser.add_argument("--dms", action="store_true", help="Use DMS format for input")
    parser.add_argument("--auto", action="store_true", help="Automatically detect current location")

    args = parser.parse_args()

    if args.auto:
        return get_current_location()
    elif args.dms:
        print("Enter latitude and longitude in DMS format.")
        lat_deg = int(input("Enter latitude degrees: "))
        lat_min = int(input("Enter latitude minutes: "))
        lat_sec = float(input("Enter latitude seconds: "))
        lat_dir = input("Enter latitude direction (N/S): ").strip().upper()

        lon_deg = int(input("Enter longitude degrees: "))
        lon_min = int(input("Enter longitude minutes: "))
        lon_sec = float(input("Enter longitude seconds: "))
        lon_dir = input("Enter longitude direction (E/W): ").strip().upper()

        latitude = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
        longitude = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)
    elif args.lat is not None and args.lon is not None:
        latitude = args.lat
        longitude = args.lon
    else:
        raise ValueError("You must specify either --lat and --lon, or --auto, or --dms.")

    return latitude, longitude


def get_current_location():
    g = geocoder.ip("me")
    if g.ok:
        return g.latlng
    else:
        return None


if __name__ == "__main__":
    try:
        lat, lon = parse_coordinates_from_flags()
        locator = lat_lon_to_maidenhead(lat, lon)
        print(f"Maidenhead Locator: {locator}")
    except ValueError as e:
        print(f"Error: {e}")
