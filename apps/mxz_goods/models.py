from django.db import models


# Create your models here.
class MxzGoodCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='分类名称', default='')
    parent = models.ForeignKey("self", null=True, blank=True, verbose_name="父类", on_delete=models.DO_NOTHING,
                               related_name="sub_cat")
    logo = models.ImageField(verbose_name="分类logo图片", upload_to="uploads/goods_img/")
    is_nav = models.BooleanField(default=False, verbose_name="是否显示在导航栏")
    sort = models.IntegerField(verbose_name="排序")


class MxzGoods(models.Model):
    STATUS = {
        (0, "正常"),
        (1, "下架"),
    }
    name = models.CharField(max_length=50, verbose_name="商品名称", default="")
    category = models.ForeignKey(MxzGoodCategory, blank=True, null=True, verbose_name="商品分类", on_delete=models.DO_NOTHING)
    market_price = models.DecimalField(max_digits=8, default=0, decimal_places=2, verbose_name="市场价格")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="实际价格")
    status = models.IntegerField(default=0, choices=STATUS)

