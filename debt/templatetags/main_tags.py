from datetime import datetime , timedelta
from django import template
import jalali_date


register = template.Library()



@register.filter(name='shamsi')
def shamsi(value):
	date = jalali_date.date2jalali(value)
	return date

@register.filter(name='month')
def month(value):
	date = jalali_date.date2jalali(value)
	month = None
	if date.month == 1:
		month = 'فروردین'
	elif date.month == 2:
		month = 'اردیبهشت'
	elif date.month == 3:
		month = 'خرداد'
	elif date.month == 4:
		month = 'تیر'
	elif date.month == 5:
		month = 'مرداد'
	elif date.month == 6:
		month = 'شهریور'
	elif date.month == 7:
		month = 'مهر'
	elif date.month == 8:
		month = 'آبان'
	elif date.month == 9:
		month = 'آذر'
	elif date.month == 10:
		month = 'دی'
	elif date.month == 11:
		month = 'بهمن'
	elif date.month == 12:
		month = 'اسفند'

	return month


@register.filter(name='day')
def day(value):
	date = jalali_date.date2jalali(value)
	day = date.day

	return day


@register.filter(name='year')
def year(value):
	date = jalali_date.date2jalali(value)
	year = date.year

	return year


@register.filter(name='remaining')
def remaining(value):
	date = value
	now = datetime.now()
	# date = date.replace(tzinfo=None)
	one_hour = date + timedelta(hours=1)
	some_hour = date + timedelta(hours=7)
	two_days = date + timedelta(days=2)
	one_day = date + timedelta(days=1)
	some_day = date + timedelta(days=4)
	one_week = date + timedelta(weeks=1)
	two_weeks =date + timedelta(weeks=2)
	one_month = date + timedelta(days=30)
	two_month = date + timedelta(days=60)
	some_month = date + timedelta(days=210)
	one_year = date + timedelta(days=356)
	two_years = date + timedelta(days=730)
	message = ''

	if now < one_hour:
		message = 'لحظاتی پیش'
	elif now < some_hour:
		message = 'ساعاتی پیش'
	elif now < one_day :
		message = 'امروز'
	elif now < two_days	:
		message = 'دیروز'
	elif now < some_day:
		message = 'چند روز پیش'
	elif now < one_week:
		message = 'هفته جاری'
	elif now < two_weeks:
		message = 'هفته پیش'
	elif now < one_month:
		message = 'چند هفته پیش'
	elif now < two_month :
		message = 'ماه پیش'
	elif now < some_month :
		message = 'چند ماه پیش'
	elif now < one_year:
		message = 'امسال'
	elif now < two_years:
		message = 'سال پیش'
	else:
		message = 'چند سال پیش'

	return message




