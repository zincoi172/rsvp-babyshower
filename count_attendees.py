import csv

def count_total_guests(file_path='responses.csv'):
    total = 0
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            # Format: [timestamp, name, attendance, guests]
            try:
                attendance = row[2].strip().lower()
                guests = int(row[3])
                if attendance == 'yes':
                    total += guests
            except (IndexError, ValueError):
                continue  # Skip malformed rows
    return total

if __name__ == "__main__":
    count = count_total_guests()
    print(f"🎉 Total number of attendees (including +1s): {count}")
