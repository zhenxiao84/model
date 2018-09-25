from django.db import models

class Request(models.Model):
    request_id = models.CharField(max_length=127, primary_key=True)
    model_name = models.CharField(max_length=127, db_index=True)
    customer_id = models.IntegerField(db_index=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)

