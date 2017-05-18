from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import TemporaryInfo, PermanentlyInfo, CustomerInfo, NoncreditworthyInfo, RegisteredRecords, DebtDocument, \
    JobCategory, Union, State, City, Statistics
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from random import randint
import smtplib
from datetime import datetime, timedelta, date
import khayyam
import requests
from django.core.mail import send_mail

small_alphabet_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z']
capital_alphabet_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                         'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
acount_upgrade = True
error_message = 'مقادیر به درستی وارد نشده اند، و یا مشکلی در انجام عملیات' + '\n' + 'پیش آمده است. لطفا دوباره تلاش کنید و در صورت مشاهده' + '\n' + 'این پیغام با مدیریت تماس حاصل فرمایید'
error_message2 = 'مقادیر به درستی وارد نشده اند، و یا مشکلی در ثبت نام' + '\n' + 'پیش آمده است. لطفا دوباره تلاش کنید و در صورت مشاهده' + '\n' + 'این پیغام با مدیریت تماس حاصل فرمایید'


def create_secure_link_30(alphabet_list_1, alphabet_list_2):
    return str(randint(0, 9)) + alphabet_list_1[randint(0, 23)] + \
           str(randint(0, 9)) + alphabet_list_2[randint(0, 23)] + str(randint(0, 9)) + alphabet_list_1[randint(0, 23)] \
           + str(randint(0, 9)) + alphabet_list_2[randint(0, 23)] + str(randint(0, 9)) + alphabet_list_1[randint(0, 23)] \
           + str(randint(0, 9)) + alphabet_list_2[randint(0, 23)] + \
           str(randint(0, 9)) + alphabet_list_1[randint(0, 23)] + str(randint(0, 9)) + alphabet_list_2[randint(0, 23)] \
           + str(randint(0, 9)) + alphabet_list_1[randint(0, 23)] + str(randint(0, 9)) + alphabet_list_2[randint(0, 23)] \
           + str(randint(0, 9)) + alphabet_list_1[randint(0, 23)] + \
           str(randint(0, 9)) + alphabet_list_2[randint(0, 23)] + str(randint(0, 9)) + alphabet_list_1[randint(0, 23)] \
           + str(randint(0, 9)) + alphabet_list_2[randint(0, 23)] + str(randint(0, 9)) + alphabet_list_1[randint(0, 23)]


def create_secure_link_20(alphabet_list_1, alphabet_list_2):
    return str(randint(0, 9)) + alphabet_list_1[randint(0, 23)] + \
           str(randint(0, 9)) + alphabet_list_2[randint(0, 23)] + str(randint(0, 9)) + alphabet_list_1[randint(0, 23)] \
           + str(randint(0, 9)) + alphabet_list_2[randint(0, 23)] + str(randint(0, 9)) + alphabet_list_1[randint(0, 23)] \
           + str(randint(0, 9)) + alphabet_list_2[randint(0, 23)] + \
           str(randint(0, 9)) + alphabet_list_1[randint(0, 23)] + str(randint(0, 9)) + alphabet_list_2[randint(0, 23)] \
           + str(randint(0, 9)) + alphabet_list_1[randint(0, 23)] + str(randint(0, 9)) + alphabet_list_2[randint(0, 23)] \


def create_secure_link_4():
    return str(randint(1, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))


def send_email(admin, pwd, user, message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(admin, pwd)
        server.sendmail(admin, user, message.encode('UTF-8'))
        server.close()
        return True
    except:
        return False


def word_validator(wrd):
    word = str(wrd)
    new_word = ''
    for letter in word:
        if letter != ' ':
            new_word = new_word + letter.lower()
        elif letter == '@' or letter == '.':
            new_word = new_word + letter
        else:
            pass
    return new_word


def round_to_five(num):
    remaining = num % 5
    if remaining in range(0, 3):
        result = num - remaining
    else:
        result = num + (5 - remaining)
    return result


def scrn_name_validator (name):
    name_list = []
    index_list = set({})
    first_name1 = ''
    last_name1 = ''
    first_name_list = []
    last_name_list = []
    first_name = ''
    last_name = ''
    for letter in name:
        name_list.append(letter)
    for num in range(len(name_list)):
        if num > 0 and num < (len(name_list)-1):
            if name_list[num] == ' ' and name_list[num+1] == ' ' and name_list[num-1] == ' ':
                index_list.add(num)
            elif name_list[num] == ' ' and name_list[num+1] == '_':
                index_list.add(num)
            elif name_list[num] == ' ' and name_list[num-1] == '_':
                index_list.add(num)
        else:
            if name_list[num] == ' ':
                index_list.add(num)
    for num in index_list:
        name_list[num] = ''
    for letter in name_list:
        if letter != '':
            if letter != '_':
                first_name1 += letter
                name_list[name_list.index(letter)] = ''
            else:
                break
    for letter in name_list:
        if letter != '' and letter != '_':
            last_name1 += letter
            name_list[(name_list.index(letter))] = ''
    for letter in first_name1:
        first_name_list.append(letter)
    for letter in last_name1:
        last_name_list.append(letter)
    if first_name_list[0] == ' ': first_name_list.pop(0)
    if first_name_list[-1] == ' ': first_name_list.pop(-1)
    if last_name_list[0] == ' ': last_name_list.pop(0)
    if last_name_list[-1] == ' ': last_name_list.pop(-1)
    for letter in first_name_list:
        first_name += letter
    for letter in last_name_list:
        last_name += letter
    return (first_name, last_name)


def gn_name_validator (first_name1, last_name1):    #Get Name name validator
    first_name_list = []
    first_name_index_list = set({})
    last_name_list = []
    last_name_index_list = set({})
    first_name = ''
    last_name = ''
    for letter in first_name1:
        first_name_list.append(letter)
    for num in range(len(first_name_list)):
        if first_name_list[num] == ' ':
            first_name_index_list.add(num)
        else:
            break
    for num in range(len(first_name_list)-1, -1, -1):
        if first_name_list[num] == ' ':
            first_name_index_list.add(num)
        else:
            break
    for indexx in first_name_index_list:
        first_name_list[indexx] = ''
    for letter in first_name_list:
        if letter != '':
            first_name += letter
    for letter in last_name1:
        last_name_list.append(letter)
    for num in range(len(last_name_list)):
        if last_name_list[num] == ' ':
            last_name_index_list.add(num)
        else:
            break
    for num in range(len(last_name_list)-1, -1, -1):
        if last_name_list[num] == ' ':
            last_name_index_list.add(num)
        else:
            break
    for indexx in last_name_index_list:
        last_name_list[indexx] = ''
    for letter in last_name_list:
        if letter != '':
            last_name += letter
    return (first_name, last_name)


def send_sms(phone_number, message):
    request = requests.post("http://niksms.com/fa/publicapi/ptpsms",
                            params={'username': '09166661288', 'password': '1234r5678', 'sendernumber': '9830002530000033',
                                    'numbers': str(phone_number), 'sendon': '2016/01/01-00:00', 'sendtype': '1',
                                    'message': message})
    if request.json().get('Status') == 1:
        return request.json()
    else:
        return False


def index(request):
    if request.user.is_authenticated():
        user = PermanentlyInfo.objects.get(username=request.user.username)
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        if user.first_log_in == False:
            user.first_log_in = True
            user.save()
            message = "Subject: راهنمای استفاده از سامانه سجام\nکاربر گرامی\n\nمی توانید از پی دی اف ضمیمه شده به عنوان راهنمای استفاده از سامانه ی سجام استفاده کنید\n\nسیستم جامع استعلام مشتریان = سجام\nآدرس سایت:\nwWw.SamanehEstelam.Org"
#            send_mail('راهنمای استفاده از سامانه سجام', mail_message, 'info@samanehestelam.org',[str(user.email)], fail_silently=False)
            return render(request, 'base_in/base_in.html', {'user': user, 'first_time': 'y'})
        else:
            return render(request, 'base_in/base_in.html', {'user': user})
    else:
        return render(request, 'signupapp/index.html', {})


def signup(request):
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        return render(request, 'signupapp/ok_in.html',
                      {'message': 'کاربر گرامی، شما اجازه ی دسترسی به این صفحه را ندارید', 'from': 'loggedin_signup',
                       'user': user})
    else:
        if request.POST:
            try:
                user = PermanentlyInfo.objects.get(email=request.POST['email'])
                return render(request, 'signupapp/ok_out.html',
                              {'message': 'یک حساب کاربری با این ایمیل ثبت شده است', 'from': 'failed_signup_page'})
            except:
                try:
                    cyear = str(khayyam.JalaliDatetime.now().date())[0:4]  # Current year
                    cbirthday = str(khayyam.JalaliDatetime.now().date()).replace(cyear, str(
                        int(cyear) - 20))  # Custom Birthday
                    cbldd = str(khayyam.JalaliDatetime.now().date()).replace(cyear, str(
                        int(cyear) + 2))  # Custom business license due date
                    user = PermanentlyInfo(
                        first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        phone='0',
                        mobile='0',
                        mobile_is_varified=False,
                        fax='0',
                        id_num='0',
                        job_category='',
                        union='',
                        business_license_num='0',
                        father_name='',
                        state='',
                        city='',
                        address='',
                        brand='',
                        birthday=cbirthday,
                        gender='',
                        signup_date=str(date.today()),
                        business_license_due_date=cbldd,
                        b_name='',
                        b_branch_name='',
                        b_branch_code=0,
                        b_acount_num=0,
                        b_card_num=0,
                        b_sheba_num=0,
                        b_complete=False,
                        b_varified=False,
                        email=word_validator(request.POST['email']),
                        email_is_activated=False,
                        secondary_email='',
                        secondary_email_is_activated=False,
                        username=word_validator(request.POST['email']),
                        password=request.POST['password'],
                        registered_records_num=0,
                        about='',
                        certified=False,
                        is_complete=False,
                        info_complete=False,
                        last_edit=cbldd,
                        last_sync=cbldd,
                        user_certification_link=create_secure_link_30(small_alphabet_list, small_alphabet_list),
                        user_email_activation_link=create_secure_link_30(small_alphabet_list, capital_alphabet_list),
                        user_secondary_email_activation_link=create_secure_link_30(small_alphabet_list,
                                                                                   capital_alphabet_list),
                        user_phone_varification_number=create_secure_link_4(),
                        user_pass_reset_link=create_secure_link_30(capital_alphabet_list, small_alphabet_list),
                        day_search=0,
                        last_search_date=str(khayyam.JalaliDatetime.now().date()),
                        complete_percentage=0,
                        acount_upgrade_date=str(khayyam.JalaliDatetime.now().date()),
                        gone_bad_records=0,
                        first_log_in=False,
                    )
                    user.save()
                    cheque_dd = user.debtdocument_set.create(name="چک", used_num=0, value="cheque")
                    demand_note_dd = user.debtdocument_set.create(name="سفته", used_num=0, value="demand_note")
                    cheque_dd.save()
                    demand_note_dd.save()
                    user1 = User.objects.create_user(user.username, user.email, user.password)
                    user1.is_active = False
                    user1.save()
                    mail_message = "کاربر گرامی\n\nلطفا از لینک زیر برای فعال سازی حساب کاربری خود در سامانه ی سجام استفاده نمایید:\n\nhttp://www.samanehestelam.com/aaa/{}\n\nبا تشکر\nسیستم جامع استعلام مشتریان = سجام\nآدرس سایت:\nwWw.SamanehEstelam.Org".format(str(user.user_email_activation_link))
#                    user_mail_func = send_email('samaneestelam@gmail.com', '0okmnji98U', [str(user.email)], message)
                    send_mail('تایید اکانت سجام', mail_message, 'info@samanehestelam.org',
                              [str(user.email)], fail_silently=False)
                    return render(request, 'signupapp/ok_out.html', {
                        'message': 'به سامانه جامع استعلام خوش حسابی مشتریان - سجام - خوش آمدید.' + '\n' + 'برای فعال کردن حساب خود از طریق ایمیل ارسال شده اقدام کنید',
                        'from': 'signup_page'})
                except:
                    return render(request, 'signupapp/ok_out.html',
                                  {'message': error_message2, 'from': 'bad_entry_signup'})
        else:
            job_categories = JobCategory.objects.all()
            unions = Union.objects.all()
            return render(request, 'signupapp/signup_page.html',
                          {'signupp': 'YES', 'jobcategories': job_categories, 'unions': unions})


def certify_a_user(request, user_cl):  # USELESS
    if request.user.is_authenticated():
        try:
            user = TemporaryInfo.objects.get(certify_link=user_cl)
            certified_user = PermanentlyInfo(
                first_name=user.first_name,
                last_name=user.last_name,
                phone=user.phone,
                mobile=user.mobile,
                mobile_is_varified=False,
                fax=user.fax,
                id_num=user.id_num,
                job_category=user.job_category,
                union=user.union,
                business_license_num=user.business_license_num,
                father_name=user.father_name,
                state=user.state,
                city=user.city,
                address=user.address,
                brand=user.brand,
                birthday=user.birthday,
                gender=user.gender,
                signup_date=user.signup_date,
                business_license_due_date=user.business_license_due_date,
                email=user.email,
                secondary_email='',
                username=user.username,
                password=user.password,
                registered_records_num=user.registered_records_num,
                about=user.about,
                certified=True,

            )
            certified_user.save()
            user1 = User.objects.create_user(certified_user.username, certified_user.email, certified_user.password)
            user1.is_active = False
            user1.save()
            user.delete()
            message = "Subject: تایید اکانت در سجام\nکاربر گرامی\n\nلطفا از لینک زیر برای فعال سازی حساب کاربری خود در سامانه ی سجام استفاده نمایید:\n\nhttp://www.samanehestelam.com/aaa/{}\n\nبا تشکر\nسیستم جامع استعلام مشتریان = سجام\nآدرس سایت:\nwWw.SamanehEstelam.Com".format(str(certified_user.user_activation_link))
            user_mail_func = send_email('samaneestelam@gmail.com', '0okmnji98U', [str(certified_user.email)], message)
#            send_mail('تایید ایمیل دوم در سامانه سجام', mail_message, 'info@samanehestelam.org',[str(user.secondary_email)], fail_silently=False)
            if user_mail_func == False:
                return render(request, 'signupapp/ok_out.html',
                              {'message': 'کاربر تایید شده اما ایمیل حاوی اطلاعات برای ایشان ارسال نشد',
                               'from': 'nomail_certify_a_user'})
            else:
                return render(request, 'signupapp/ok_out.html',
                              {'message': 'کاربر تایید شده و ایمیل حاوی اطلاعات برای ایشان ارسال شد',
                               'from': 'certify_a_user'})
        except:
            return render(request, 'signupapp/ok_out.html',
                          {'message': 'کاربر مورد نظر موجود نمی باشد', 'from': 'failed_certfiy_a_user'})
    else:
        return render(request, 'signupapp/ok_in.html',
                      {'message': 'کاربر گرامی، شما اجازه ی دسترسی به این صفحه را ندارید', 'from': 'loggedin_signup'})


def activate_a_user(request, user_ual):  # USELESS
    if request.user.is_authenticated():
        try:
            user = PermanentlyInfo.objects.get(user_activation_link=user_ual)
            user1 = authenticate(username=str(user.username), password=str(user.password))
            user1.is_active = True
            user.user_activation_link = ''
            user.save()
            user1.save()
            return render(request, 'signupapp/ok_out.html',
                          {'message': 'به استعلام خوش آمدید', 'from': 'activate_a_user'})
        except:
            return render(request, 'signupapp/ok_out.html',
                          {'message': 'کاربر مورد نظر موجود نمی باشد و یا اطلاعات ایشان هنوز تایید نشده است',
                           'from': 'failed_activate_a_user'})
    else:
        return render(request, 'signupapp/ok_in.html',
                      {'message': 'کاربر گرامی، شما اجازه ی دسترسی به این صفحه را ندارید', 'from': 'loggedin_signup'})


def activate_an_email(request, user_eal):
    try:
        user = PermanentlyInfo.objects.get(user_email_activation_link=user_eal)
        user.user_email_activation_link = ''
        user.email_is_activated = True
        user.save()
        user1 = authenticate(username=user.username, password=user.password)
        user1.is_active = True
        user1.save()
        return render(request, 'signupapp/ok_out.html',
                          {'message': 'ایمیل و حساب کاربری با موفقیت فعال شد', 'from': 'activate_an_acount'})
    except:
        try:
            user = PermanentlyInfo.objects.get(user_secondary_email_activation_link=user_eal)
            user.user_secondary_email_activation_link = ''
            user.secondary_email_is_activated = True
            user.save()
            return render(request, 'signupapp/ok_out.html',
                              {'message': 'ایمیل دوم {} با موفقیت فعال شد'.format(str(user.secondary_email), ),
                               'from': 'activate_an_email'})
        except:
            return render(request, 'signupapp/ok_out.html',
                          {'message': 'آدرس اشتباه می باشد', 'from': 'failed_activate_a_user'})


def dologin(request):
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        return HttpResponseRedirect('/')
    else:
        if request.POST:
            username = word_validator(request.POST['username'])
            password = request.POST['password']
            user1 = authenticate(username=username, password=password)
            if user1 is None:
                try:
                    username1 = PermanentlyInfo.objects.get(email=username).username
                    user1 = authenticate(username=username1, password=password)
                    if user1 is not None:
                        if user1.is_active == 1:
                            login(request, user1)
                            request.session['last_touch'] = khayyam.JalaliDatetime.now()
                            user = PermanentlyInfo.objects.get(username=username1)
                            if user.certified == 0:
                                complete_percentage1 = 0
                                texts = [user.first_name, user.last_name, user.father_name, user.address, user.brand,
                                         user.union, user.job_category, user.state, user.city, user.gender, user.b_name,
                                         user.b_branch_name, user.email, user.secondary_email, user.b_sheba_num,]
                                nums = [user.b_branch_code, user.b_card_num, user.b_acount_num,
                                        user.id_num, user.business_license_num, user.fax, user.phone, user.mobile]
                                bools = [user.mobile_is_varified, user.email_is_activated,
                                         user.secondary_email_is_activated, user.b_complete, user.b_varified]
                                for text in texts:
                                    if text != '':
                                        complete_percentage1 += 3
                                for num in nums:
                                    if num != 0:
                                        complete_percentage1 += 3
                                for bool in bools:
                                    if bool != 0:
                                        complete_percentage1 += 3
                                complete_percentage = round_to_five(complete_percentage1)
                                user.complete_percentage = complete_percentage
                                if nums[0] != 0 and nums[1] != 0 and nums[2] != 0 and texts[10] != '' and texts[11] != '' and texts[14] != '':
                                    user.b_complete = True
                                if texts[0] != '' and texts[1] != '' and texts[2] != '' and texts[3] != '' and texts[4] != '' and texts[5] != '' and texts[6] != '' and texts[7] != '' and texts[8] != '' and texts[9] != '' and texts[12] != '' and texts[13] != '' and nums[3] != 0 and nums[4] != 0 and nums[5] != 0 and nums[6] != 0 and nums[7] != 0 and bools[0] != 0 and bools[1] != 0 and bools[10] != 0:
                                    user.info_complete = True
                                if user.b_complete == 1 and user.info_complete == 1:
                                    user.is_complete = True
                            if str(khayyam.JalaliDatetime.now().date()) != user.last_search_date:
                                user.day_search = 0
                            rrs = user.registeredrecords_set.all()  # Registered Records
                            nc_records = [record for record in rrs if record.debt_cleared == 0]  # Not Cleared
                            for record in nc_records:
                                if str(khayyam.JalaliDatetime.now().date()) > str(record.debt_due_date):
                                    record.gone_bad = True
                                    customer = CustomerInfo.objects.get(id=record.customer_id)
                                    customer.registered_late_records_num += 1
                                    customer.save()
                                else:
                                    record.gone_bad = False
                                    customer = CustomerInfo.objects.get(id=record.customer_id)
                                    customer.registered_late_records_num -= 1
                                    customer.save()
                                record.save()
                            gb_records = [record for record in rrs if record.debt_cleared == 0 and record.gone_bad == 1]
                            user.gone_bad_records = len(gb_records)
                            request.session['earlierFill'] = False
                            if user.acount_type != 'base' and (
                                khayyam.JalaliDatetime.now().date() - user.acount_upgrade_date()) >= 31:
                                ab_message = "کاربر گرامی\n\nبه دلیل اتمام مدت اعتبار، نوع حساب شما در سامانه ی سجام به حالت عادی تغییر کرد.\n\nبا تشکر\nسیستم جامع استعلام مشتریان = سجام\nآدرس سایت:\nwWw.SamanehEstelam.Org"
#                                ab_mail = send_email('samaneestelam@gmail.com', '0okmnji98U', [str(user.email)], ab_message)
                                send_mail('اتمام اعتبار حساب ویژه سجام', ab_message, 'info@samanehestelam.org',
                                          [str(user.email)], fail_silently=False)
                                user.acount_type = 'base'
                            user.save()
                            request.session['earlierFill'] = False
                            request.session['racEarlierFill'] = False
                            request.session['ecEarlierFill'] = False
                            return HttpResponseRedirect('/')
                        else:
                            return render(request, 'signupapp/ok_out.html',
                                          {'message': 'حساب کاربری مورد نظر هنوز فعال نشده است',
                                           'from': 'not_active_login'})
                    else:
                        return render(request, 'signupapp/login_page.html', {'from': 'wrong_login'})
                except:
                    return render(request, 'signupapp/login_page.html', {'from': 'wrong_login'})
            else:
                if user1.is_active == 1:
                    login(request, user1)
                    request.session['last_touch'] = khayyam.JalaliDatetime.now()
                    user = PermanentlyInfo.objects.get(username=word_validator(request.POST['username']))
                    if user.certified == 0:
                        complete_percentage1 = 0
                        texts = [user.first_name, user.last_name, user.father_name, user.address, user.brand,
                                 user.union, user.job_category, user.state, user.city, user.gender, user.b_name,
                                 user.b_branch_name, user.email, user.secondary_email, user.b_sheba_num, ]
                        nums = [user.b_branch_code, user.b_card_num, user.b_acount_num, user.id_num,
                                user.business_license_num, user.fax, user.phone, user.mobile]
                        bools = [user.mobile_is_varified, user.email_is_activated, user.secondary_email_is_activated,
                                 user.b_complete, user.b_varified]
                        for text in texts:
                            if text != '':
                                complete_percentage1 += 3
                        for num in nums:
                            if num != 0:
                                complete_percentage1 += 3
                        for bool in bools:
                            if bool != 0:
                                complete_percentage1 += 3
                        complete_percentage = round_to_five(complete_percentage1)
                        user.complete_percentage = complete_percentage
                        if nums[0] != 0 and nums[1] != 0 and nums[2] != 0 and texts[10] != '' and texts[11] != '' and \
                                        texts[14] != '':
                            user.b_complete = True
                        if texts[0] != '' and texts[1] != '' and texts[2] != '' and texts[3] != '' and texts[
                            4] != '' and texts[5] != '' and texts[6] != '' and texts[7] != '' and texts[8] != '' and \
                                        texts[9] != '' and texts[12] != '' and texts[13] != '' and nums[3] != 0 and \
                                        nums[4] != 0 and nums[5] != 0 and nums[6] != 0 and nums[7] != 0 and bools[
                            0] != 0 and bools[1] != 0 and bools[10] != 0:
                            user.info_complete = True
                        if user.b_complete == 1 and user.info_complete == 1:
                            user.is_complete = True
                    if str(khayyam.JalaliDatetime.now().date()) != user.last_search_date:
                        user.day_search = 0
                    rrs = user.registeredrecords_set.all()  # Registered Records
                    nc_records = [record for record in rrs if record.debt_cleared == 0]  # Not Cleared
                    for record in nc_records:
                        if str(khayyam.JalaliDatetime.now().date()) > str(record.debt_due_date):
                            record.gone_bad = True
                            customer = CustomerInfo.objects.get(id=record.customer_id)
                            customer.registered_late_records_num += 1
                            customer.save()
                        else:
                            record.gone_bad = False
                            customer = CustomerInfo.objects.get(id=record.customer_id)
                            customer.registered_late_records_num -= 1
                            customer.save()
                        record.save()
                    gb_records = [record for record in rrs if record.debt_cleared == 0 and record.gone_bad == 1]
                    user.gone_bad_records = len(gb_records)
                    request.session['earlierFill'] = False
                    if user.acount_type != 'base' and (
                        khayyam.JalaliDatetime.now().date() - khayyam.JalaliDatetime.date(user.acount_upgrade_date)).days >= 31:
                        ab_message = "کاربر گرامی\n\nبه دلیل اتمام مدت اعتبار، نوع حساب شما در سامانه ی سجام به حالت عادی تغییر کرد.\n\nبا تشکر\nسیستم جامع استعلام مشتریان = سجام\nآدرس سایت:\nwWw.SamanehEstelam.Org"
#                        ab_mail = send_email('samaneestelam@gmail.com', '0okmnji98U', [str(user.email)], ab_message)
                        send_mail('اتمام اعتبار حساب ویژه سجام', ab_message, 'info@samanehestelam.org',
                                  [str(user.email)], fail_silently=False)
                        user.acount_type = 'base'
                    user.save()
                    request.session['earlierFill'] = False
                    request.session['racEarlierFill'] = False
                    request.session['ecEarlierFill'] = False
                    return HttpResponseRedirect('/')
                else:
                    return render(request, 'signupapp/ok_out.html',
                                  {'message': 'حساب کاربری مورد نظر هنوز فعال نشده است', 'from': 'not_active_login'})
        else:
            return render(request, 'signupapp/login_page.html', {'from': 'none'})


def dologout(request):
    logout(request)
    return HttpResponseRedirect('/')


def forgotpass(request):
    if not request.user.is_authenticated():
        if request.POST:
            try:
                user = PermanentlyInfo.objects.get(email=request.POST['user_email'])
                mail_message = "کاربر گرامی\n\nلطفا از لینک زیر برای تغییر رمز عبور خود استفاده نمایید:\n\nhttp://www.samanehestelam.org/newpass/{}\n\nبا تشکر\nسیستم جامع استعلام مشتریان = سجام\nآدرس سایت:\nwWw.SamanehEstelam.Org".format(str(user.user_pass_reset_link))
#                user_mail_func = send_email('samaneestelam@gmail.com', '0okmnji98U', [str(user.email), ], message)
                send_mail('تغییر رمز سجام', mail_message, 'info@samanehestelam.org',
                          [str(user.email)], fail_silently=False)
                return render(request, 'signupapp/ok_out.html',
                                  {'message': 'ایمیل تغییر کلمه عبور به {} فرستاده شد'.format(str(user.email), ),
                                   'from': 'forgot_pass'})
            except:
                return render(request, 'signupapp/ok_out.html',
                              {'message': 'ایمیل {} در سامانه ثبت نشده است'.format(str(request.POST['user_email'])),
                               'from': 'wrong_mail_forgotten_pass'})
        else:
            return render(request, 'signupapp/get_email_forgotten_pass.html', {})
    else:
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        return HttpResponseRedirect('/')


def newpass(request, user_prl):
    try:
        user = PermanentlyInfo.objects.get(user_pass_reset_link=user_prl)
        user1 = authenticate(username=user.username, password=user.password)
        login(request, user1)
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        request.session['earlierFill'] = False
        if user.certified == 0:
            complete_percentage = 0
            texts = [user.first_name, user.last_name, user.father_name, user.address, user.brand, user.union,
                     user.job_category, user.state, user.city, user.gender, user.b_name, user.b_branch_name, user.email,
                     user.secondary_email, user.b_sheba_num, ]
            nums = [user.b_branch_code, user.b_card_num, user.b_acount_num, user.id_num,
                    user.business_license_num, user.fax, user.phone, user.mobile]
            bools = [user.mobile_is_varified, user.email_is_activated, user.secondary_email_is_activated,
                     user.b_complete, user.b_varified]
            for text in texts:
                if text != '':
                    complete_percentage += 3
            for num in nums:
                if num != 0:
                    complete_percentage += 3
            for bool in bools:
                if bool != 0:
                    complete_percentage += 3
            complete_percentage = round_to_five(complete_percentage)
            user.complete_percentage = complete_percentage
            if nums[0] != 0 and nums[1] != 0 and nums[2] != 0 and texts[10] != '' and texts[11] != '' and \
                            texts[14] != '':
                user.b_complete = True
            if texts[0] != '' and texts[1] != '' and texts[2] != '' and texts[3] != '' and texts[4] != '' and texts[
                5] != '' and texts[6] != '' and texts[7] != '' and texts[8] != '' and texts[9] != '' and texts[
                12] != '' and texts[13] != '' and nums[3] != 0 and nums[4] != 0 and nums[5] != 0 and nums[6] != 0 and \
                            nums[7] != 0 and bools[0] != 0 and bools[1] != 0 and bools[10] != 0:
                user.info_complete = True
            if user.b_complete == 1 and user.info_complete == 1:
                user.is_complete = True
        if str(khayyam.JalaliDatetime.now().date()) != str(user.last_search_date):
            user.day_search = 0
        user.save()
        rrs = user.registeredrecords_set.all()  # Registered Records
        nc_records = [record for record in rrs if record.debt_cleared == 0]  # Not Cleared
        for record in nc_records:
            if str(khayyam.JalaliDatetime.now().date()) > str(record.debt_due_date):
                record.gone_bad = True
                customer = CustomerInfo.objects.get(id=record.customer_id)
                customer.registered_late_records_num += 1
                customer.save()
            else:
                record.gone_bad = False
                customer = CustomerInfo.objects.get(id=record.customer_id)
                customer.registered_late_records_num -= 1
                customer.save()
            record.save()
            if user.acount_type != 'base' and (khayyam.JalaliDatetime.now().date() - khayyam.JalaliDatetime.date(user.acount_upgrade_date)).days >= 31:
                ab_message = "کاربر گرامی\n\nبه دلیل اتمام مدت اعتبار، نوع حساب شما در سامانه ی سجام به حالت عادی تغییر کرد.\n\nبا تشکر\nسیستم جامع استعلام مشتریان = سجام\nآدرس سایت:\nwWw.SamanehEstelam.Org"
#                ab_mail = send_email('samaneestelam@gmail.com', '0okmnji98U', [str(user.email)], ab_message)
                send_mail('اتمام اعتبار حساب ویژه سجام', ab_message, 'info@samanehestelam.org',
                          [str(user.email)], fail_silently=False)
                user.acount_type = 'base'
                user.save()
        if request.POST:
            user.password = request.POST['password']
            user.user_pass_reset_link = create_secure_link_30(capital_alphabet_list, small_alphabet_list)
            user1 = User.objects.get(username=user.username)
            user1.set_password(request.POST['password'])
            user.save()
            user1.save()
            return render(request, 'signupapp/ok_in.html',
                          {'message': 'رمز عبور جدید با موفقیت ثبت شد', 'from': 'newpass', 'user': user})
        else:
            return render(request, 'signupapp/new_pass_page.html', {'code': user_prl, 'user': user})
    except:
        return render(request, 'signupapp/ok_out.html',
                      {'message': 'آدرس مورد نظر معتبر نمی باشد', 'from': 'failed_new_pass'})


def gcin(request):  # Get Customer Id Num
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        request.session['from_gcn'] = False
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if request.POST:
            try:
                int(request.POST['customer_id_num'])
                try:
                    customer = CustomerInfo.objects.get(id_num=request.POST['customer_id_num'])
                    return HttpResponseRedirect('/rar/{}/'.format(customer.id, ))
                except:
                    try:
                        tradesman = PermanentlyInfo.objects.get(id_num=request.POST['customer_id_num'])
                        request.session['tradesman'] = tradesman
                        return render(request, 'signupapp/show_found_users.html',
                                      {'users': tradesman, 'user': user, 'from': 'gncin'})
                    except:
                        request.session['new_customer_id_num'] = int(request.POST['customer_id_num'])
                        job_categories = JobCategory.objects.all()
                        states = State.objects.all()
                        cities = City.objects.all()
                        return render(request, 'signupapp/register_a_customer.html',
                                      {'jobcategories': job_categories, 'states': states, 'cities': cities,
                                       'user': user, 'session': request.session})
            except:
                return render(request, 'signupapp/ok_in.html',
                              {'message': error_message, 'from': 'bad_entry_signup', 'user': user})
        else:
            return render(request, 'signupapp/get_customer_id_num_register.html', {'user': user})
    else:
        return HttpResponseRedirect('/dologin/')


def gcn(request):  # Get Customer Name
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        request.session['from_gcn'] = False
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if request.POST:
            nc_first_name1 = request.POST['customer_first_name']
            nc_last_name1 = request.POST['customer_last_name']
            nc_first_name, nc_last_name = gn_name_validator(nc_first_name1, nc_last_name1)
            customer_list1 = [customer for customer in CustomerInfo.objects.all() if
                              customer.first_name == nc_first_name and customer.last_name == nc_last_name]
            customer_ids = {customer.id for customer in customer_list1}
            customer_list = []
            for customer in customer_ids:
                customer1 = CustomerInfo.objects.get(id=customer)
                customer_list.append(customer1)
            if len(customer_list) != 0:
                request.session['first_name'] = nc_first_name
                request.session['last_name'] = nc_last_name
                return render(request, 'signupapp/show_found_users.html',
                              {'users': customer_list, 'user': user, 'from': 'gcn'})
            else:
                request.session['from_gcn'] = True
                request.session['first_name'] = nc_first_name
                request.session['last_name'] = nc_last_name
                return render(request, 'signupapp/ok_in.html', {
                    'message': 'اطلاعات {} در سامانه ی سجام ثبت نشده است'.format(
                        str(nc_first_name) + ' ' + str(nc_last_name), ), 'from': 'empty_gcn', 'user': user})
        else:
            return render(request, 'signupapp/get_customer_id_num_register.html', {'user': user})
    else:
        return HttpResponseRedirect('/dologin/')


def gncin(request):  # Get New Customer Id Num
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if request.POST:
            try:
                int(request.POST['customer_id_num'])
                try:
                    customer = CustomerInfo.objects.get(id_num=request.POST['customer_id_num'])
                    return HttpResponseRedirect('/scri/{}/'.format(request.POST['customer_id_num'], ))
                except:
                    try:
                        tradesman = PermanentlyInfo.objects.get(id_num=request.POST['customer_id_num'])
                        request.session['tradesman'] = tradesman
                        return render(request, 'signupapp/show_found_users.html',
                                      {'users': tradesman, 'user': user, 'from': 'gncin'})
                    except:
                        request.session['new_customer_id_num'] = int(request.POST['customer_id_num'])
                        job_categories = JobCategory.objects.all()
                        states = State.objects.all()
                        cities = City.objects.all()
                        return render(request, 'signupapp/register_a_customer.html',
                                      {'jobcategories': job_categories, 'states': states, 'cities': cities,
                                       'user': user, 'session': request.session})
            except:
                return render(request, 'signupapp/ok_in.html',
                              {'message': error_message, 'from': 'bad_entry_signup', 'user': user})
        else:
            return render(request, 'signupapp/get_new_customer_id_num_register.html', {'user': user})
    else:
        return HttpResponseRedirect('/dologin/')


def gncn(request):  # Get New Customer Name
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if request.POST:
            nc_first_name1 = request.POST['customer_first_name']
            nc_last_name1 = request.POST['customer_last_name']
            nc_first_name, nc_last_name = gn_name_validator(nc_first_name1, nc_last_name1)
            customer_list1 = [customer for customer in CustomerInfo.objects.all() if
                              customer.first_name == nc_first_name and customer.last_name == nc_last_name]
            customer_ids = {customer.id for customer in customer_list1}
            customer_list = []
            for customer in customer_ids:
                customer1 = CustomerInfo.objects.get(id=customer)
                customer_list.append(customer1)
            if len(customer_list) != 0:
                request.session['first_name'] = nc_first_name
                request.session['last_name'] = nc_last_name
                return render(request, 'signupapp/show_found_users.html',
                              {'users': customer_list, 'user': user, 'from': 'gncn'})
            else:
                #                tradesman_list1 = [tradesman for tradesman in PermanentlyInfo.objects.all() if tradesman.first_name == nc_first_name and tradesman.last_name == nc_last_name]
                #                tradesman_ids = {tradesman.id_num for tradesman in tradesman_list1}
                #                tradesman_list = []
                #                for tradesman in tradesman_ids:
                #                    tradesman1 = PermanentlyInfo.objects.get(id_num=tradesman)
                #                    tradesman_list.append(tradesman1)
                #                if len(tradesman_list) != 0:
                #                    request.session['first_name'] = nc_first_name
                #                    request.session['last_name'] = nc_last_name
                #                    return render(request, 'signupapp/show_found_users.html', {'users': customer_list, 'user': user, 'from': 'gncn'})
                request.session['first_name'] = nc_first_name
                request.session['last_name'] = nc_last_name
                states = State.objects.all()
                cities = City.objects.all()
                request.session['racEarlierFill'] = False
                return render(request, 'signupapp/register_a_customer_name.html',
                              {'states': states, 'cities': cities, 'user': user, 'session': request.session})
        else:
            return render(request, 'signupapp/get_new_customer_name_register.html', {'user': user})
    else:
        return HttpResponseRedirect('/dologin/')


def gncift(request):  # Get New Customer Info From Tradesmen
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin/')
    else:
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        if 'tradesman' not in request.session:
            return HttpResponseRedirect('/gncin/')
        else:
            user = PermanentlyInfo.objects.get(username=request.user.username)
            states = State.objects.all()
            cities = City.objects.all()
            return render(request, 'signupapp/register_a_tradesman_customer.html',
                          {'states': states, 'cities': cities, 'user': user, 'session': request.session})


def rac(request):  # Register A Customer
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if request.POST:
            try:
                first_name, last_name = gn_name_validator(request.POST['first_name'], request.POST['last_name'])
                customer = user.customerinfo_set.create(
                    first_name=first_name,
                    last_name=last_name,
                    father_name='',
                    gender=request.POST['gender'],
                    id_num=request.POST['id_num'],
                    state=request.POST['state'],
                    city=request.POST['city'],
                    job=request.POST['job'],
                    about='',
                    relative_id_num=0,
                    relativity='',
                    searched_num=0,
                    registered_records_num=0,
                    registered_late_records_num=0,
                    customer_link=create_secure_link_20(small_alphabet_list, capital_alphabet_list),
                )
                customer.save()
                if request.POST['relative_id_num'] != '':
                    try:
                        int(request.POST['relative_id_num'])
                        customer.relative_id_num = request.POST['relative_id_num']
                    except:
                        pass
                if request.POST['relativity'] != '':
                    customer.relativity = request.POST['relativity']
                if request.POST['father_name'] != '':
                    customer.father_name = request.POST['father_name']
                if request.POST['about'] != '':
                    customer.about = request.POST['about']
                state = State.objects.get(name=customer.state)
                city = state.city_set.get(name=customer.city)
                state.used_num += 1
                city.used_num += 1
                customer.save()
                state.save()
                city.save()
                return render(request, 'signupapp/ok_in.html', {
                    'message': 'اطلاعات {} با موفقیت ثبت شد'.format(customer.first_name + ' ' + customer.last_name, ),
                    'from': 'rac', 'user': user})
            except:
                return render(request, 'signupapp/ok_in.html',
                              {'message': error_message, 'from': 'bad_entry_signup', 'user': user})
        else:
            return HttpResponseRedirect('/gncin/')
    else:
        return HttpResponseRedirect('/dologin/')


def racni(request):  # Register A Customer No Id
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if request.POST:
            request.session['racPostTemp'] = request.POST
            request.session['racEarlierFill'] = True
            if request.POST['id_num'] != 0 and request.POST['id_num'] != '':
                try:
                    int(request.POST['id_num'])
                    old_customer = CustomerInfo.objects.get(id_num=request.POST['id_num'])
                    states = State.objects.all()
                    cities = City.objects.all()
                    session = request.session
                    return render(request, 'signupapp/register_a_customer_name.html',
                                  {'states': states, 'cities': cities, 'user': user, 'session': request.session,
                                   'error_message': 'کد ملی {} قبلا در سامانه ثبت شده است'.format(
                                       request.POST['id_num'])})
                except:
                    try:
                        first_name, last_name = gn_name_validator(request.POST['first_name'], request.POST['last_name'])
                        customer = user.customerinfo_set.create(
                            first_name=first_name,
                            last_name=last_name,
                            father_name='',
                            gender=request.POST['gender'],
                            id_num=0,
                            state=request.POST['state'],
                            city=request.POST['city'],
                            job=request.POST['job'],
                            about='',
                            relative_id_num=0,
                            relativity='',
                            searched_num=0,
                            registered_records_num=0,
                            registered_late_records_num=0,
                            customer_link=create_secure_link_20(small_alphabet_list, capital_alphabet_list),
                        )
                        customer.save()
                        if request.POST['relative_id_num'] != '':
                            try:
                                int(request.POST['relative_id_num'])
                                customer.relative_id_num = request.POST['relative_id_num']
                            except:
                                pass
                        if request.POST['relativity'] != '':
                            customer.relativity = request.POST['relativity']
                        if request.POST['father_name'] != '':
                            customer.father_name = request.POST['father_name']
                        if request.POST['id_num'] != '':
                            try:
                                int(request.POST['id_num'])
                                customer.id_num = request.POST['id_num']
                            except:
                                pass
                        if request.POST['about'] != '':
                            customer.about = request.POST['about']
                        state = State.objects.get(name=customer.state)
                        city = state.city_set.get(name=customer.city)
                        state.used_num += 1
                        city.used_num += 1
                        customer.save()
                        state.save()
                        city.save()
                        request.session['racEarlierFill'] = False
                        request.session['racPostTemp'] = None
                        return render(request, 'signupapp/ok_in.html', {'message': 'اطلاعات {} با موفقیت ثبت شد'.format(
                            customer.first_name + ' ' + customer.last_name, ), 'from': 'racni', 'user': user})
                    except:
                        request.session['racEarlierFill'] = False
                        request.session['racPostTemp'] = None
                        return render(request, 'signupapp/ok_in.html',
                                      {'message': error_message, 'from': 'bad_entry_signup', 'user': user})
        else:
            request.session['racEarlierFill'] = False
            request.session['racPostTemp'] = None
            return HttpResponseRedirect('/gncin/')
    else:
        return HttpResponseRedirect('/dologin/')


def racnifg(request):  # Register A New Customer No Id From GCN/SCRN
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if request.session['from_gcn'] == True:
            states = State.objects.all()
            cities = City.objects.all()
            return render(request, 'signupapp/register_a_customer_name.html',
                          {'states': states, 'cities': cities, 'user': user, 'session': request.session})
        else:
            return HttpResponseRedirect('/gncn/')
    else:
        return HttpResponseRedirect('/dologin')


def racft(request):  # Register a Customer From Tradesmen
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if request.POST:
            try:
                first_name, last_name = gn_name_validator(request.POST['first_name'], request.POST['last_name'])
                customer = user.customerinfo_set.create(
                    first_name=first_name,
                    last_name=last_name,
                    father_name='',
                    gender=request.POST['gender'],
                    id_num=request.POST['id_num'],
                    state=request.POST['state'],
                    city=request.POST['city'],
                    job=request.POST['job'],
                    about='',
                    relative_id_num=0,
                    relativity='',
                    searched_num=0,
                    registered_records_num=0,
                    registered_late_records_num=0,
                    customer_link=create_secure_link_20(small_alphabet_list, capital_alphabet_list),
                )
                customer.save()
                if request.POST['relative_id_num'] != '':
                    try:
                        int(request.POST['relative_id_num'])
                        customer.relative_id_num = request.POST['relative_id_num']
                    except:
                        pass
                if request.POST['relativity'] != '':
                    customer.relativity = request.POST['relativity']
                if request.POST['father_name'] != '':
                    customer.father_name = request.POST['father_name']
                if request.POST['about'] != '':
                    customer.about = request.POST['about']
                state = State.objects.get(name=customer.state)
                city = state.city_set.get(name=customer.city)
                state.used_num += 1
                city.used_num += 1
                customer.save()
                state.save()
                city.save()
                request.session.pop('tradesman')
                return render(request, 'signupapp/ok_in.html', {
                    'message': 'اطلاعات {} با موفقیت ثبت شد'.format(customer.first_name + ' ' + customer.last_name, ),
                    'from': 'racni', 'user': user})
            except:
                return render(request, 'signupapp/ok_in.html',
                              {'message': error_message, 'from': 'bad_entry_signup', 'user': user})
        else:
            return HttpResponseRedirect('/gncin/')
    else:
        return HttpResponseRedirect('/dologin/')


def racfs(request):  # Register a Customer From SAC
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if request.POST:
            try:
                first_name, last_name = gn_name_validator(request.POST['first_name'], request.POST['last_name'])
                customer = user.customerinfo_set.create(
                    first_name=first_name,
                    last_name=last_name,
                    father_name='',
                    gender=request.POST['gender'],
                    id_num=request.POST['id_num'],
                    state=request.POST['state'],
                    city=request.POST['city'],
                    job=request.POST['job'],
                    about='',
                    relative_id_num=0,
                    relativity='',
                    searched_num=0,
                    registered_records_num=0,
                    registered_late_records_num=0,
                    customer_link=create_secure_link_20(small_alphabet_list, capital_alphabet_list),
                )
                customer.save()
                if request.POST['relative_id_num'] != '':
                    try:
                        int(request.POST['relative_id_num'])
                        customer.relative_id_num = request.POST['relative_id_num']
                    except:
                        pass
                if request.POST['relativity'] != '':
                    customer.relativity = request.POST['relativity']
                if request.POST['father_name'] != '':
                    customer.father_name = request.POST['father_name']
                if request.POST['about'] != '':
                    customer.about = request.POST['about']
                state = State.objects.get(name=customer.state)
                city = state.city_set.get(name=customer.city)
                state.used_num += 1
                city.used_num += 1
                customer.save()
                state.save()
                city.save()
                return render(request, 'signupapp/ok_in.html', {
                    'message': 'اطلاعات {} با موفقیت ثبت شد'.format(customer.first_name + ' ' + customer.last_name, ),
                    'from': 'racni', 'user': user})
            except:
                return render(request, 'signupapp/ok_in.html',
                              {'message': error_message, 'from': 'bad_entry_signup', 'user': user})
        else:
            try:
                searched_id_num = request.session['searched_id_num']
                request.session.pop('searched_id_num')
                job_categories = JobCategory.objects.all()
                states = State.objects.all()
                cities = City.objects.all()
                return render(request, 'signupapp/register_a_customer.html',
                              {'jobcategories': job_categories, 'states': states, 'cities': cities, 'user': user,
                               'session': request.session, 'from': 'racfs', 'sin': str(searched_id_num)})
            except:
                return HttpResponseRedirect('/sac/')
    else:
        return HttpResponseRedirect('/dologin/')


def rar(request):  # Register A Record    #USELESS
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if request.POST:
            try:
                cyear = str(khayyam.JalaliDatetime.now().date())[0:4]  # Current year
                cdcd = str(khayyam.JalaliDatetime.now().date()).replace(cyear, str(
                    int(cyear) + 20))  # Custom Debt Clearance Date
                s_year = request.POST['debt_start_date_year']
                s_month = request.POST['debt_start_date_month']
                s_day = request.POST['debt_start_date_day']
                d_year = request.POST['debt_due_date_year']
                d_month = request.POST['debt_due_date_month']
                d_day = request.POST['debt_due_date_day']
                customer = CustomerInfo.objects.get(id_num=request.POST['id_num'])
                record = customer.noncreditworthyinfo_set.create(
                    register_date=str(khayyam.JalaliDatetime.now().date()),
                    debt_amount=request.POST['debt_amount'],
                    registered_by_id=user.id,
                    debt_kind=request.POST['debt_kind'],
                    debt_start_date=request.POST['debt_start_date_year'] + '-' + request.POST[
                        'debt_start_date_month'] + '-' + request.POST['debt_start_date_day'],
                    debt_due_date=request.POST['debt_due_date_year'] + '-' + request.POST['debt_due_date_month'] + '-' +
                                  request.POST['debt_due_date_day'],
                    proof_for_debt=request.POST['proof_for_debt'],
                    debt_cleared=False,
                    gone_bad=False,
                    debt_clearance_date=cdcd,
                    about=request.POST['about'],
                    record_link=create_secure_link_30(small_alphabet_list, capital_alphabet_list),
                )
                registered_by = PermanentlyInfo.objects.get(username=request.user.username)
                record1 = registered_by.registeredrecords_set.create(
                    customer_id=customer.id,
                    customer_id_num=request.POST['id_num'],
                    customer_first_name=request.POST['first_name'],
                    customer_last_name=request.POST['last_name'],
                    register_date=str(khayyam.JalaliDatetime.now().date()),
                    debt_amount=request.POST['debt_amount'],
                    registered_by_id=user.id,
                    debt_kind=request.POST['debt_kind'],
                    debt_start_date=request.POST['debt_start_date_year'] + '-' + request.POST[
                        'debt_start_date_month'] + '-' + request.POST['debt_start_date_day'],
                    debt_due_date=request.POST['debt_due_date_year'] + '-' + request.POST['debt_due_date_month'] + '-' +
                                  request.POST['debt_due_date_day'],
                    proof_for_debt=request.POST['proof_for_debt'],
                    debt_cleared=False,
                    gone_bad=False,
                    debt_clearance_date=cdcd,
                    about=request.POST['about'],
                    record_link=record.record_link,
                )
                if khayyam.JalaliDatetime.now().date() > record.debt_due_date:
                    record.gone_bad = True
                    record1.gone_bad = True
                    customer.registered_late_records_num += 1
                record.save()
                record1.save()
                user.registered_records_num += 1
                customer.registered_records_num += 1
                user.save()
                customer.save()
                debt_document = user.debtdocument_set.get(value=record.proof_for_debt)
                debt_document.used_num += 1
                debt_document.save()
                return render(request, 'signupapp/ok_in.html', {
                    'message': 'گزارش برای {} {} با موفقیت ثبت شد'.format(customer.first_name, customer.last_name),
                    'from': 'rar', 'user': user})
            except:
                return render(request, 'signupapp/ok_in.html',
                              {'message': error_message, 'from': 'bad_entry_signup', 'user': user})
        else:
            request.session['last_touch'] = khayyam.JalaliDatetime.now()
            return HttpResponseRedirect('/gcin/')
    else:
        return HttpResponseRedirect("/")


def rarwi(request, customer_id):  # Register A Record With Id
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if request.POST:
            try:
                cyear = str(khayyam.JalaliDatetime.now().date())[0:4]  # Current year
                cdcd = str(khayyam.JalaliDatetime.now().date()).replace(cyear, str(
                int(cyear) + 20))  # Custom Debt Clearance Date
#                s_year = request.POST['debt_start_date_year']
#                s_month = request.POST['debt_start_date_month']
#                s_day = request.POST['debt_start_date_day']
#                d_year = request.POST['debt_due_date_year']
#                d_month = request.POST['debt_due_date_month']
#                d_day = request.POST['debt_due_date_day']
                customer = CustomerInfo.objects.get(id=customer_id)
                record = customer.noncreditworthyinfo_set.create(
                    register_date=str(khayyam.JalaliDatetime.now().date()),
                    debt_amount=request.POST['debt_amount'],
                    registered_by_id=user.id,
                    debt_kind=request.POST['debt_kind'],
#                    debt_start_date=request.POST['debt_start_date_year'] + '-' + request.POST[
#                        'debt_start_date_month'] + '-' + request.POST['debt_start_date_day'],
                    debt_start_date=str(request.POST['debt_start_date']).replace('/', '-'),
#                    debt_due_date=request.POST['debt_due_date_year'] + '-' + request.POST['debt_due_date_month'] + '-' +
#                                  request.POST['debt_due_date_day'],
                    debt_due_date=str(request.POST['debt_due_date']).replace('/', '-'),
                    proof_for_debt=request.POST['proof_for_debt'],
                    debt_cleared=False,
                    gone_bad=False,
                    debt_clearance_date=cdcd,
                    about='',
                    record_link=create_secure_link_30(small_alphabet_list, capital_alphabet_list),
                )
                registered_by = PermanentlyInfo.objects.get(username=request.user.username)
                record1 = registered_by.registeredrecords_set.create(
                    customer_id_num=customer.id_num,
                    customer_id=customer.id,
                    customer_first_name=customer.first_name,
                    customer_last_name=customer.last_name,
                    register_date=str(khayyam.JalaliDatetime.now().date()),
                    debt_amount=request.POST['debt_amount'],
                    registered_by_id=user.id,
                    debt_kind=request.POST['debt_kind'],
#                    debt_start_date=request.POST['debt_start_date_year'] + '-' + request.POST[
#                        'debt_start_date_month'] + '-' + request.POST['debt_start_date_day'],
                    debt_start_date=str(request.POST['debt_start_date']).replace('/', '-'),
#                    debt_due_date=request.POST['debt_due_date_year'] + '-' + request.POST['debt_due_date_month'] + '-' +
#                                  request.POST['debt_due_date_day'],
                    debt_due_date=str(request.POST['debt_due_date']).replace('/', '-'),
                    proof_for_debt=request.POST['proof_for_debt'],
                    debt_cleared=False,
                    gone_bad=False,
                    debt_clearance_date=cdcd,
                    about='',
                    record_link=record.record_link,
                )
                if str(khayyam.JalaliDatetime.now().date()) > record.debt_due_date:
                    record.gone_bad = True
                    record1.gone_bad = True
                    customer.registered_late_records_num += 1
                if request.POST['about'] != '':
                    record.about = request.POST['about']
                    record1.about = request.POST['about']
                record.save()
                record1.save()
                user.registered_records_num += 1
                customer.registered_records_num += 1
                user.save()
                customer.save()
                if record.proof_for_debt != "none":
                    debt_document = user.debtdocument_set.get(value=record.proof_for_debt)
                    debt_document.used_num += 1
                    debt_document.save()
                return render(request, 'signupapp/ok_in.html', {
                    'message': 'گزارش برای {} {} با موفقیت ثبت شد'.format(customer.first_name, customer.last_name),
                    'from': 'rar', 'user': user})
            except:
                return render(request, 'signupapp/ok_in.html',
                              {'message': error_message, 'from': 'bad_entry_signup', 'user': user})
        else:
            try:
                request.session['last_touch'] = khayyam.JalaliDatetime.now()
                customer = CustomerInfo.objects.get(id=customer_id)
                dds = user.debtdocument_set.all()
                today = str(khayyam.JalaliDatetime.now().date())
                return render(request, 'signupapp/register_a_record.html',
                              {'customer': customer, 'user': user, 'debt_documents': dds, 'today': today,
                               'from': 'rarwi'})
            except:
                return render(request, 'signupapp/ok_in.html',
                              {'message': 'کاربر مورد نظر ثبت نشده است', 'from': 'failed_rarwi', 'user': user})
    else:
        return HttpResponseRedirect("/")


def scri(request, customer_id_num):  # Show Customer's Records by ID
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        try:
            customer = CustomerInfo.objects.get(id_num=customer_id_num)
            today = khayyam.JalaliDatetime.now().date()
            customer.searched_num += 1
            customer_records = customer.noncreditworthyinfo_set.all()
            records = [record for record in customer_records if record.debt_cleared == 0]
            for record in records:
                if str(today) > str(record.debt_due_date):
                    record.gone_bad = True
                else:
                    record.gone_bad = False
                record.save()
            amount = 0
            if len(records) != 0:
                for record in records:
                    amount += int(record.debt_amount)
                amount = amount // len(records)
            amount = round(amount, -3)
            if len(records) == 0:
                first_part = 'بدهی ثبت شده برای این کاربر وجود ندارد'
            elif len(records) == 1:
                if amount >= 1000 and amount < 1000000:
                    amount = amount // 1000
                    first_part = 'یک مورد بدهی ثبت شده با مبلغ {} هزار تومان'.format(str(amount), )
                elif amount >= 1000000 and amount < 1000000000:
                    amount = amount // 1000
                    first_part = 'یک مورد بدهی ثبت شده با مبلغ {} میلیون و {} هزار تومان'.format(str(amount//1000), str(amount - (amount//1000)*1000))
                elif amount >= 1000000000:
                    amount = amount // 1000
                    first_part = 'یک مورد بدهی ثبت شده با مبلغ {} میلیارد و {} میلیون و {} هزار تومان'.format(str(amount // 1000000),
                                                                                                 str((amount - (amount // 1000000) * 1000000) // 1000),
                                                                                                 str(amount - (amount // 1000) * 1000))
                else:
                    first_part = 'بدهی ثبت شده برای این کاربر وجود ندارد'
            else:
                if amount >= 1000 and amount < 1000000:
                    amount = amount // 1000
                    first_part = '{} بدهی ثبت شده با میانگین مبلغ {} هزار تومان'.format(str(len(records)), str(amount))
                elif amount >= 1000000 and amount < 1000000000:
                    amount = amount // 1000
                    first_part = '{} بدهی ثبت شده با میانگین مبلغ {} میلیون و {} هزار تومان'.format(str(len(records)), str(amount//1000), str(amount - (amount//1000)*1000))
                elif amount >= 1000000000:
                    amount = amount // 1000
                    first_part = '{} بدهی ثبت شده با میانگین مبلغ {} میلیارد و {} میلیون و {} هزار تومان'.format(str(len(records)), str(amount // 1000000),
                                                                                                 str((amount - (amount // 1000000) * 1000000) // 1000),
                                                                                                 str(amount - (amount // 1000) * 1000))
                else:
                    first_part = 'بدهی ثبت شده برای این کاربر وجود ندارد'
            bad_records = [record for record in customer_records if record.debt_cleared == 0 and record.gone_bad == 1]
            bad_amount = 0
            bad_average_date = 0
            if len(bad_records) != 0:
                for record in bad_records:
                    bad_amount += int(record.debt_amount)
                bad_amount = bad_amount // len(bad_records)
                bad_amount = round(bad_amount, -3)
                bad_month2 = [(today - khayyam.JalaliDatetime.date(record.debt_due_date)).days // 30 for record in
                              bad_records]
                bad_month1 = 0
                for bms in bad_month2: bad_month1 += bms
                bad_average_date = bad_month1 // len(bad_month2)
            if len(bad_records) == 0:
                second_part = 'تاخیر در پرداخت برای این فرد وجود ندارد'
            elif len(bad_records) == 1:
                if bad_amount >= 1000 and bad_amount < 1000000:
                    bad_amount = bad_amount // 1000
                    second_part = 'یک مورد بدهی دارای تاخیر با مبلغ {} هزار تومان و تاخیر {} ماه'.format(str(bad_amount),
                                                                                            str(bad_average_date))
                elif bad_amount >= 1000000 and bad_amount < 1000000000:
                    bad_amount = bad_amount // 1000
                    second_part = 'یک مورد بدهی دارای تاخیر با مبلغ {} میلیون و {} هزار تومان و تاخیر {} ماه'.format(str(bad_amount//1000), str(bad_amount - (bad_amount//1000)*1000), str(bad_average_date))
                elif bad_amount >= 1000000000:
                    bad_amount = bad_amount // 1000
                    second_part = 'یک مورد بدهی دارای تاخیر با مبلغ {} میلیارد و {} میلیون و {} هزار تومان و تاخیر {} ماه'.format(str(bad_amount // 1000000),
                                                                                                 str((bad_amount - (bad_amount // 1000000) * 1000000) // 1000),
                                                                                                 str(bad_amount - (bad_amount // 1000) * 1000), str(bad_average_date))
                else:
                    second_part = 'تاخیر در پرداخت برای این فرد وجود ندارد'
            else:
                if bad_amount >= 1000 and bad_amount < 1000000:
                    bad_amount = bad_amount // 1000
                    second_part = '{} مورد بدهی دارای تاخیر با میانگین مبلغ {} هزار تومان '.format(str(len(bad_records)), str(
                    bad_amount), ) + '\n' + 'و میانگین تاخیر {} ماه'.format(str(bad_average_date), )
                elif bad_amount >= 1000000 and bad_amount < 1000000000:
                    bad_amount = bad_amount // 1000
                    second_part = '{} بدهی دارای تاخیر با میانگین مبلغ {} میلیون و {} هزار تومان'.format(str(len(bad_records)), str(bad_amount//1000), str(bad_amount - (bad_amount//1000)*1000)) + '\n' + 'و میانگین تاخیر {} ماه'.format(str(bad_average_date))
                elif bad_amount >= 1000000000:
                    bad_amount = bad_amount // 1000
                    second_part = '{} بدهی ثبت شده با میانگین مبلغ {} میلیارد و {} میلیون و {} هزار تومان'.format(str(len(bad_records)), str(bad_amount // 1000000),
                                                                                                 str((bad_amount - (bad_amount // 1000000) * 1000000) // 1000),
                                                                                                 str(bad_amount - (bad_amount // 1000) * 1000)) + '\n' + 'و میانگین تاخیر {} ماه'.format(str(bad_average_date))
                else:
                    second_part = 'تاخیر در پرداخت برای این فرد وجود ندارد'
            if user.acount_type == "base" or user.acount_type == "bronze":
                message = {'part1': "استعلام کاربر با کد ملی {}".format(str(customer.id_num), ), 'part2': str(
                    customer.first_name) + " " + str(customer.last_name), 'part3': first_part, 'part4': second_part}
            elif user.acount_type == "silver":
                message = {'part1': "استعلام کاربر با کد ملی {}".format(str(customer.id_num), ), 'part2': str(
                    customer.first_name) + " " + str(
                    customer.last_name), 'part3': first_part, 'part4': second_part, 'part5': "استان {} و صنف {}".format(
                    customer.state, customer.job)}
            else:
                drecords = [record for record in customer_records if
                        record.debt_cleared == 1 and str(record.debt_start_date) > str(
                                record.debt_due_date)]  # DoneRecords
                damount = 0
                daverage_date = 0
                if len(drecords) != 0:
                    for record in drecords:
                        damount += int(record.debt_amount)
                    damount = damount // len(drecords)
                    damount = round(damount, -3)
                    dmonth2 = [(record.debt_clearance_date - record.debt_due_date).days // 30 for record in drecords]
                    dmonth1 = 0
                    for bms in dmonth2: dmonth1 += bms
                    daverage_date = dmonth1 // len(dmonth2)
                if len(drecords) == 0:
                    third_part = 'در سوابق قبلی دارای خوش حسابی است'
                elif len(drecords) == 1:
                    if damount >= 1000 and damount < 1000000:
                        damount = damount // 1000
                        third_part = 'قبلا دارای یک مورد بدهی با مبلغ {} هزار تومان و تاخیر {} ماه بوده است'.format(str(damount),
                                                                                                         str(daverage_date))
                    elif damount >= 1000000 and damount < 1000000000:
                        damount = damount // 1000
                        third_part = 'قبلا دارای یک مورد بدهی با مبلغ {} میلیون و {} هزار تومان و تاخیر {} ماه بوده است'.format(
                            str(damount  // 1000), str(damount  - (damount // 1000) * 1000),
                                str(daverage_date))
                    elif damount >= 1000000000:
                        damount = damount // 1000
                        third_part = 'قبلا دارای یک مورد بدهی با مبلغ {} میلیارد و {} میلیون و {} هزار تومان و تاخیر {} ماه بوده است'.format(
                            str(damount // 1000000),
                            str((damount - (damount // 1000000) * 1000000) // 1000),
                            str(damount - (damount // 1000) * 1000), str(daverage_date))
                    else:
                        third_part = 'در سوابق قبلی دارای خوش حسابی است'
                else:
                    if damount >= 1000 and damount < 1000000:
                        damount = damount // 1000
                        third_part = 'قبلا دارای {} مورد بدهی با میانگین مبلغ {} هزار تومان'.format(str(len(drecords)), str(damount)) + '\n' + ' و میانگین تاخیر {} ماه بوده است'.format(
                            str(daverage_date), )
                    elif damount >= 1000000 and damount < 1000000000:
                        damount = damount // 1000
                        third_part = 'قبلا دارای {} مورد بدهی با میانگین مبلغ {} میلیون و {} هزار تومان'.format(
                            str(len(drecords)), str(damount // 1000),
                            str(damount - (damount // 1000) * 1000)) + '\n' + 'و میانگین تاخیر {} ماه بوده است'.format(
                            str(daverage_date))
                    elif damount >= 1000000000:
                        damount = damount // 1000
                        third_part = 'قبلا دارای {} مورد بدهی با میانگین مبلغ {} میلیارد و {} میلیون و {} هزار تومان'.format(
                            str(len(drecords)), str(damount // 1000000),
                            str((damount - (damount // 1000000) * 1000000) // 1000),
                            str(damount - (damount // 1000) * 1000)) + '\n' + 'و میانگین تاخیر {} ماه بوده است'.format(
                            str(daverage_date))
                    else:
                        third_part = 'در سوابق قبلی دارای خوش حسابی است'
                message = {'part1': "استعلام کاربر با کد ملی {}".format(str(customer.id_num), ),'part2': str(
                    customer.first_name) + " " + str(
                    customer.last_name), 'part3': first_part, 'part4': second_part,'part5': "استان {} و صنف {}".format(
                    customer.state, customer.job), 'part6': third_part}
            return render(request, 'signupapp/ok_in.html', {'message': message, 'from': 'scr', 'user': user})
        except:
            request.session['searched_id_num'] = customer_id_num
            return render(request, 'signupapp/ok_in.html', {
                'message': 'اطلاعاتی با کد ملی {} در سامانه سجام ثبت نشده است'.format(str(customer_id_num), ),
                'from': 'failed_scr', 'user': user})
    else:
        return HttpResponseRedirect('/dologin/')


def scrii(request, customer_id):  # Show Customer's Records by ID ID
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        try:
            customer = CustomerInfo.objects.get(id=customer_id)
            today = khayyam.JalaliDatetime.now().date()
            customer.searched_num += 1
            customer_records = customer.noncreditworthyinfo_set.all()
            records = [record for record in customer_records if record.debt_cleared == 0]
            for record in records:
                if str(today) > str(record.debt_due_date):
                    record.gone_bad = True
                else:
                    record.gone_bad = False
                record.save()
            amount = 0
            if len(records) != 0:
                for record in records:
                    amount += int(record.debt_amount)
                amount = amount // len(records)
            amount = round(amount, -3)
            if len(records) == 0:
                first_part = 'بدهی ثبت شده برای این کاربر وجود ندارد'
            elif len(records) == 1:
                if amount >= 1000 and amount < 1000000:
                    amount = amount // 1000
                    first_part = 'یک مورد بدهی ثبت شده با مبلغ {} هزار تومان'.format(str(amount), )
                elif amount >= 1000000 and amount < 1000000000:
                    amount = amount // 1000
                    first_part = 'یک مورد بدهی ثبت شده با مبلغ {} میلیون و {} هزار تومان'.format(str(amount//1000), str(amount - (amount//1000)*1000))
                elif amount >= 1000000000:
                    amount = amount // 1000
                    first_part = 'یک مورد بدهی ثبت شده با مبلغ {} میلیارد و {} میلیون و {} هزار تومان'.format(str(amount // 1000000),
                                                                                                 str((amount - (amount // 1000000) * 1000000) // 1000),
                                                                                                 str(amount - (amount // 1000) * 1000))
                else:
                    first_part = 'بدهی ثبت شده برای این کاربر وجود ندارد'
            else:
                if amount >= 1000 and amount < 1000000:
                    amount = amount // 1000
                    first_part = '{} بدهی ثبت شده با میانگین مبلغ {} هزار تومان'.format(str(len(records)), str(amount))
                elif amount >= 1000000 and amount < 1000000000:
                    amount = amount // 1000
                    first_part = '{} بدهی ثبت شده با میانگین مبلغ {} میلیون و {} هزار تومان'.format(str(len(records)), str(amount//1000), str(amount - (amount//1000)*1000))
                elif amount >= 1000000000:
                    amount = amount // 1000
                    first_part = '{} بدهی ثبت شده با میانگین مبلغ {} میلیارد و {} میلیون و {} هزار تومان'.format(str(len(records)), str(amount // 1000000),
                                                                                                 str((amount - (amount // 1000000) * 1000000) // 1000),
                                                                                                 str(amount - (amount // 1000) * 1000))
                else:
                    first_part = 'بدهی ثبت شده برای این کاربر وجود ندارد'
            bad_records = [record for record in customer_records if record.debt_cleared == 0 and record.gone_bad == 1]
            bad_amount = 0
            bad_average_date = 0
            if len(bad_records) != 0:
                for record in bad_records:
                    bad_amount += int(record.debt_amount)
                bad_amount = bad_amount // len(bad_records)
                bad_amount = round(bad_amount, -3)
                bad_month2 = [(today - khayyam.JalaliDatetime.date(record.debt_due_date)).days // 30 for record in
                              bad_records]
                bad_month1 = 0
                for bms in bad_month2: bad_month1 += bms
                bad_average_date = bad_month1 // len(bad_month2)
            if len(bad_records) == 0:
                second_part = 'تاخیر در پرداخت برای این فرد وجود ندارد'
            elif len(bad_records) == 1:
                if bad_amount >= 1000 and bad_amount < 1000000:
                    bad_amount = bad_amount // 1000
                    second_part = 'یک مورد بدهی دارای تاخیر با مبلغ {} هزار تومان و تاخیر {} ماه'.format(str(bad_amount),
                                                                                            str(bad_average_date))
                elif bad_amount >= 1000000 and bad_amount < 1000000000:
                    bad_amount = bad_amount // 1000
                    second_part = 'یک مورد بدهی دارای تاخیر با مبلغ {} میلیون و {} هزار تومان و تاخیر {} ماه'.format(str(bad_amount//1000), str(bad_amount - (bad_amount//1000)*1000), str(bad_average_date))
                elif bad_amount >= 1000000000:
                    bad_amount = bad_amount // 1000
                    second_part = 'یک مورد بدهی دارای تاخیر با مبلغ {} میلیارد و {} میلیون و {} هزار تومان و تاخیر {} ماه'.format(str(bad_amount // 1000000),
                                                                                                 str((bad_amount - (bad_amount // 1000000) * 1000000) // 1000),
                                                                                                 str(bad_amount - (bad_amount // 1000) * 1000), str(bad_average_date))
                else:
                    second_part = 'تاخیر در پرداخت برای این فرد وجود ندارد'
            else:
                if bad_amount >= 1000 and bad_amount < 1000000:
                    bad_amount = bad_amount // 1000
                    second_part = '{} مورد بدهی دارای تاخیر با میانگین مبلغ {} هزار تومان '.format(str(len(bad_records)), str(
                    bad_amount), ) + '\n' + 'و میانگین تاخیر {} ماه'.format(str(bad_average_date), )
                elif bad_amount >= 1000000 and bad_amount < 1000000000:
                    bad_amount = bad_amount // 1000
                    second_part = '{} بدهی دارای تاخیر با میانگین مبلغ {} میلیون و {} هزار تومان'.format(str(len(bad_records)), str(bad_amount//1000), str(bad_amount - (bad_amount//1000)*1000)) + '\n' + 'و میانگین تاخیر {} ماه'.format(str(bad_average_date))
                elif bad_amount >= 1000000000:
                    bad_amount = bad_amount // 1000
                    second_part = '{} بدهی ثبت شده با میانگین مبلغ {} میلیارد و {} میلیون و {} هزار تومان'.format(str(len(bad_records)), str(bad_amount // 1000000),
                                                                                                 str((bad_amount - (bad_amount // 1000000) * 1000000) // 1000),
                                                                                                 str(bad_amount - (bad_amount // 1000) * 1000)) + '\n' + 'و میانگین تاخیر {} ماه'.format(str(bad_average_date))
                else:
                    second_part = 'تاخیر در پرداخت برای این فرد وجود ندارد'
            if user.acount_type == "base" or user.acount_type == "bronze":
                message = {'part1': "استعلام کاربر با کد ملی {}".format(str(customer.id_num), ), 'part2': str(
                    customer.first_name) + " " + str(customer.last_name), 'part3': first_part, 'part4': second_part}
            elif user.acount_type == "silver":
                message = {'part1': "استعلام کاربر با کد ملی {}".format(str(customer.id_num), ), 'part2': str(
                    customer.first_name) + " " + str(
                    customer.last_name), 'part3': first_part, 'part4': second_part, 'part5': "استان {} و صنف {}".format(
                    customer.state, customer.job)}
            else:
                drecords = [record for record in customer_records if
                        record.debt_cleared == 1 and str(record.debt_start_date) > str(
                                record.debt_due_date)]  # DoneRecords
                damount = 0
                daverage_date = 0
                if len(drecords) != 0:
                    for record in drecords:
                        damount += int(record.debt_amount)
                    damount = damount // len(drecords)
                    damount = round(damount, -3)
                    dmonth2 = [(record.debt_clearance_date - record.debt_due_date).days // 30 for record in drecords]
                    dmonth1 = 0
                    for bms in dmonth2: dmonth1 += bms
                    daverage_date = dmonth1 // len(dmonth2)
                if len(drecords) == 0:
                    third_part = 'در سوابق قبلی دارای خوش حسابی است'
                elif len(drecords) == 1:
                    if damount >= 1000 and damount < 1000000:
                        damount = damount // 1000
                        third_part = 'قبلا دارای یک مورد بدهی با مبلغ {} هزار تومان و تاخیر {} ماه بوده است'.format(str(damount),
                                                                                                         str(daverage_date))
                    elif damount >= 1000000 and damount < 1000000000:
                        damount = damount // 1000
                        third_part = 'قبلا دارای یک مورد بدهی با مبلغ {} میلیون و {} هزار تومان و تاخیر {} ماه بوده است'.format(
                            str(damount  // 1000), str(damount  - (damount // 1000) * 1000),
                                str(daverage_date))
                    elif damount >= 1000000000:
                        damount = damount // 1000
                        third_part = 'قبلا دارای یک مورد بدهی با مبلغ {} میلیارد و {} میلیون و {} هزار تومان و تاخیر {} ماه بوده است'.format(
                            str(damount // 1000000),
                            str((damount - (damount // 1000000) * 1000000) // 1000),
                            str(damount - (damount // 1000) * 1000), str(daverage_date))
                    else:
                        third_part = 'در سوابق قبلی دارای خوش حسابی است'
                else:
                    if damount >= 1000 and damount < 1000000:
                        damount = damount // 1000
                        third_part = 'قبلا دارای {} مورد بدهی با میانگین مبلغ {} هزار تومان'.format(str(len(drecords)), str(damount)) + '\n' + ' و میانگین تاخیر {} ماه بوده است'.format(
                            str(daverage_date), )
                    elif damount >= 1000000 and damount < 1000000000:
                        damount = damount // 1000
                        third_part = 'قبلا دارای {} مورد بدهی با میانگین مبلغ {} میلیون و {} هزار تومان'.format(
                            str(len(drecords)), str(damount // 1000),
                            str(damount - (damount // 1000) * 1000)) + '\n' + 'و میانگین تاخیر {} ماه بوده است'.format(
                            str(daverage_date))
                    elif damount >= 1000000000:
                        damount = damount // 1000
                        third_part = 'قبلا دارای {} مورد بدهی با میانگین مبلغ {} میلیارد و {} میلیون و {} هزار تومان'.format(
                            str(len(drecords)), str(damount // 1000000),
                            str((damount - (damount // 1000000) * 1000000) // 1000),
                            str(damount - (damount // 1000) * 1000)) + '\n' + 'و میانگین تاخیر {} ماه بوده است'.format(
                            str(daverage_date))
                    else:
                        third_part = 'در سوابق قبلی دارای خوش حسابی است'
                message = {'part1': "استعلام کاربر با کد ملی {}".format(str(customer.id_num), ), 'part2': str(
                    customer.first_name) + " " + str(
                    customer.last_name), 'part3': first_part, 'part4': second_part, 'part5': "استان {} و صنف {}".format(
                    customer.state, customer.job), 'part6': third_part}
            return render(request, 'signupapp/ok_in.html', {'message': message, 'from': 'scr', 'user': user})
        except:
            return HttpResponseRedirect('/sac')
    else:
        return HttpResponseRedirect('/dologin/')


def scrn(request, customer_name):  # Show Customer's Records by NAME
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        c_first_name, c_last_name = scrn_name_validator(str(customer_name))
        try:
            customer_list1 = [customer for customer in CustomerInfo.objects.all() if
                              customer.first_name == c_first_name and customer.last_name == c_last_name]
            customer_ids = {customer.id for customer in customer_list1}
            customer_list = []
            for customer in customer_ids:
                customer1 = CustomerInfo.objects.get(id=customer)
                customer_list.append(customer1)
            if len(customer_list) != 0:
                return render(request, 'signupapp/show_found_users.html', {'users': customer_list, 'user': user})
            else:
                request.session['from_gcn'] = True
                request.session['first_name'] = c_first_name
                request.session['last_name'] = c_last_name
                return render(request, 'signupapp/ok_in.html', {
                    'message': 'اطلاعات {} در سامانه سجام ثبت نشده است'.format(c_first_name + ' ' + c_last_name, ),
                    'from': 'empty_scrn', 'user': user})
        except:
            return render(request, 'signupapp/ok_in.html',
                          {'message': error_message, 'from': 'failed_scrn', 'user': user})
    else:
        return HttpResponseRedirect('/dologin/')


def sac(request):  # Search A Customer
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if user.last_search_date == str(khayyam.JalaliDatetime.now().date()):
            if int(user.day_search) <= 99:
                if request.POST:
                    user.day_search += 1
                    user.last_search_date = str(khayyam.JalaliDatetime.now().date())
                    user.save()
                    if 'customer_id_num' in request.POST:
                        return HttpResponseRedirect('/scri/' + request.POST['customer_id_num'])
                    elif 'customer_first_name' in request.POST:
                        return HttpResponseRedirect(
                            '/scrn/' + request.POST['customer_first_name'] + '_' + request.POST['customer_last_name'])
                else:
                    return render(request, 'signupapp/get_customer_id_num_search.html', {})
            else:
                return render(request, 'signupapp/ok_in.html', {'user': user,
                                                                'message': 'مشتری گرامی، برای استعلام بیشتر از صد مشتری در روز، لطفا حساب کاربری خود را کامل کنید',
                                                                'from': 'done_sac', 'user': user})
        else:
            user.day_search = 0
            user.last_search_date = str(khayyam.JalaliDatetime.now().date())
            user.save()
            if request.POST:
                try:
                    user.day_search += 1
                    user.last_search_date = str(khayyam.JalaliDatetime.now().date())
                    user.save()
                    if 'customer_id_num' in request.POST:
                        return HttpResponseRedirect('/scri/' + request.POST['customer_id_num'])
                    elif 'customer_first_name' in request.POST:
                        return HttpResponseRedirect(
                            '/scrn/' + request.POST['customer_first_name'] + '_' + request.POST['customer_last_name'])
                except:
                    return render(request, 'signupapp/ok_in.html',
                                  {'message': error_message, 'from': 'bad_entry_signup', 'user': user})
            else:
                return render(request, 'signupapp/get_customer_id_num_search.html', {'user': user})
    else:
        return HttpResponseRedirect('/dologin/')


def uprofile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin/')
    else:
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        rrs0 = user.registeredrecords_set.all()  # Registered Records
        rrs1 = {record.customer_id for record in rrs0}
        rrs = []
        for id in rrs1:
            rrs2 = [record for record in rrs0 if record.customer_id == id]
            for record1 in rrs2:
                rrs.append(record1)
        rcs = user.customerinfo_set.all()  # Registered Customers
        try:
            union = Union.objects.get(value=user.union)
        except:
            union = user.union
        try:
            jobcategory = JobCategory.objects.get(value=user.job_category)
        except:
            jobcategory = user.job_category
        return render(request, 'signupapp/uprofile.html', {'user': user, 'rrs': rrs, 'rcs': rcs, 'union': union, 'jobcategory': jobcategory})


def pci(request):  # Pre Complete Information
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin/')
    else:
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if user.is_complete == 0:
            return render(request, 'signupapp/pre_ci_page.html', {'user': user})
        else:
            return HttpResponseRedirect('/uprofile/')


def ci_profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin/')
    else:
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        user1 = User.objects.get(username=request.user.username)
        unions1 = Union.objects.all()
        unions = [union for union in unions1 if union.approved == True]
        try:
            union = unions1.get(value=user.union)
            if union.approved == True:
                union_other = False
            else:
                union_other = True
        except:
            union = user.union
            union_other = True
        jobcategories1 = JobCategory.objects.all()
        jobcategories = [jc for jc in jobcategories1 if jc.approved == True]
        try:
            jobcategory = jobcategories1.get(value=user.job_category)
            if jobcategory.approved == True:
                jc_other = False
            else:
                jc_other = True
        except:
            jobcategory = user.job_category
            jc_other = True
        cities = City.objects.all()
        states = State.objects.all()
        if user.city != '':
            city = cities.get(name=user.city).value
        else:
            city = ''
        if user.state != '':
            state = states.get(name=user.state).value
        else:
            state = ''
        if not request.POST:
            if request.session['earlierFill'] != False:
                return render(request, 'signupapp/ci_profile_page.html',
                              {'user': user, 'unions': unions, 'union': union, 'union_other': union_other, 'jobcategories': jobcategories,
                               'jobcategory': jobcategory, 'jc_other': jc_other, 'cities': cities, 'states': states, 'city': city, 'state': state, 'from': 'cip',
                               'pt': request.session['postTemp'], 'ef': 'true'})
            else:
                return render(request, 'signupapp/ci_profile_page.html',
                              {'user': user, 'unions': unions, 'union': union, 'union_other': union_other, 'jobcategories': jobcategories,
                               'jobcategory': jobcategory, 'jc_other': jc_other, 'cities': cities, 'states': states, 'city': city, 'state': state,  'from': 'cip',
                               'ef': 'false'})
        else:
            try:
                request.session['postTemp'] = request.POST
                user.phone = request.POST['phone']
                if request.POST['mobile'][0] == 0 and str(request.POST['mobile']) != '0':
                    mobileTemp = ''
                    for num in range(1, len(request.POST['mobile'])):
                        mobileTemp += request.POST['mobile'][num]
                else:
                    mobileTemp = str(request.POST['mobile'])
                if str(user.mobile) != mobileTemp:
                    user.mobile = mobileTemp
                    user.mobile_is_varified = False
                    user.user_phone_varification_number = create_secure_link_4()
                user.fax = request.POST['fax']
                if str(user.id_num) != request.POST['id_num']:
                    try:
                        already_user = PermanentlyInfo.objects.get(id_num=request.POST['id_num'])
                        request.session['earlierFill'] = True
                        return render(request, 'signupapp/ok_in.html',
                                      {'message': 'کد ملی {} قبلا در سایت ثبت شده است'.format(request.POST['id_num'], ),
                                       'from': 'bad_cip', 'user': user})
                    except:
                        user.id_num = request.POST['id_num']
                user.father_name = request.POST['father_name']
                user.city = request.POST['city']
                user.state = request.POST['state']
                if request.POST['job_category'] == 'other':
                    user.job_category = request.POST['other_job_category']
                else:
                    if request.POST['job_category']:
                        user.job_category = request.POST['job_category']
                if request.POST['union'] == 'other':
                    user.union = request.POST['other_union']
                else:
                    if request.POST['union'] != '':
                        user.union = request.POST['union']
                user.business_license_num = request.POST['business_license_num']
                #            user.business_license_due_date = request.POST['business_license_due_date']
#                user.business_license_due_date = request.POST['blddy'] + "-" + request.POST['blddm'] + "-" + \
#                                                 request.POST['blddd']
                user.business_license_due_date = str(request.POST['business_license_due_date']).replace('/', '-')
                #            user.state = request.POST['state']
                #            user.city = request.POST['city']
#                user.address = request.POST['address']
                user.brand = request.POST['brand']
                #            user.birthday = request.POST['birthday']
#                user.birthday = request.POST['birthday_y'] + "-" + request.POST['birthday_m'] + "-" + request.POST[
#                   'birthday_d']
                user.birthday = str(request.POST['birthday']).replace('/', '-')
                user.gender = request.POST['gender']
                secEmailTemp = word_validator(request.POST['secondary_email'])
                if user.secondary_email != word_validator(request.POST['secondary_email']) and len(secEmailTemp) > 0:
                    try:
                        try:
                            user2 = PermanentlyInfo.objects.get(email=request.POST['secondary_email'])
                            request.session['earlierFill'] = True
                            return render(request, 'signupapp/ok_in.html', {
                                'message': 'ایمیل {} قبلا در سایت ثبت شده است'.format(
                                    request.POST['secondary_email'], ), 'from': 'bad_cip', 'user': user})
                        except:
                            user2 = PermanentlyInfo.objects.get(secondary_email=request.POST['secondary_email'])
                            request.session['earlierFill'] = True
                            return render(request, 'signupapp/ok_in.html', {
                                'message': 'ایمیل {} قبلا در سایت ثبت شده است'.format(
                                    request.POST['secondary_email'], ), 'from': 'bad_cip', 'user': user})
                    except:
                        user.secondary_email = word_validator(request.POST['secondary_email'])
                        user.secondary_email_is_activated = False
                        user.user_secondary_email_activation_link = create_secure_link_30(small_alphabet_list, capital_alphabet_list)
                        mail_message = "کاربر گرامی\n\nلطفا از لینک زیر برای فعال سازی ایمیل دوم خود در سامانه ی سجام استفاده نمایید:\n\nhttp://www.samanehestelam.com/aaa/{}\n\nبا تشکر\nسیستم جامع استعلام مشتریان = سجام\nآدرس سایت:\nwWw.SamanehEstelam.Org".format(str(user.user_secondary_email_activation_link))
#                        user_mail_func = send_email('samaneestelam@gmail.com', '0okmnji98U',[str(user.secondary_email)], message)
                        send_mail('تاییدایمیل دوم در امانه سجام', mail_message, 'info@samanehestelam.org',
                                  [str(user.secondary_email)], fail_silently=False)
                elif len(secEmailTemp) == 0:
                    user.secondary_email = ''
                    user.secondary_email_is_activated = False
                    user.user_secondary_email_activation_link = create_secure_link_30(small_alphabet_list, capital_alphabet_list)
                if user.username != word_validator(request.POST['username']):
                    try:
                        user2 = PermanentlyInfo.objects.get(username=request.POST['username'])
                        request.session['earlierFill'] = True
                        return render(request, 'signupapp/ok_in.html', {
                            'message': 'نام کاربری {} قبلا در سایت ثبت شده است'.format(request.POST['username'], ),
                            'from': 'bad_cip', 'user': user})
                    except:
                        user.username = word_validator(request.POST['username'])
                        user1.username = word_validator(request.POST['username'])
                if request.POST['about'] != '':
                    user.about = request.POST['about']
                user.save()
                user1.save()
                # The next 1 lines estimate the complete percentage and save it to the PermanentlyInfo
                complete_percentage1 = 0
                texts = [user.first_name, user.last_name, user.father_name, user.address, user.brand, user.union,
                         user.job_category, user.state, user.city, user.gender, user.b_name, user.b_branch_name,
                         user.email, user.secondary_email]
                nums = [user.b_branch_code, user.b_sheba_num, user.b_card_num, user.b_acount_num, user.id_num,
                        user.business_license_num, user.fax, user.phone, user.mobile]
                bools = [user.mobile_is_varified, user.email_is_activated, user.secondary_email_is_activated,
                         user.b_complete, user.b_varified]
                for text in texts:
                    if text != '':
                        complete_percentage1 += 3
                for num in nums:
                    if num != 0:
                        complete_percentage1 += 3
                for bool in bools:
                    if bool != 0:
                        complete_percentage1 += 3
                complete_percentage = round_to_five(complete_percentage1)
                user.complete_percentage = complete_percentage
                user.save()
                if request.POST['union'] != 'other' and request.POST['union'] != '':
                    union2 = Union.objects.get(value=request.POST['union'])
                    union2.used_num += 1
                    union2.save()
                elif request.POST['union'] == 'other' and request.POST['union'] != '':
                    try:
                        union2 = Union.objects.get(name=str(request.POST['other_union']))
                        pass
                    except:
                        union2 = Union(name=str(request.POST['other_union']), value=str(request.POST['other_union']), used_num=0, approved=False)
                        union2.save()
                if request.POST['job_category'] != 'other' and request.POST['job_category'] != '':
                    job_category2 = JobCategory.objects.get(value=request.POST['job_category'])
                    job_category2.used_num += 1
                    job_category2.save()
                elif request.POST['job_category'] == 'other' and request.POST['job_category'] != '':
                    try:
                        job_category2 = union2.jobcategory_set.get(name=str(request.POST['other_job_category']))
                        pass
                    except:
                        job_category2 = union2.jobcategory_set.create(name=str(request.POST['other_job_category']), value=str(request.POST['other_job_category']), used_num=0, approved=False)
                        job_category2.save()
                if request.POST['city'] != '':
                    city1 = City.objects.get(name=request.POST['city'])
                    city1.used_num += 1
                    city1.save()
                if request.POST['state'] != '':
                    state1 = State.objects.get(name=request.POST['state'])
                    state1.used_num += 1
                    state1.save()
                if mobileTemp != '0' and user.mobile_is_varified == 0:
                    try:
                        user3 = PermanentlyInfo.objects.get(mobile=mobileTemp)
                        if user3.mobile_is_varified == 1:
                            request.session['earlierFill'] = True
                            return render(request, 'signupapp/ok_in.html', {'message': 'شماره ی موبایل {} قبلا در سامانه سجام ثبت و فعال شده است'.format(str(mobileTemp),), 'from': 'bad_cip', 'user': user})
                        else:
                            sms_message = 'کد تایید سجام' + '\n' + str(user.user_phone_varification_number) + '\n' + 'wWw.SamanehEstelam.Org' + '\n' + 'سامانه جامع استعلام مشتریان'
                            sms = send_sms(user.mobile, sms_message)
                            if sms == False:
                                request.session['earlierFill'] = True
                                return render(request, 'signupapp/ok_in.html', {
                            'message': 'شماره موبایل وارد شده صحیح نیست. در صورت تمایل شماره موبایل صحیح و فعال خود را وارد کنید و در غیر اینصورت، آن را برابر صفر قرار دهید',
                            'from': 'bad_cip'})
                            else:
                                request.session['postTemp'] = None
                                request.session['earlierFill'] = False
                                return render(request, 'signupapp/get_phone_validation_code.html', {'user': user})
                    except:
                        sms_message = 'کد تایید سجام' + '\n' + str(
                            user.user_phone_varification_number) + '\n' + 'wWw.SamanehEstelam.Org' + '\n' + 'سامانه جامع استعلام مشتریان'
                        sms = send_sms(user.mobile, sms_message)
                        if sms == False:
                            request.session['earlierFill'] = True
                            return render(request, 'signupapp/ok_in.html', {
                                'message': 'شماره موبایل وارد شده صحیح نیست. در صورت تمایل شماره موبایل صحیح و فعال خود را وارد کنید و در غیر اینصورت، آن را برابر صفر قرار دهید',
                                'from': 'bad_cip'})
                        else:
                            request.session['postTemp'] = None
                            request.session['earlierFill'] = False
                            return render(request, 'signupapp/get_phone_validation_code.html', {'user': user})
                request.session['postTemp'] = None
                request.session['earlierFill'] = False
                return HttpResponseRedirect('/uprofile/')
            except:
                request.session['postTemp'] = None
                request.session['earlierFill'] = False
                return render(request, 'signupapp/ok_in.html',
                              {'message': error_message, 'from': 'bad_entry_signup', 'user': user})


def vumn(request):  # Validate User Mobile Number
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin/')
    else:
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if request.POST:
            entered_code = int(request.POST['validation_code'])
            validation_code = user.user_phone_varification_number
            if str(entered_code) == str(validation_code):
                user.mobile_is_varified = True
                user.user_phone_varification_number == 0
                user.save()
                return render(request, 'signupapp/ok_in.html',
                              {'message': 'شماره موبایل {} با موفقیت فعال شد'.format(user.mobile, ), 'from': 'vumn',
                               'user': user})
            else:
                return render(request, 'signupapp/ok_in.html',
                              {'message': str(validation_code), 'from': 'bad_vumn', 'user': user})
        else:
            if user.mobile_is_varified == False:
                return HttpResponseRedirect('/uprofile/cip/')
            else:
                return HttpResponseRedirect('/uprofile/')


def ci_bank(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin/')
    else:
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if request.POST:
            try:
                user.b_name = request.POST['b_name']
                user.b_branch_name = request.POST['b_branch_name']
                user.b_branch_code = request.POST['b_branch_code']
                user.b_acount_num = request.POST['b_acount_num']
                user.b_card_num = request.POST['b_card_num']
                user.b_sheba_num = request.POST['b_sheba_num']
                user.save()
                return HttpResponseRedirect('/uprofile/')
            except:
                return render(request, 'signupapp/ok_in.html',
                              {'message': error_message, 'from': 'bad_entry_signup', 'user': user})
        else:
            return render(request, 'signupapp/ci_bank_page.html', {'user': user})


def se(request, user_id):  # Send E-mail
    if request.user.is_authenticated():
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(id=user_id)
        if user.secondary_email != "":
            mail_message = "کاربر گرامی\n\nلطفا از لینک زیر برای فعال سازی ایمیل دوم خود در سامانه ی سجام استفاده نمایید:\n\nhttp://www.samanehestelam.com/aaa/{}\n\nبا تشکر\nسیستم جامع استعلام مشتریان = سجام\nآدرس سایت:\nwWw.SamanehEstelam.Org".format(str(user.user_secondary_email_activation_link))
#            user_mail_func = send_email('samaneestelam@gmail.com', '0okmnji98U', [str(user.secondary_email)], message)
            send_mail('تایید ایمیل دوم در سامانه سجام', mail_message, 'info@samanehestelam.org', [str(user.secondary_email)], fail_silently=False)
            return render(request, 'signupapp/ok_in.html',
                          {'message': 'ایمیل تایید به {} فرستاده شد'.format(str(user.secondary_email), ),
                           'from': 'send_email', 'user': user})
        else:
            return HttpResponseRedirect('/uprofile/pci/')
    else:
        return HttpResponseRedirect('/dologin/')


def srr(request):  # USELESS
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin')
    else:
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        records = PermanentlyInfo.objects.get(username=request.user.username).registeredrecords_set.all()
        return render(request, 'signupapp/show_records.html', {'customer': records, 'from': 'srr'})


def er(request, given_record_link):  # Edit a Record
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin/')
    else:
        user = PermanentlyInfo.objects.get(username=request.user.username)
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        try:
            record = NoncreditworthyInfo.objects.get(record_link=given_record_link)
            record1 = RegisteredRecords.objects.get(record_link=given_record_link)
            dds = user.debtdocument_set.all()
            if request.POST:
                try:
                    record.debt_amount = request.POST['debt_amount']
                    record.debt_kind = request.POST['debt_kind']
                    #                record.debt_start_date = request.POST['debt_start_date']
                    record.debt_start_date = request.POST['debt_start_date_year'] + '-' + request.POST[
                        'debt_start_date_month'] + '-' + request.POST['debt_start_date_day']
                    #                record.debt_due_date = request.POST['debt_due_date']
                    record.debt_due_date = request.POST['debt_due_date_year'] + '-' + request.POST[
                        'debt_due_date_month'] + '-' + request.POST['debt_due_date_day']
                    #                record.debt_clearance_date = request.POST['debt_clearance_date']
                    if 'debt_cleared' in request.POST:
                        record.debt_clearance_date = request.POST['debt_clearance_date_year'] + '-' + request.POST[
                            'debt_clearance_date_month'] + '-' + request.POST['debt_clearance_date_day']
                    record.about = request.POST['about']
                    record1.debt_amount = request.POST['debt_amount']
                    record1.debt_kind = request.POST['debt_kind']
                    #                record1.debt_start_date = request.POST['debt_start_date']
                    record1.debt_start_date = request.POST['debt_start_date_year'] + '-' + request.POST[
                        'debt_start_date_month'] + '-' + request.POST['debt_start_date_day']
                    #                record1.debt_due_date = request.POST['debt_due_date']
                    record1.debt_due_date = request.POST['debt_due_date_year'] + '-' + request.POST[
                        'debt_due_date_month'] + '-' + request.POST['debt_due_date_day']
                    record1.proof_for_debt = request.POST['proof_for_debt']
                    #                record1.debt_clearance_date = request.POST['debt_clearance_date']
                    if 'debt_cleared' in request.POST:
                        record1.debt_clearance_date = request.POST['debt_clearance_date_year'] + '-' + request.POST[
                            'debt_clearance_date_month'] + '-' + request.POST['debt_clearance_date_day']
                    if request.POST['about'] != '':
                        record1.about = request.POST['about']
                    if 'debt_cleared' in request.POST:
                        record.debt_cleared = True
                        record1.debt_cleared = True
                    else:
                        record.debt_cleared = False
                        record1.debt_cleared = False
                    if record.proof_for_debt != request.POST['proof_for_debt']:
                        old_debt_document = user.debtdocument_set.get(value=record.proof_for_debt)
                        old_debt_document.used_num -= 1
                        old_debt_document.save()
                        record.proof_for_debt = request.POST['proof_for_debt']
                    record.save()
                    record1.save()
                    return HttpResponseRedirect('/uprofile/')
                except:
                    return render(request, 'signupapp/ok_in.html',
                                  {'message': error_message, 'from': 'bad_entry_signup', 'user': user})
            else:
                return render(request, 'signupapp/edit_a_record.html', {'record': record, 'from': 'ear', 'user': user})
        except:
            return render(request, 'signupapp/ok_in.html',
                          {'message': 'گزارش مورد نظر موجود نیست', 'from': 'failed_er', 'user': user})


def rr(request, given_record_link):  # Remove a Customer
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin/')
    else:
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        try:
            record = NoncreditworthyInfo.objects.get(record_link=given_record_link)
            record1 = RegisteredRecords.objects.get(record_link=given_record_link)
            debt_document = user.debtdocument_set.get(value=record.proof_for_debt)
            debt_document.used_num -= 1
            debt_document.save()
            record.delete()
            record1.delete()
            return HttpResponseRedirect('/uprofile/')
        except:
            return render(request, 'signupapp/ok_in.html',
                          {'message': 'گزارش مورد نظر موجود نیست', 'from': 'failed_rr', 'user': user})


def ec(request, given_customer_link):  # Edit a Customer
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin/')
    else:
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        try:
            customer = CustomerInfo.objects.get(customer_link=given_customer_link)
            if request.POST:
                try:
                    request.session['ecPostTemp'] = request.POST
                    request.session['ecEarlierFill'] = True
                    customer.father_name = request.POST['father_name']
                    customer.gender = request.POST['gender']
                    if int(request.POST['id_num']) != 0 and str(customer.id_num) != str(int(request.POST['id_num'])):
                        try:
                            old_customer = CustomerInfo.objects.get(id_num=request.POST['id_num'])
                            return render(request, 'signupapp/edit_a_customer.html',
                                          {'customer': customer, 'user': user, 'session': request.session,
                                           'error_message': 'کد ملی {} قبلا در سامانه ثبت شده است'.format(
                                               request.POST['id_num'])})
                        except:
                            customer.id_num = request.POST['id_num']
                    customer.relative_id_num = request.POST['relative_id_num']
                    customer.relativity = request.POST['relativity']
                    customer.job = request.POST['job']
                    if request.POST['about'] != '':
                        customer.about = request.POST['about']
                    customer.save()
                    request.session['ecEarlierFill'] = False
                    request.session['ecPostTemp'] = None
                    return HttpResponseRedirect('/uprofile/')
                except:
                    request.session['ecEarlierFill'] = False
                    request.session['ecPostTemp'] = None
                    return render(request, 'signupapp/ok_in.html',
                                  {'message': error_message, 'from': 'bad_entry_signup', 'user': user})
            else:
                request.session['ecEarlierFill'] = False
                request.session['ecPostTemp'] = None
                return render(request, 'signupapp/edit_a_customer.html',
                              {'customer': customer, 'user': user, 'session': request.session})
        except:
            return render(request, 'signupapp/ok_in.html',
                          {'message': 'کاربر مورد نظر موجود نیست', 'from': 'failed_er', 'user': user})


def add_debt_document(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin/')
    else:
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if request.POST:
            try:
                user_dd = user.debtdocument_set.create(name=request.POST['dd_name'], used_num=0)
                user_dd.value = 'extra_dd_' + str(user_dd.id)
                user_dd.save()
                return HttpResponseRedirect('/uprofile/add')
            except:
                return render(request, 'signupapp/ok_in.html',
                              {'message': error_message, 'from': 'bad_entry_signup', 'user': user})
        else:
            dds = user.debtdocument_set.all()
            num = len(dds)
            return render(request, 'signupapp/add_debt_document.html',
                          {'dds': dds, 'num1': num + 1, 'num2': num + 2, 'user': user})


def remove_debt_document(request, dd_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin/')
    else:
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        try:
            user_dd = user.debtdocument_set.get(id=dd_id)
            if user_dd.used_num == 0:
                user_dd.delete()
                return HttpResponseRedirect('/uprofile/add/')
            else:
                return render(request, 'signupapp/ok_in.html', {
                    'message': 'نوع سند {} در حال استفاده است و امکان حذف آن وجود ندارد'.format(str(user_dd.name), ),
                    'from': 'in_use_rdd', 'user': user})
        except:
            return HttpResponseRedirect('/uprofile/add/')


def euprofile(request):  # Edit UProfile
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin/')
    else:
        request.session['last_touch'] = khayyam.JalaliDatetime.now()
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if request.POST:
            try:
                user.phone = request.POST['phone']
                user.fax = request.POST['fax']
                user.address = request.POST['address']
                if request.POST['about'] != '':
                    user.about = request.POST['about']
                user.save()
                return HttpResponseRedirect('/uprofile/')
            except:
                return render(request, 'signupapp/ok_in.html',
                              {'message': error_message, 'from': 'bad_entry_signup', 'user': user})
        else:
            return render(request, 'signupapp/edit_profile.html', {'user': user})


def au(request):  # Acount Upgrade
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin/')
    else:
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if acount_upgrade == True:
            request.session['last_touch'] = khayyam.JalaliDatetime.now()
            return render(request, 'signupapp/acount_upgrade_page.html', {'user': user})
        else:
            return render(request, 'signupapp/ok_in.html',
                          {'message': 'در حال حاضر این صفحه در دسترس نمی باشد', 'from': 'fau', 'user': user})


def acb(request):  # Acount Check Bronze
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin/')
    else:
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if acount_upgrade == True:
            if user.certified == 1:
                request.session['last_touch'] = khayyam.JalaliDatetime.now()
                user.acount_type = 'bronze'
                user.acount_upgrade_date = khayyam.JalaliDatetime.now().date()
                user.save()
                return HttpResponseRedirect('/')
            else:
                return render(request, 'signupapp/ok_in.html',
                              {'message': 'به دلیل عدم تایید هویت حقوقی، این حساب کاربری قابل ارتقاء نمی باشد',
                               'from': 'failed_ac', 'user': user})
        else:
            return render(request, 'signupapp/ok_in.html',
                          {'message': 'در حال حاضر این صفحه در دسترس نمی باشد', 'from': 'fau', 'user': user})


def acs(request):  # Acount Check Silver
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin/')
    else:
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if acount_upgrade == True:
            if user.certified == 1:
                request.session['last_touch'] = khayyam.JalaliDatetime.now()
                user.acount_type = 'silver'
                user.acount_upgrade_date = khayyam.JalaliDatetime.now().date()
                user.save()
                return HttpResponseRedirect('/')
            else:
                return render(request, 'signupapp/ok_in.html',
                              {'message': 'به دلیل عدم تایید هویت حقوقی، این حساب کاربری قابل ارتقاء نمی باشد',
                               'from': 'failed_ac', 'user': user})
        else:
            return render(request, 'signupapp/ok_in.html',
                          {'message': 'در حال حاضر این صفحه در دسترس نمی باشد', 'from': 'fau', 'user': user})


def acg(request):  # Acount Check Gold
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/dologin/')
    else:
        user = PermanentlyInfo.objects.get(username=request.user.username)
        if acount_upgrade == True:
            if user.certified == 1:
                request.session['last_touch'] = khayyam.JalaliDatetime.now()
                user.acount_type = 'gold'
                user.acount_upgrade_date = khayyam.JalaliDatetime.now().date()
                user.save()
                return HttpResponseRedirect('/')
            else:
                return render(request, 'signupapp/ok_in.html',
                              {'message': 'به دلیل عدم تایید هویت حقوقی، این حساب کاربری قابل ارتقاء نمی باشد',
                               'from': 'failed_ac', 'user': user})
        else:
            return render(request, 'signupapp/ok_in.html',
                          {'message': 'در حال حاضر این صفحه در دسترس نمی باشد', 'from': 'fau', 'user': user})


def rules(request):
    if not request.user.is_authenticated():
        return render(request, 'signupapp/rules_page_out.html', {})
    else:
        user = PermanentlyInfo.objects.get(username=request.user.username)
        return render(request, 'signupapp/rules_page_in.html', {'user': user})


def sms_dig(request):
#    if not request.GET:
#        return HttpResponseRedirect('/')
#    else:
#        try:
#            user = PermanentlyInfo.objects.get(mobile=request.GET['FROM'])
#            if user.mobile_is_varified == 1:
#                customer = CustomerInfo.objects.get(id_num=request.GET['TEXT'])
#                customer.searched_num += 1
#                customer_records = customer.noncreditworthyinfo_set.all()
#                records = [record for record in customer_records if record.debt_cleared == 0]
#                for record in records:
#                    if str(record.debt_start_date) > str(record.debt_due_date):
#                        record.gone_bad = True
#                    else:
#                        record.gone_bad = False
#                    record.save()
#                amount = 0
#                if len(records) != 0:
#                    for record in records:
#                        amount += int(record.debt_amount)
#                    amount = amount // len(records)
#                amount = round(amount, -3)
#                if len(records) == 0:
#                    first_part = 'بدهی ثبت شده برای این کاربر وجود ندارد'
#                elif len(records) == 1:
#                    first_part = 'یک مورد بدهی ثبت شده با مبلغ {} تومان'.format(str(amount), )
#                else:
#                    first_part = '{} بدهی ثبت شده با میانگین مبلغ {} تومان'.format(str(len(records)), str(amount))
#                bad_records = [record for record in customer_records if
#                               record.debt_cleared == 0 and record.gone_bad == 1]
#                bad_amount = 0
#                bad_average_date = 0
#                if len(bad_records) != 0:
#                    for record in bad_records:
#                        bad_amount += int(record.debt_amount)
#                    bad_amount = bad_amount // len(bad_records)
#                    bad_amount = round(bad_amount, -3)
#                    bad_month2 = [(khayyam.JalaliDatetime.now().date() - record.debt_due_date).days // 30 for record in bad_records]
#                    bad_month1 = 0
#                    for bms in bad_month2: bad_month1 += bms
#                    bad_average_date = bad_month1 // len(bad_month2)
#                if len(bad_records) == 0:
#                    second_part = 'تاخیر در پرداخت برای این فرد وجود ندارد'
#                elif len(bad_records) == 1:
#                    second_part = 'یک مورد بدهی دارای تاخیر با مبلغ {} تومان و تاخیر {} ماه'.format(str(bad_amount),
#                                                                                                    str(
#                                                                                                        bad_average_date))
#                else:
#                    second_part = ''.format(str(len(bad_records)), str(bad_amount), str(bad_average_date))
#                if user.acount_type == "base" or user.acount_type == "silver":
#                    message = "استعلام کاربر با کد ملی {}".format(str(customer.id_num), ) + "\n" + str(
#                        customer.first_name) + " " + str(customer.last_name) + "\n" + first_part + "\n" + second_part
#                else:
#                    message = "استعلام کاربر با کد ملی {}".format(str(customer.id_num), ) + "\n" + str(
#                        customer.first_name) + " " + str(
#                        customer.last_name) + "\n" + first_part + "\n" + second_part + "\n" + "استان {} و صنف {}".format(
#                        customer.state, customer.job)
#                send_sms(request.GET['from'], message)
#            else:
#                send_sms(request.GET['from'], 'این شماره در سیستم سجام فعال نشده است')
#        except:
    send_sms(request.GET['from'], 'این شماره در سیستم سجام فعال نشده است')


def sie(request):  # Send Info Email
    if not request.POST:
        return HttpResponseRedirect('/')
    else:
        mail_message = request.POST['message'] + "\n\n\n" + "from:" + "\n" + request.POST['name'] + "\n" + request.POST[
            'email']
#        mail = send_email('samaneestelam@gmail.com', '0okmnji98U', ['samaneestelam@gmail.com'], message)
        send_mail('تماس با ما', mail_message, 'info@samanehestelam.org',
                  ['info@samanehestelam.org'], fail_silently=False)
        if request.user.is_authenticated():
            user = PermanentlyInfo.objects.get(username=request.user.username)
            return render(request, 'signupapp/ok_in.html', {
                'message': 'ایمیل با موفقیت فرستاده شد. پاسخ شما در اسرع وقت به {} فرستاده خواهد شد'.format(
                    str(request.POST['email']), ), 'from': 'sie', 'user': user})
        else:
            return render(request, 'signupapp/ok_out.html', {
                'message': 'ایمیل با موفقیت فرستاده شد. پاسخ شما در اسرع وقت به {} فرستاده خواهد شد'.format(
                    str(request.POST['email']), ), 'from': 'sie'})


def social_statistics_go(request, social_name):
    name = social_name
    if name == 'facebook':
        sm = Statistics.objects.get(name=name)
        sm.went_to += 1
        sm.save()
        return HttpResponseRedirect('https://facebook.com/samane.estelam')
    elif name == 'twitter':
        sm = Statistics.objects.get(name=name)
        sm.went_to += 1
        sm.save()
        return HttpResponseRedirect('https://twitter.com/samane.estelam')
    elif name == 'telegram':
        sm = Statistics.objects.get(name=name)
        sm.went_to += 1
        sm.save()
        return HttpResponseRedirect('/')
    elif name == 'gplus':
        sm = Statistics.objects.get(name=name)
        sm.went_to += 1
        sm.save()
        return HttpResponseRedirect('https://plus.google.com/u/0/106721263188422742225')
    elif name == 'youtube':
        sm = Statistics.objects.get(name=name)
        sm.went_to += 1
        sm.save()
        return HttpResponseRedirect('/')
    elif name == 'instagram':
        sm = Statistics.objects.get(name=name)
        sm.went_to += 1
        sm.save()
        return HttpResponseRedirect('/')
    elif name == 'aparat':
        sm = Statistics.objects.get(name=name)
        sm.went_to += 1
        sm.save()
        return HttpResponseRedirect('/')
    elif name == 'lenzor':
        sm = Statistics.objects.get(name=name)
        sm.went_to += 1
        sm.save()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def social_statistics_come(request, social_name):
    name = social_name
    if name == 'facebook':
        sm = Statistics.objects.get(name=name)
        sm.came_from += 1
        sm.save()
        return HttpResponseRedirect('/')
    elif name == 'twitter':
        sm = Statistics.objects.get(name=name)
        sm.came_from += 1
        sm.save()
        return HttpResponseRedirect('/')
    elif name == 'telegram':
        sm = Statistics.objects.get(name=name)
        sm.came_from += 1
        sm.save()
        return HttpResponseRedirect('/')
    elif name == 'gplus':
        sm = Statistics.objects.get(name=name)
        sm.came_from += 1
        sm.save()
        return HttpResponseRedirect('/')
    elif name == 'youtube':
        sm = Statistics.objects.get(name=name)
        sm.came_from += 1
        sm.save()
        return HttpResponseRedirect('/')
    elif name == 'instagram':
        sm = Statistics.objects.get(name=name)
        sm.came_from += 1
        sm.save()
        return HttpResponseRedirect('/')
    elif name == 'aparat':
        sm = Statistics.objects.get(name=name)
        sm.came_from += 1
        sm.save()
        return HttpResponseRedirect('/')
    elif name == 'lenzor':
        sm = Statistics.objects.get(name=name)
        sm.came_from += 1
        sm.save()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def test(request):
    if not request.POST:
        return render(request, 'signupapp/test.html', {})
    else:
        if request.POST['test'] == 'test2':
            return HttpResponseRedirect('/test/#test2')
