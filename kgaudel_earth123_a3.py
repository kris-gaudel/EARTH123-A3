from decimal import Decimal, ROUND_HALF_UP
# Need this library for precision

# Constants with precise decimal values
WATERSHED_AREA_KM2 = Decimal('4')
WATERSHED_AREA_M2 = WATERSHED_AREA_KM2 * Decimal('1000000')
LAKE_AREA_KM2 = Decimal('0.0645')
LAKE_AREA_M2 = LAKE_AREA_KM2 * Decimal('1000000')

# Month data with Decimal values for precision
month_map = {
    # Month: (number of days, precipitation in mm/month, discharge in m^3/s)
    "January": (31, Decimal('63.7'), Decimal('0.01')),
    "February": (28, Decimal('80.4'), Decimal('0')),
    "March": (31, Decimal('36.8'), Decimal('0.14')),
    "April": (30, Decimal('32.4'), Decimal('0.21')),
    "May": (31, Decimal('62.7'), Decimal('0.11')),
    "June": (30, Decimal('36.8'), Decimal('0.04')),
    "July": (31, Decimal('20.4'), Decimal('0.03')),
    "August": (31, Decimal('51.9'), Decimal('0.04')),
    "September": (30, Decimal('73.6'), Decimal('0.06')),
    "October": (31, Decimal('80.4'), Decimal('0.11')),
    "November": (30, Decimal('61.7'), Decimal('0.10')),
    "December": (31, Decimal('42.4'), Decimal('0.07'))
}

def calculate_discharge_mm(days: int, discharge_m3s: Decimal) -> Decimal:
    seconds_per_day = Decimal('86400')  # 24 * 3600
    monthly_discharge_m3 = discharge_m3s * Decimal(str(days)) * seconds_per_day
    return (monthly_discharge_m3 / WATERSHED_AREA_M2 * Decimal('1000')).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

# Part a) Yearly ET calculation
print("\nPart a) Yearly Evapotranspiration Calculation")
print("-" * 50)

discharge_mm = {}
total_precip = Decimal('0')

for month, (days, precip, discharge) in month_map.items():
    monthly_discharge_mm = calculate_discharge_mm(days, discharge)
    discharge_mm[month] = monthly_discharge_mm
    total_precip += precip
    
    print(f"{month}:")
    print(f"  Precipitation: {precip} mm")
    print(f"  Discharge: {monthly_discharge_mm} mm")

total_discharge_mm = sum(discharge_mm.values())
yearly_et = total_precip - total_discharge_mm
daily_et = (yearly_et / Decimal('365')).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

print("\nYearly Totals:")
print(f"Total precipitation: {total_precip} mm")
print(f"Total discharge: {total_discharge_mm} mm")
print(f"Total evapotranspiration: {yearly_et} mm")
print(f"Average daily evapotranspiration: {daily_et} mm/day")

# Part b) July storage calculation
print("\nPart b) July Storage Change")
print("-" * 50)

# July calculations
july_days, july_precip, july_discharge = month_map["July"]
july_et_cm_day = Decimal('0.053')

# Convert to m^3
july_precip_m3 = (july_precip / Decimal('1000')) * WATERSHED_AREA_M2
july_discharge_m3 = july_discharge * Decimal(str(july_days)) * Decimal('86400')
july_et_m3 = (july_et_cm_day / Decimal('100')) * Decimal(str(july_days)) * WATERSHED_AREA_M2

july_precip_m3 = july_precip_m3.quantize(Decimal('0.01'))
july_discharge_m3 = july_discharge_m3.quantize(Decimal('0.01'))
july_et_m3 = july_et_m3.quantize(Decimal('0.01'))
july_storage_change = (july_precip_m3 - july_discharge_m3 - july_et_m3).quantize(Decimal('0.01'))

print(f"July precipitation volume: {july_precip_m3} m^3")
print(f"July discharge volume: {july_discharge_m3} m^3")
print(f"July ET volume: {july_et_m3} m^3")
print(f"July storage change: {july_storage_change} m^3")

# Part c) Lake level change
print("\nPart c) Lake Level Change")
print("-" * 50)

lake_level_change = (july_storage_change / LAKE_AREA_M2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
print(f"Lake level change: {lake_level_change} m")
