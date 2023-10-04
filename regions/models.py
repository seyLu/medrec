from django.db import models


class Region(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=["code"], name="region_code_idx"),
        ]

    def __str__(self):
        return f"{self.name}, {self.code}"


class Province(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    region_code = models.ForeignKey(
        Region, to_field="code", on_delete=models.CASCADE, default="0800000000"
    )

    class Meta:
        indexes = [
            models.Index(fields=["code"], name="province_code_idx"),
        ]

    def __str__(self):
        return f"{self.name}, {self.code}"


class City(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    province_code = models.ForeignKey(
        Province, to_field="code", on_delete=models.CASCADE, default="0831600000"
    )
    region_code = models.ForeignKey(
        Region, to_field="code", on_delete=models.CASCADE, default="0800000000"
    )

    class Meta:
        indexes = [
            models.Index(fields=["code"], name="city_code_idx"),
        ]

    def __str__(self):
        return f"{self.name}, {self.code}"


class District(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    city_code = models.ForeignKey(
        City, to_field="code", on_delete=models.CASCADE, default="0831600000"
    )
    province_code = models.ForeignKey(
        Province, to_field="code", on_delete=models.CASCADE, default="0831600000"
    )
    region_code = models.ForeignKey(
        Region, to_field="code", on_delete=models.CASCADE, default="0800000000"
    )

    class Meta:
        indexes = [
            models.Index(fields=["code"], name="district_code_idx"),
        ]

    def __str__(self):
        return f"{self.name}, {self.code}"
