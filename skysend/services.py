from datetime import datetime, date, timedelta
from django.utils import timezone
import zoneinfo
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import send_mail

from skysend.models import MailingSettings, MailingStatus
tz = zoneinfo.ZoneInfo(settings.TIME_ZONE)

def cron_send_mail():
    """Ядро обработки автоматической отправки писем по заданию crontab"""
    emails = []
    body_subjects = {}
    datatime_today = datetime.utcnow().replace(tzinfo=timezone.utc)
    send_mail_is_active = MailingSettings.objects.filter(is_active=True)
    for send_mail_obj in send_mail_is_active:
        print(f'{send_mail_obj} {datatime_today}')
        if send_mail_obj.status_mailing in ['created', 'edited']:
            send_mail_obj.status_mailing = 'running'
            send_mail_obj.save()
        if (datatime_today - timedelta(minutes=2)) < send_mail_obj.mailing_date_next < datatime_today:
            emails = []
            body_subjects = {}
            for mailingclient in send_mail_obj.mailingclient_set.all():
                emails.append(mailingclient.sending_email)
            for mailingmessage in send_mail_obj.mailingmessage_set.all():
                body_subjects[mailingmessage.email_subject] = mailingmessage.email_body
            for email in emails:
                for subject, body in body_subjects.items():
                    try:
                        send_mail(
                            subject=subject,
                            message=body,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[email]
                        )
                        MailingStatus.objects.create(
                            mailing_settings=send_mail_obj,
                            data_time_status=datetime.now(),
                            attempted_status=True,
                            mail_server_response=f'{email}:[{subject}][{body}]'
                        )
                        print(f'{email}:[{subject}][{body}]')
                    except Exception as send_error:
                        MailingStatus.objects.create(
                            mailing_settings=send_mail_obj,
                            data_time_status=datetime.now(),
                            attempted_status=False,
                            mail_server_response=f'{email}:[{subject}][{body}] {str(send_error)}'
                        )
                        print(f'{email}:[{subject}][{body}] {str(send_error)}')
            mailing_date_next = datetime_send_next(
                begin_date=send_mail_obj.begin_date,
                end_date=send_mail_obj.end_date,
                time=send_mail_obj.sending_time,
                frequence=send_mail_obj.intervals
            )
            if send_mail_obj.mailing_date_next == mailing_date_next:
                send_mail_obj.is_active = False
                send_mail_obj.status_mailing = 'completed'
                send_mail_obj.save()
            else:
                send_mail_obj.mailing_date_next = mailing_date_next
                send_mail_obj.save()
            emails = []
            body_subjects = {}


def one_send_mail(mailing_settings):
    """Отправка письма при создании рассылки если поля begin_date и sending_time были указаны в прошлом"""
    emails = []
    body_subjects = {}
    for mailingclient in mailing_settings.mailingclient_set.all():
        emails.append(mailingclient.sending_email)
    for mailingmessage in mailing_settings.mailingmessage_set.all():
        body_subjects[mailingmessage.email_subject] = mailingmessage.email_body
    for email in emails:
        for subject, body in body_subjects.items():
            try:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email]
                )
                MailingStatus.objects.create(
                    mailing_settings=mailing_settings,
                    data_time_status=datetime.now(),
                    attempted_status=True,
                    mail_server_response=f'{email}:[{subject}][{body}]'
                )
            except Exception as send_error:
                MailingStatus.objects.create(
                    mailing_settings=mailing_settings,
                    data_time_status=datetime.now(),
                    attempted_status=False,
                    mail_server_response=f'{email}:[{subject}][{body}] {str(send_error)}'
                )


def datetime_send_next(begin_date, end_date, time, frequence):
    """Формирование даты следующей отправки для поля MailingSettings.mailing_date_next """
    begin_datetime_send = datetime.combine(begin_date, time)
    end_datetime_send = datetime.combine(end_date, time)
    if frequence == 'daily':
        next_datetime_send = datetime.combine(begin_date, time) + timedelta(days=1)
        while True:
            if next_datetime_send < datetime.today():
                next_datetime_send = next_datetime_send + timedelta(days=1)
            else:
                break
        if begin_datetime_send > datetime.today():
            return begin_datetime_send.replace(tzinfo=tz).astimezone(tz=timezone.utc)
        if next_datetime_send < end_datetime_send:
            return next_datetime_send.replace(tzinfo=tz).astimezone(tz=timezone.utc)
        else:
            next_datetime_send = next_datetime_send - timedelta(days=1)
            return next_datetime_send.replace(tzinfo=tz).astimezone(tz=timezone.utc)
    elif frequence == 'weekly':
        next_datetime_send = datetime.combine(begin_date, time) + timedelta(weeks=1)
        while True:
            if next_datetime_send < datetime.today():
                next_datetime_send = next_datetime_send + timedelta(weeks=1)
            else:
                break
        if begin_datetime_send > datetime.today():
            return begin_datetime_send.replace(tzinfo=tz).astimezone(tz=timezone.utc)
        if next_datetime_send < end_datetime_send:
            return next_datetime_send.replace(tzinfo=tz).astimezone(tz=timezone.utc)
        else:
            next_datetime_send = next_datetime_send - timedelta(weeks=1)
            return next_datetime_send.replace(tzinfo=tz).astimezone(tz=timezone.utc)
    elif frequence == 'monthly':
        next_datetime_send = datetime.combine(begin_date, time) + relativedelta(months=+1)
        while True:
            if next_datetime_send < datetime.today():
                next_datetime_send = next_datetime_send + relativedelta(months=+1)
            else:
                break
        if begin_datetime_send > datetime.today():
            return begin_datetime_send.replace(tzinfo=tz).astimezone(tz=timezone.utc)
        if next_datetime_send < end_datetime_send:
            return next_datetime_send.replace(tzinfo=tz).astimezone(tz=timezone.utc)
        else:
            next_datetime_send = next_datetime_send - relativedelta(months=+1)
            return next_datetime_send.replace(tzinfo=tz).astimezone(tz=timezone.utc)
