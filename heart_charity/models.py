from django.db import models



class Volunteer(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=50, null=True, blank=True)
    phone=models.CharField(max_length=12, null=True, blank=True)
    gender=models.CharField(max_length=6,null=True, blank=True)
    dob=models.DateField( null=True, blank=True)
    subject=models.CharField(max_length=30)
    message=models.TextField()

    def __str__(self):
        return self.name
    
class Contact(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=50, null=True, blank=True)
    message=models.TextField()

    def __str__(self):
        return self.name


class Cause(models.Model):
    name = models.CharField(max_length=30)
    img = models.ImageField(upload_to='causes/', null=True, blank=True)  # Store cause images in a separate folder
    detail = models.CharField(max_length=500)
    raised = models.FloatField()
    goal = models.FloatField()

    def __str__(self):
        return self.name

class Donate(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, null=True, blank=True)
    amount = models.FloatField()
    photo = models.ImageField(upload_to='donors/', blank=True, null=True)  # Photo field for donor images
    cause = models.ForeignKey(Cause, on_delete=models.CASCADE)  # Link donation to a cause

    def __str__(self):
        return f"{self.name} - {self.cause.name}"
    
class Person(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    disability_type = models.CharField(max_length=30, null=True, blank=True)
    dis_percentage = models.CharField(max_length=3, null=True, blank=True)
    udid_no = models.CharField(max_length=18, null=True, blank=True)
    aadhaar_no = models.CharField(max_length=16, null=True, blank=True)
    age = models.CharField(max_length=3, null=True, blank=True)
    gender = models.CharField(max_length=6, null=True, blank=True)
    dependent = models.CharField(max_length=300, null=True, blank=True)
    occupation = models.CharField(max_length=30, null=True, blank=True)
    salary = models.CharField(max_length=10, null=True, blank=True)
    it_return = models.CharField(max_length=10, null=True, blank=True)
    date_registered = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return self.name
    
    def mask_phone(self):
        if self.phone and len(self.phone) >= 4:
            return f"xxxxxx{self.phone[-4:]}"
        return "Null"  # Default masking if the phone number is missing or too short

    def mask_udid(self):
        if self.udid_no and len(self.udid_no) >= 4:
            return f"xxxx-xxxx-xx-{self.udid_no[-4:]}"
        return "Null"  # Default masking if UDID is missing or too short

    def mask_aadhaar(self):
        if self.aadhaar_no and len(self.aadhaar_no) >= 4:
            return f"xxxx-xxxx-{self.aadhaar_no[-4:]}"
        return "Null"  # Default masking if Aadhaar is missing or too short
    

class work(models.Model):
    name=models.CharField(max_length=30)
    img=models.ImageField()
    detail=models.CharField(max_length=500)

    def __str__(self):
        return self.name
    

# class Donations(models.Model):
#     name=models.CharField(max_length=30)
#     email=models.EmailField(max_length=30)
#     photo = models.ImageField(upload_to='donors/', null=True, blank=True)
#     amount=models.FloatField()

#     def __str__(self):
#         return self.name
    

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name

class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.event.name}"

        
        