"""Read calendar health counts locally; never read or print appointment subjects."""
import json
from datetime import datetime, timedelta
import pythoncom
from win32com.client import dynamic

def wall(value):
    return datetime(value.year, value.month, value.day, value.hour, value.minute)

pythoncom.CoInitialize()
try:
    app = dynamic.Dispatch('Outlook.Application')
    now = datetime.now()
    end = now + timedelta(days=60)
    results = []
    for store in app.Session.Stores:
        if str(store.DisplayName) != 'iCloud':
            continue
        for folder in store.GetRootFolder().Folders:
            if int(folder.DefaultItemType) != 1:
                continue
            row = dict(calendar=str(folder.Name), total=0, read=0, errors=0,
                       recurring_series=0, upcoming_nonrecurring=0,
                       upcoming_busy_timed=0, upcoming_all_day=0)
            items = folder.Items
            items.IncludeRecurrences = False
            row['total'] = int(items.Count)
            for index in range(1, row['total'] + 1):
                try:
                    item = items.Item(index)
                    start, finish = wall(item.Start), wall(item.End)
                    recurring = bool(item.IsRecurring)
                    busy, all_day = int(item.BusyStatus), bool(item.AllDayEvent)
                    row['read'] += 1
                    if recurring:
                        row['recurring_series'] += 1
                    elif finish > now and start < end:
                        row['upcoming_nonrecurring'] += 1
                        row['upcoming_all_day'] += int(all_day)
                        row['upcoming_busy_timed'] += int(not all_day and busy in (2, 3))
                except Exception:
                    row['errors'] += 1
            results.append(row)
    print(json.dumps(dict(calendars=results, subjects_read=False, events_changed=False,
                         recurrence_expanded=False, phone_sync_freshness_verified=False), ensure_ascii=False))
finally:
    pythoncom.CoUninitialize()
