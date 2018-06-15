from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    '''
    购物车类
    '''
    def __init__(self, request):
        '''
        初始化购物车
        :param request: 将购物车与session关联
        '''

        # 添加一个实例属性session，便于类里其他方法访问session
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart: # 代表session中么有cart这个key，也就是session没有存储购物车相关信息
            cart = self.session[settings.CART_SESSION_ID] = {}

        # 再添加一个实例属性
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        '''添加商品到购物车，或者更新商品数量
        '''
        product_id = str(product.id) # 因为JSON的key值只能为字符串
        if product_id not in self.cart: # cart为一个字典类型，self.cart返回字典的key列表
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        # 更新session中的cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # 标记session为’modified',会自动存储
        self.session.modified = True

    def remove(self, product):
        '''从购物车移去一件商品
        '''
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        '''迭代购物车中的每一个元素，
        并且从数据库中获取相应的商品。
        '''
        # 获取购物车中所有元素的id
        product_ids = self.cart.keys()

        # 查询数据库，提取相应的商品对象
        products = Product.objects.filter(id__in=product_ids)

        # 把商品对象也加入购物车
        for product in products:
            self.cart[str(product.id)]['product'] = product

        # 构造一个生成器
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        '''
        数出购物车中所有的元素
        :return: 购物车商品总数
        '''
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # 删除session中的购物车
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True


