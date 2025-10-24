def calculate_stats(records):
    if not records:
        return "Записей пока нет"
    
    durations = [r[0] for r in records]
    avg = sum(durations) / len(durations)
    return f"📊 Ваша статистика:\nСреднее время сна: {avg:.1f} часов\nВсего записей: {len(records)}"

def validate_time(time_str):
    try:
        from datetime import datetime
        datetime.strptime(time_str, '%H:%M')
        return True
    except:
        return False