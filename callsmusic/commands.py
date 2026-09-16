# Persian command specification for callsmusic
# This file defines Persian command aliases, responses, buttons, and helper parsers.
# It is intentionally content-only and contains no credentials.

PLAYER_BUTTONS = {
    'play': '▶️ پخش',
    'pause': '⏸ مکث',
    'resume': '▶️ ادامه',
    'next': '⏭ بعدی',
    'stop': '⏹ اتمام',
    'queue': '📋 صف',
    'support': '👤 پشتیبان',
}

PLAYBACK_SPEEDS = {
    '0.5': '0.5x',
    '1.0': '1x',
    '1.5': '1.5x',
    '2.0': '2x',
}


# Persian responses (keep existing responses from project intact if any)
RESPONSES = {
    'processing': '<b>🔄 در حال پردازش...</b>',
    'playing': '<b>▶️ در حال پخش...</b>',
    'queued': '<b>#️⃣ در صف شماره {position}</b>',
    'nothing_playing': '<b>❌ چیزی پخش نمی شود</b>',
    'paused': '<b>⏸ متوقف شد</b>',
    'resumed': '<b>▶️ ادامه داده شد</b>',
}


def parse_seek_command(text: str):
    # parse جلو N or عقب N (N seconds)
    parts = text.strip().split()
    if not parts:
        return None
    cmd = parts[0]
    if len(parts) == 1:
        return None
    try:
        n = int(parts[1])
    except Exception:
        return None
    if n < 1 or n > 100:
        return None
    if cmd in ('جلو', '/جلو'):
        return ('forward', n)
    if cmd in ('عقب', '/عقب'):
        return ('backward', n)
    return None


def parse_charge_command(text: str):
    # شارژ N where N in [30,60,90,180,365]
    parts = text.strip().split()
    if len(parts) < 2:
        return None
    try:
        n = int(parts[1])
    except Exception:
        return None
    if n not in (30, 60, 90, 180, 365):
        return None
    mapping = {30: '1 ماه', 60: '2 ماه', 90: '3 ماه', 180: '6 ماه', 365: '1 سال'}
    return (n, mapping[n])


def parse_call_title(text: str):
    # عنوان کال <text>
    parts = text.split(None, 1)
    if len(parts) < 2:
        return None
    return parts[1].strip()


def music_message(track):
    # Minimal formatter for current track info
    return f"<b>آهنگ:</b> {track.get('title', 'Unknown')}\n<b>ارسال کننده:</b> {track.get('by', 'Unknown')}"


def user_info_text(user):
    return f"<b>آیدی:</b> {user.id}\n<b>نام:</b> {user.first_name}"


def charge_text(days, label):
    return f"<b>شارژ شد:</b> {label} ({days} روز)"


def configuration_text(config):
    return '<b>تنظیمات فعلی:</b>\n' + '\n'.join(f"{k}: {v}" for k, v in config.items())


# COMMAND mapping: map Persian and English command names to handler keys used by filters
# The handlers in the project are registered using helpers.filters.command('play') etc.
# We will provide aliases so that command('play') will match Persian commands via
# import and usage in helpers.filters if needed.

COMMAND_ALIASES = {
    # play mapping
    'play': ['play', 'پخش', '/پخش'],
    'pause': ['pause', 'مکث', '/مکث'],
    'resume': ['resume', 'ادامه', '/ادامه'],
    'stop': ['stop', 'اتمام', '/اتمام'],
    'skip': ['skip', 'بعدی', '/بعدی'],
    'previous': ['previous', 'قبلی', '/قبلی'],
    'forward': ['جلو', '/جلو'],
    'backward': ['عقب', '/عقب'],
    'speed': ['سرعت', '/سرعت'],

    # queue/track/owner
    'queue': ['صف', '/صف'],
    'current': ['آهنگ', '/آهنگ'],
    'owner': ['مالک', '/مالک'],

    # call control
    'start_call': ['شروع کال', '/شروع کال'],
    'end_call': ['پایان کال', '/پایان کال'],
    'call_comment_on': ['کامنت کال فعال', '/کامنت کال فعال'],
    'call_comment_off': ['کامنت کال غیر فعال', '/کامنت کال غیر فعال'],
    'call_title': ['عنوان کال', '/عنوان کال'],

    # subscription/admin
    'charge': ['شارژ', '/شارژ'],
    'force_sub': ['عضویت اجباری', '/عضویت اجباری'],
    'config': ['پیکربندی', '/پیکربندی'],
    'player_manager': ['مدیر پلیر', '/مدیر پلیر'],
    'promote_music': ['ترفـیع موزیک', '/ترفـیع موزیک', 'ترفیع موزیک', '/ترفیع موزیک'],
    'promote_assistant': ['ارتقا معاون پلیر', '/ارتقا معاون پلیر'],
    'id': ['آیدی', '/آیدی'],
    'always_online': ['همیشه آنلاین', '/همیشه آنلاین'],
    'do_not_disturb': ['مزاحمت نکن', '/مزاحمت نکن'],
}
