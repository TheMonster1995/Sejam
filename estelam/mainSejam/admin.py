from django.contrib import admin

# Register your models here.

from .models import TemporaryInfo, PermanentlyInfo, CustomerInfo, NoncreditworthyInfo, RegisteredRecords, JobCategory, Union, State, City, DebtDocument

admin.site.register(JobCategory)
admin.site.register(Union)
admin.site.register(City)

class DebtDocuments (admin.TabularInline):
    model = DebtDocument
    extra = 0

class RegisteredCustomers (admin.TabularInline):
    model = CustomerInfo
    extra = 0

class RegisteredRecordss (admin.TabularInline):
    model = RegisteredRecords
    extra = 0

class SejamAdminUser(admin.ModelAdmin):
    fieldsets = [
        ('اطلاعات فردی', {'fields': ['id_num', 'first_name', 'last_name', 'father_name', 'birthday', 'gender', 'phone', 'mobile', 'fax', ], 'classes': ['collapse']}),
        ('اطلاعات حقوقی', {'fields': ['brand', 'union', 'job_category', 'business_license_num', 'business_license_due_date', 'state', 'city', 'address', ], 'classes': ['collapse']}),
        ('اطلاعات حساب بانکی', {'fields': ['b_name', 'b_branch_name', 'b_branch_code', 'b_acount_num', 'b_card_num', 'b_sheba_num', ], 'classes': ['collapse']}),
        ('اطلاعات حساب کاربری', {'fields': ['username', 'email', 'secondary_email', 'password', 'signup_date', 'registered_records_num', 'day_search', 'last_search_date', 'complete_percentage', 'acount_upgrade_date', 'about', ], 'classes': ['collapse']}),
        ('لینک ها و تاییدیه ها', {'fields': ['first_log_in', 'mobile_is_varified', 'b_complete', 'b_varified', 'email_is_activated', 'secondary_email_is_activated', 'info_complete', 'is_complete', 'complete_percentage', 'certified', 'deleted', 'user_certification_link', 'user_email_activation_link', 'user_secondary_email_activation_link', 'user_phone_varification_number', 'user_pass_reset_link', ], 'classes': ['collapse']}),
    ]
    inlines = [RegisteredCustomers, RegisteredRecordss, DebtDocuments]

admin.site.register(PermanentlyInfo, SejamAdminUser)

class BadRecords (admin.TabularInline):
    model = NoncreditworthyInfo
    extra = 0

class SejamAdminCustomer (admin.ModelAdmin):
    fieldsets = [
        ('اطلاعات فردی', {'fields':['first_name', 'last_name', 'father_name', 'id_num', 'gender', 'relative_id_num', 'relativity', 'about'], 'classes':['collapse']}),
        ('اطلاعات حقوقی', {'fields':['state', 'city', 'job' ], 'classes':['collapse']}),
        ('اطلاعات حساب کاربری', {'fields':['relation', 'registered_records_num', 'registered_late_records_num', 'searched_num', 'customer_link' ], 'classes':['collapse']}),
    ]
    inlines = [BadRecords]

admin.site.register(CustomerInfo, SejamAdminCustomer)

class SejamAdminRecord (admin.ModelAdmin):
    fieldsets = [
        ('اطلاعات گزارش', {'fields':['relation', 'registered_by_id', 'register_date', 'debt_amount', 'debt_kind', 'proof_for_debt', 'debt_start_date', 'debt_due_date', 'debt_cleared', 'debt_clearance_date', 'about', 'gone_bad', 'record_link'], 'classes':['collapse']}),
    ]

admin.site.register(NoncreditworthyInfo, SejamAdminRecord)

class Cities (admin.TabularInline):
    model = City
    extra = 0

class SejamAdminState (admin.ModelAdmin):
    fieldsets = [
    ('اطلاعات استان', {'fields': ['name', 'value', 'used_num'], 'classes': ['collapse']}),
    ]
    inlines = [Cities]

admin.site.register(State, SejamAdminState)
