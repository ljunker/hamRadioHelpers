frequency = float(input("Enter desired frequency (MHz): "))
wavelength = 300 / frequency
dipollength = wavelength / 2
leg_length = dipollength / 2
print(f"Wave length: {wavelength}")
print(f"Dipol length: {dipollength}")
print(f"Leg length: {leg_length}")