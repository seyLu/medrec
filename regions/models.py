from django.db import models


class Region(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["code"], name="region_code_idx"),
        ]

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}, {self.code}"


class Province(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["code"], name="province_code_idx"),
        ]

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    region = models.ForeignKey(
        Region, to_field="code", on_delete=models.CASCADE, default="0800000000"
    )

    def __str__(self) -> str:
        return f"{self.name}, {self.code}"


class City(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["code"], name="city_code_idx"),
        ]

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    province = models.ForeignKey(
        Province, to_field="code", on_delete=models.CASCADE, default="0831600000"
    )
    region = models.ForeignKey(
        Region, to_field="code", on_delete=models.CASCADE, default="0800000000"
    )

    def __str__(self) -> str:
        return f"{self.name}, {self.code}"


class District(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["code"], name="district_code_idx"),
        ]

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    city = models.ForeignKey(
        City, to_field="code", on_delete=models.CASCADE, default="0831600000"
    )
    province = models.ForeignKey(
        Province, to_field="code", on_delete=models.CASCADE, default="0831600000"
    )
    region = models.ForeignKey(
        Region, to_field="code", on_delete=models.CASCADE, default="0800000000"
    )

    def __str__(self) -> str:
        return f"{self.name}, {self.code}"
