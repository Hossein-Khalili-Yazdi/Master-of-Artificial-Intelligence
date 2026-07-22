def min_max_scaling(numbers, old_min, old_max, new_min, new_max):
    """
    اعداد را با استفاده از روش Min-Max به محدوده جدید تبدیل می‌کند.
    
    فرمول:
    X_scaled = ((X - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    """
    # بررسی تقسیم بر صفر
    if old_max - old_min == 0:
        return [new_min] * len(numbers) # اگر همه اعداد یکسان باشند، همه به new_min تبدیل می‌شوند

    transformed_numbers = []
    for x in numbers:
        # محاسبه تبدیل
        x_scaled = ((x - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
        transformed_numbers.append(x_scaled)

    return transformed_numbers

# --- بخش ورودی‌ها ---

print("برنامه تبدیل اعداد به روش Min-Max Scaling")
print("-----------------------------------------")

# 1. گرفتن ۱۰ عدد از کاربر
numbers = []
print("لطفاً ۱۰ عدد را یکی پس از دیگری وارد کنید:")
for i in range(10):
    while True:
        try:
            num = float(input(f"عدد {i+1}: "))
            numbers.append(num)
            break
        except ValueError:
            print("ورودی نامعتبر است، لطفاً یک عدد وارد کنید.")

# 2. گرفتن محدوده فعلی (قدیم)
while True:
    try:
        old_min = float(input("\nلطفاً حداقل (Min) محدوده فعلی اعداد (Old Min) را وارد کنید: "))
        old_max = float(input("لطفاً حداکثر (Max) محدوده فعلی اعداد (Old Max) را وارد کنید: "))
        if old_min >= old_max:
            print(".باشد (Old Max) باید بزرگتر از حداقل (Old Min) حداقل (Old Max)")
        else:
            break
    except ValueError:
        print(".ورودی نامعتبر است، لطفاً یک عدد وارد کنید")

# 3. گرفتن محدوده جدید
while True:
    try:
        new_min = float(input("\nلطفاً حداقل (Min) محدوده جدید (New Min) را وارد کنید: "))
        new_max = float(input("لطفاً حداکثر (Max) محدوده جدید (New Max) را وارد کنید: "))
        if new_min >= new_max:
            print(".باشد (New Max) باید بزرگتر از حداقل (New Min) حداقل (New Max)")
        else:
            break
    except ValueError:
        print(".ورودی نامعتبر است، لطفاً یک عدد وارد کنید")

# --- بخش پردازش و خروجی ---

# اجرای تابع تبدیل
transformed_list = min_max_scaling(numbers, old_min, old_max, new_min, new_max)

print("\n\nنتایج تبدیل Min-Max Scaling:")
print("-----------------------------------------")
print(f"اعداد اصلی: {numbers}")
print(f"محدوده فعلی: [{old_min}, {old_max}]")
print(f"محدوده جدید: [{new_min}, {new_max}]")
print("\n")

# نمایش نتایج به صورت جفتی
for original, transformed in zip(numbers, transformed_list):
    print(f"عدد اصلی: {original:<10.4f} -> عدد تبدیل شده: {transformed:.4f}")
