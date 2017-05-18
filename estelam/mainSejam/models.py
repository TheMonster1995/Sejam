from django.db import models


# Create your models here.

class TemporaryInfo(models.Model):
    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + str(self.id_num)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    mobile = models.BigIntegerField()
    fax = models.BigIntegerField()
    id_num = models.BigIntegerField()
    job_category = models.CharField(max_length=100)
    union = models.CharField(max_length=100)
    business_license_num = models.BigIntegerField()
    father_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    brand = models.CharField(max_length=200)
    birthday = models.DateField(auto_now=False)
    gender = models.CharField(max_length=10)
    signup_date = models.DateTimeField(auto_now=False)
    business_license_due_date = models.DateField(auto_now=False)
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    registered_records_num = models.IntegerField()
    about = models.TextField()
    certified = models.BooleanField(default=False)
    certify_link = models.CharField(max_length=30)
    first_log_in = models.BooleanField(default=False)


class PermanentlyInfo(models.Model):
    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + str(self.id_num)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    mobile = models.BigIntegerField()
    mobile_is_varified = models.BooleanField(default=False)
    fax = models.BigIntegerField()
    id_num = models.BigIntegerField()
    job_category = models.CharField(max_length=100)
    union = models.CharField(max_length=100)
    business_license_num = models.BigIntegerField()
    father_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    brand = models.CharField(max_length=200)
    birthday = models.DateField(auto_now=False)
    gender = models.CharField(max_length=10)
    signup_date = models.DateTimeField(auto_now=False)
    business_license_due_date = models.DateField(auto_now=False)
    b_name = models.CharField(max_length=100)  # Bank name
    b_branch_name = models.CharField(max_length=100)
    b_branch_code = models.CharField(max_length=100)
    b_acount_num = models.BigIntegerField()
    b_card_num = models.BigIntegerField()
    b_sheba_num = models.CharField(max_length=50)
    b_complete = models.BooleanField(default=False)
    b_varified = models.BooleanField(default=False)
    email = models.EmailField(max_length=254)
    email_is_activated = models.BooleanField(default=False)
    secondary_email = models.EmailField(max_length=254)
    secondary_email_is_activated = models.BooleanField(default=False)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    registered_records_num = models.IntegerField()
    about = models.TextField()
    last_edit = models.DateField(auto_now=False)
    last_sync = models.DateField(auto_now=False)
    user_certification_link = models.CharField(max_length=30)
    user_email_activation_link = models.CharField(max_length=30)
    user_secondary_email_activation_link = models.CharField(max_length=30)
    user_phone_varification_number = models.IntegerField()
    user_pass_reset_link = models.CharField(max_length=30)
    certified = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    info_complete = models.BooleanField(default=False)
    day_search = models.IntegerField()
    last_search_date = models.DateField(auto_now=False)
    complete_percentage = models.IntegerField()
    deleted = models.BooleanField(default=False)
    acount_type = models.CharField(max_length=10, default="base")
    acount_upgrade_date = models.DateField(auto_now=False)
    gone_bad_records = models.BigIntegerField()
    first_log_in = models.BooleanField(default=False)


class CustomerInfo(models.Model):
    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + str(self.id_num)

    relation = models.ForeignKey(PermanentlyInfo)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    id_num = models.BigIntegerField()
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    registered_records_num = models.IntegerField()
    registered_late_records_num = models.IntegerField()
    relative_id_num = models.BigIntegerField()
    relativity = models.CharField(max_length=100)
    searched_num = models.IntegerField()
    about = models.TextField()
    customer_link = models.CharField(max_length=20)


class NoncreditworthyInfo(models.Model):
    def __str__(self):
        return str(self.relation.first_name) + ' ' + str(self.relation.last_name) + ' ' + str(
            self.relation.id_num) + ' ' + str(self.id)

    relation = models.ForeignKey(CustomerInfo)
    register_date = models.DateField(auto_now=False)
    debt_amount = models.BigIntegerField()
    registered_by_id = models.BigIntegerField()
    debt_kind = models.CharField(max_length=30)
    debt_start_date = models.DateField(auto_now=False)
    debt_due_date = models.DateField(auto_now=False)
    proof_for_debt = models.CharField(max_length=30)
    debt_cleared = models.BooleanField(default=False)
    debt_clearance_date = models.DateField(auto_now=False)
    about = models.TextField()
    gone_bad = models.BooleanField(default=False)
    record_link = models.CharField(max_length=30)


class RegisteredRecords(models.Model):
    def __str__(self):
        return str(self.id)

    relation = models.ForeignKey(PermanentlyInfo)
    customer_id = models.BigIntegerField()
    customer_id_num = models.BigIntegerField()
    customer_first_name = models.CharField(max_length=100)
    customer_last_name = models.CharField(max_length=100)
    register_date = models.DateField(auto_now=False)
    debt_amount = models.BigIntegerField()
    registered_by_id = models.BigIntegerField()
    debt_kind = models.CharField(max_length=30)
    debt_start_date = models.DateField(auto_now=False)
    debt_due_date = models.DateField(auto_now=False)
    proof_for_debt = models.CharField(max_length=30)
    debt_cleared = models.BooleanField(default=False)
    debt_clearance_date = models.DateField(auto_now=False)
    about = models.TextField()
    gone_bad = models.BooleanField(default=False)
    record_link = models.CharField(max_length=30)


class DebtDocument(models.Model):  # Also known as debt proof or proof for debt

    def __str__(self):
        return str(self.id) + ' ' + str(self.name)

    relation = models.ForeignKey(PermanentlyInfo)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    used_num = models.BigIntegerField()


class Union(models.Model):
    def __str__(self):
        return str(self.name)

    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    used_num = models.BigIntegerField()
    approved = models.BooleanField(default=False)


class JobCategory(models.Model):
    def __str__(self):
        return str(self.name)

    relation = models.ForeignKey(Union)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    used_num = models.BigIntegerField()
    approved = models.BooleanField(default=False)


class State(models.Model):
    def __str__(self):
        return str(self.name)

    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    used_num = models.BigIntegerField()


class City(models.Model):
    def __str__(self):
        return str(self.name)

    relation = models.ForeignKey(State)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    used_num = models.BigIntegerField()


class Statistics(models.Model):
    def __str__(self):
        return str(self.name) + ' ' + str(self.came_from) + ' ' + str(self.went_to)

    name = models.CharField(max_length=100)
    came_from = models.BigIntegerField()
    went_to = models.BigIntegerField()